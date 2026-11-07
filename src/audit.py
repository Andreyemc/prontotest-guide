# -*- coding: utf-8 -*-
"""Сверка объявленных значений Pronto.pen с computed-стилями собранных страниц.

Значения из макета берутся из файла и резолвятся через его же variables,
ничего не вводится руками.
"""
import asyncio, json, pathlib, re, sys
from playwright.async_api import async_playwright

PEN = json.load(open("/mnt/user-data/uploads/Desktop/Pronto.pen"))
VARS = PEN["variables"]
SITE = pathlib.Path("/home/claude/prontotest")
PH = pathlib.Path("/home/claude/shots/placeholder.webp").read_bytes()
LOCAL = SITE / "assets/images/pronto"
SLUG = {p.stem: p for p in LOCAL.glob("*.webp")}

index = {}


def walk(n, path=""):
    p = f"{path}/{n.get('name')}"
    index[p] = n
    for c in n.get("children") or []:
        walk(c, p)


for f in PEN["children"]:
    walk(f)


def tok(v):
    if isinstance(v, str) and v.startswith("$"):
        return VARS.get(v[1:], {}).get("value", v)
    return v


def css_color(v):
    v = tok(v)
    if not isinstance(v, str) or not v.startswith("#"):
        return None
    h = v[1:]
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if len(h) == 8:
        a = int(h[6:8], 16) / 255
        if a >= 0.999:
            return f"rgb({r}, {g}, {b})"
        return f"rgba({r}, {g}, {b}, {round(a, 2):g})"
    return f"rgb({r}, {g}, {b})"


def expected(node):
    """Что макет объявляет у этого узла, в терминах CSS."""
    out = {}
    if "fontSize" in node:
        out["fontSize"] = f"{node['fontSize']}px"
    if "fontWeight" in node:
        w = node["fontWeight"]
        out["fontWeight"] = "400" if w == "normal" else str(w)
    if "fontFamily" in node:
        out["fontFamily"] = tok(node["fontFamily"])
    if "lineHeight" in node and "fontSize" in node:
        out["lineHeight"] = f"{round(node['lineHeight'] * node['fontSize'], 2):g}px"
    if "letterSpacing" in node:
        out["letterSpacing"] = f"{round(node['letterSpacing'], 3):g}px"
    if node.get("type") == "text" and "fill" in node:
        c = css_color(node["fill"])
        if c:
            out["color"] = c
    if node.get("type") in ("frame", "rectangle") and isinstance(node.get("fill"), str):
        c = css_color(node["fill"])
        if c:
            out["backgroundColor"] = c
    if "cornerRadius" in node:
        r = tok(node["cornerRadius"])
        out["borderRadius"] = f"{min(r, 999)}px" if isinstance(r, (int, float)) else None
    if "padding" in node:
        pad = node["padding"]
        pad = [pad] * 4 if isinstance(pad, (int, float)) else pad
        if len(pad) == 2:
            pad = [pad[0], pad[1], pad[0], pad[1]]
        out["padding"] = " ".join(f"{x}px" for x in pad)
    if "gap" in node:
        out["gap"] = f"{node['gap']}px"
    if "opacity" in node:
        out["opacity"] = str(node["opacity"])
    return {k: v for k, v in out.items() if v is not None}


PROBE = """(sel) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const c = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  let pad = c.paddingTop + " " + c.paddingRight + " " + c.paddingBottom + " " + c.paddingLeft;
  return { fontSize: c.fontSize, fontWeight: c.fontWeight,
           fontFamily: c.fontFamily.split(",")[0].replace(/["']/g, ""),
           lineHeight: c.lineHeight, letterSpacing: c.letterSpacing,
           color: c.color, backgroundColor: c.backgroundColor,
           borderRadius: c.borderTopLeftRadius, padding: pad, gap: c.gap,
           opacity: c.opacity, w: Math.round(r.width), h: Math.round(r.height) };
}"""


def norm(k, v):
    if v is None:
        return v
    if k == "letterSpacing" and v == "normal":
        return "0px"
    if k == "lineHeight" and v == "normal":
        return v
    if k == "borderRadius" and v.endswith("px"):
        f = float(v[:-2])
        return "999px" if f >= 999 else f"{f:g}px"
    if k in ("fontSize", "lineHeight", "gap") and v.endswith("px"):
        return f"{float(v[:-2]):g}px"
    if k == "padding":
        return " ".join(f"{float(x[:-2]):g}px" for x in v.split())
    return v


async def run(url, pairs, width, title, setup=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--font-render-hinting=none"])
        pg = await b.new_page(viewport={"width": width, "height": 1000})

        async def route(r, q):
            m = re.search(r"/guia/([a-z0-9-]+)/", q.url)
            s = m.group(1) if m else ""
            await r.fulfill(status=200, body=SLUG[s].read_bytes() if s in SLUG else PH,
                            headers={"content-type": "image/webp"})

        await pg.route("**storage.prontotest.net/**", route)
        await pg.goto((SITE / url).as_uri(), wait_until="networkidle")
        await pg.wait_for_timeout(900)
        await pg.evaluate("""() => document.querySelectorAll('.reveal').forEach(e => {
            e.classList.add('is-in'); e.style.animation='none'; e.style.opacity=1; e.style.transform='none'; })""")
        if setup:
            await pg.click(setup)
            await pg.wait_for_timeout(700)
        bad = tot = 0
        print(f"\n=== {title} ===")
        for pen_path, sel, only in pairs:
            node = index.get(pen_path)
            if node is None:
                print(f"  ? нет в макете: {pen_path}")
                continue
            exp = expected(node)
            if only:
                exp = {k: v for k, v in exp.items() if k in only}
            got = await pg.evaluate(PROBE, sel)
            if got is None:
                print(f"  ✗ нет на странице: {sel}")
                bad += 1
                continue
            diffs = []
            for k, v in exp.items():
                a, c = norm(k, v), norm(k, got.get(k))
                if a != c:
                    diffs.append(f"{k}: макет {a} ≠ прод {c}")
            tot += 1
            if diffs:
                bad += 1
                print(f"  ✗ {pen_path.split('/')[-1]}  [{sel}]")
                for d in diffs:
                    print(f"      {d}")
        print(f"  — проверено {tot}, расхождений {bad}")
        await b.close()
        return bad

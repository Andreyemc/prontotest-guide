# -*- coding: utf-8 -*-
"""Генерирует OG-карточки 1200×630 для хаба и статей в языке макета:
токены, шрифты, эйбров и плитка с обложкой — те же, что на сайте."""
import asyncio, html, json, pathlib, sys
from playwright.async_api import async_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build  # noqa: E402  (категории, флаг displayTitle, иконки)

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "og"
OUT.mkdir(parents=True, exist_ok=True)
SPRITE = (ROOT / "assets" / "icons.svg").read_text(encoding="utf-8")
FONTS = (ROOT / "assets" / "fonts").as_uri()
COVERS = ROOT / "assets" / "images" / "pronto"


def e(s):
    return html.escape(s, quote=True)


CSS = f"""
@font-face {{ font-family: "Geist"; src: url("{FONTS}/geist-variable.woff2") format("woff2"); font-weight: 100 900; }}
@font-face {{ font-family: "M PLUS U"; src: url("{FONTS}/mplusu-latin.woff2") format("woff2"); font-weight: 100 900; }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: 1200px; height: 630px; overflow: hidden; }}
body {{
  position: relative; background: #F1F5F9; color: #0F172A;
  font-family: "Geist", system-ui, sans-serif; -webkit-font-smoothing: antialiased;
}}
.glow {{ position: absolute; inset: 0; overflow: hidden; }}
.glow span {{ position: absolute; border-radius: 50%; filter: blur(100px); }}
.glow .a {{ width: 640px; height: 544px; left: 700px; top: -220px; background: #93C5FD47; }}
.glow .b {{ width: 760px; height: 646px; left: -300px; top: 240px; background: #2563EB2E; }}
.glow .c {{ width: 700px; height: 595px; left: 560px; top: 320px; background: #FFC53D3D; }}
.card {{
  position: absolute; inset: 0; display: flex; padding: 64px; gap: 48px; align-items: stretch;
}}
.col {{ flex: 1 1 auto; display: flex; flex-direction: column; justify-content: space-between; min-width: 0; }}
.logo {{ font-family: "M PLUS U"; font-weight: 900; font-size: 28px; line-height: 0.9; letter-spacing: -0.4px; }}
.eyebrow {{ display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }}
.eyebrow__tile {{
  display: inline-flex; align-items: center; justify-content: center;
  width: 34px; height: 34px; border-radius: 9px; background: rgba(15,23,42,.08);
}}
.eyebrow__tile svg {{ width: 20px; height: 20px; fill: #0F172A; }}
.eyebrow__label {{ font-size: 19px; font-weight: 700; letter-spacing: .6px; text-transform: uppercase; color: #566274; }}
.title {{ font-size: 50px; font-weight: 600; line-height: 1.1; letter-spacing: -0.5px; }}
.title--display {{
  font-family: "M PLUS U"; font-kerning: none; font-weight: 700;
  font-size: 54px; line-height: 1.02; letter-spacing: -0.6px; text-transform: uppercase;
}}
.title--hub {{ font-size: 64px; }}
.desc {{ margin-top: 20px; font-size: 26px; line-height: 1.15; color: #666666; }}
.date {{ font-size: 22px; font-weight: 600; color: #566274; }}
.tile {{ flex: none; width: 480px; border-radius: 32px; overflow: hidden; background: #fff; }}
.tile img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
"""


def page(body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{SPRITE}<div class="glow"><span class="a"></span><span class="b"></span><span class="c"></span></div>
<div class="card">{body}</div></body></html>"""


def article_html(a):
    cat = build.CATEGORY[a["slug"]]
    label, ic = build.CAT_LABEL[cat]
    disp = a["slug"] in build.DISPLAY_TITLE
    cover = (COVERS / f"{a['slug']}.webp").as_uri()
    return page(f"""
  <div class="col">
    <div class="logo">PRONTOTEST</div>
    <div>
      <div class="eyebrow"><span class="eyebrow__tile"><svg><use href="#i-{ic}"/></svg></span>
        <span class="eyebrow__label">{e(label)}</span></div>
      <div class="title{' title--display' if disp else ''}">{e(a['title'])}</div>
    </div>
    <div class="date">{e(a['published'])}</div>
  </div>
  <div class="tile"><img src="{cover}" alt=""></div>""")


def hub_html():
    cover = (COVERS / "averia-en-autovia-baliza-v16.webp").as_uri()
    return page(f"""
  <div class="col">
    <div class="logo">PRONTOTEST</div>
    <div>
      <div class="title title--display title--hub">{e(build.HUB_TITLE)}</div>
      <div class="desc">{e(build.HUB_DESC)}</div>
    </div>
    <div class="date">Tips from ProntoTest</div>
  </div>
  <div class="tile"><img src="{cover}" alt=""></div>""")


async def main():
    jobs = [("guide", hub_html())] + [(a["slug"], article_html(a)) for a in build.ARTICLES]
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--font-render-hinting=none"])
        pg = await b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        tmp = pathlib.Path("/tmp/og-render"); tmp.mkdir(exist_ok=True)
        for name, src in jobs:
            f = tmp / f"{name}.html"
            f.write_text(src, encoding="utf-8")
            await pg.goto(f.as_uri(), wait_until="load")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=90)
        await b.close()
    sizes = sorted(p.stat().st_size for p in OUT.glob("*.jpg"))
    print(f"{len(jobs)} карточек, {min(sizes)//1024}–{max(sizes)//1024} КБ, всего {sum(sizes)//1024} КБ")

asyncio.run(main())

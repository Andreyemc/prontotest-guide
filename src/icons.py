import json, sys, re, hashlib

PEN = sys.argv[1]
OUT = sys.argv[2]
d = json.load(open(PEN))

found = {}   # geometry-hash -> {names:set, geometry, viewBox, fillRule}

def walk(n):
    if n.get("type") in ("path", "icon") and n.get("geometry"):
        g = n["geometry"]
        h = hashlib.md5(g.encode()).hexdigest()[:8]
        e = found.setdefault(h, {"names": set(), "geometry": g,
                                 "viewBox": n.get("viewBox", [0, 0, 24, 24]),
                                 "fillRule": n.get("fillRule")})
        e["names"].add(n.get("name", ""))
    for c in n.get("children") or []:
        walk(c)

walk({"children": d["children"]})

PREFER = {
    "icon right of way": "traffic",
    "icon manoeuvres": "arrow-right",
    "icon traffic rules": "book-cover",
    "icon traffic signs": "warning-diamond",
    "icon lights": "energy",
    "icon road safety & accidents": "warning",
    "icon speed": "speedometer",
}

def slug(names):
    for n in sorted(names):
        if n.strip().lower() in PREFER:
            return PREFER[n.strip().lower()]
    # prefer a name that looks like "Icon xxx" but is not the bare word "Icon"
    cand = sorted(names, key=lambda s: (0 if (s.lower().startswith("icon") and s.strip().lower() != "icon") else 1, len(s)))
    s = cand[0]
    s = re.sub(r"^icon\s*", "", s, flags=re.I).strip()
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "icon"

used = set()
parts = []
report = []
for h, e in found.items():
    name = slug(e["names"])
    base = name
    i = 2
    while name in used:
        name = f"{base}-{i}"; i += 1
    used.add(name)
    vb = " ".join(str(x) for x in e["viewBox"])
    fr = f' fill-rule="{e["fillRule"]}"' if e.get("fillRule") else ""
    parts.append(f'<symbol id="i-{name}" viewBox="{vb}"><path d="{e["geometry"]}"{fr}/></symbol>')
    report.append(f"{name}  <-  {sorted(e['names'])}")

svg = ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">'
       + "".join(parts) + "</svg>\n")
open(OUT, "w").write(svg)
print("\n".join(sorted(report)))
print("total", len(parts))

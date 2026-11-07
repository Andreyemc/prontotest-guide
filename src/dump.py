"""Полный дамп узлов Pronto.pen — печатает ВСЕ ключи, ничего не скрывая."""
import json, sys

PEN = sys.argv[1]
FRAME = sys.argv[2] if len(sys.argv) > 2 else None
d = json.load(open(PEN))

SKIP = {"id", "name", "type", "children", "geometry", "viewBox"}


def fmt(n):
    parts = []
    for k, v in n.items():
        if k in SKIP:
            continue
        if isinstance(v, (dict, list)):
            v = json.dumps(v, ensure_ascii=False, separators=(",", ":"))
        parts.append(f"{k}={v}")
    if "geometry" in n:
        parts.append("geometry=<path>")
    return " ".join(parts)


def walk(n, depth=0):
    off = "OFF " if n.get("enabled") is False else ""
    print(f"{'  ' * depth}{off}[{n.get('id')}] {n.get('type')} {n.get('name')!r} :: {fmt(n)}")
    for c in n.get("children") or []:
        walk(c, depth + 1)


for f in d["children"]:
    if FRAME and f.get("id") != FRAME:
        continue
    walk(f)

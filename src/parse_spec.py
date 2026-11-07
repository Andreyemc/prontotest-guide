# -*- coding: utf-8 -*-
"""Разбирает ProntoTest-Guia-spec.md в data/guide.json.

Ничего не редактирует: тексты переносятся дословно.
"""
import json, re, sys, pathlib

SPEC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
text = SPEC.read_text(encoding="utf-8")

STORAGE = "https://storage.prontotest.net/my-bucket/prontotest/guia/"

# ---- таблица ассетов: | NN | [anim-x.svg](url) | вес | цикл | [cover-y.webp](url) |
assets = {}
for m in re.finditer(
    r"^\|\s*(\d{2})\s*\|\s*\[[^\]]+\]\((?P<anim>[^)]+)\)\s*\|\s*(?P<kb>[\d.]+)\s*\|"
    r"\s*(?P<loop>[\d.]+)\s*\|\s*\[[^\]]+\]\((?P<cover>[^)]+)\)\s*\|",
    text, re.M):
    assets[int(m.group(1))] = {
        "anim": m.group("anim"),
        "cover": m.group("cover"),
        "loop": float(m.group("loop")),
    }

# ---- секции статей
blocks = re.split(r"^### (\d{2})\. ", text, flags=re.M)[1:]
pairs = [(int(blocks[i]), blocks[i + 1]) for i in range(0, len(blocks), 2)]

DATE_RE = re.compile(
    r"Published\s+(?P<pub>\d{1,2}\s+\w+\s+\d{4})"
    r"(?:\s*·\s*Updated\s+(?P<upd>\d{1,2}\s+\w+\s+\d{4}))?")

MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], 1)}


def iso(d):
    if not d:
        return None
    day, mon, year = d.split()
    return f"{year}-{MONTHS[mon]:02d}-{int(day):02d}"


def field(body, label):
    m = re.search(rf"^- \*\*{label}:\*\*\s*(.+)$", body, re.M)
    return m.group(1).strip() if m else None


articles = []
for num, body in pairs:
    head, _, rest = body.partition("\n")
    title = head.strip()

    url = field(body, "URL") or ""
    slug = re.search(r"/en/guia/([a-z0-9-]+)", url).group(1)

    meta_title = field(body, "Meta title")
    dates_raw = field(body, "Даты") or ""
    dm = DATE_RE.search(dates_raw)
    published, updated = dm.group("pub"), dm.group("upd")

    anim_alt = field(body, "Alt анимации")
    caption = field(body, "Подпись обложки")
    more = [int(x) for x in re.findall(r"\d+", field(body, "More tips") or "")]

    takeaway = re.search(r"\*\*Key takeaway\.\*\*\s*(.+?)\n\n", body, re.S).group(1).strip()
    intro = re.search(r"\*\*Intro\.\*\*\s*(.+?)\n\n", body, re.S).group(1).strip()

    notice_block = re.search(r"\*\*What to notice\*\*\n\n(.+?)\n\n\*\*What to do\.\*\*",
                             body, re.S).group(1)
    notice = [l[2:].strip() for l in notice_block.strip().split("\n") if l.startswith("- ")]

    action = re.search(r"\*\*What to do\.\*\*\s*(.+?)(?:\n\n|\Z)", body, re.S).group(1).strip()

    a = assets[num]
    articles.append({
        "n": num,
        "slug": slug,
        "title": title,
        "metaTitle": meta_title,
        "takeaway": takeaway,
        "published": published,
        "publishedIso": iso(published),
        "updated": updated,
        "updatedIso": iso(updated),
        "animation": a["anim"],
        "animationAlt": anim_alt,
        "cover": a["cover"],
        "coverCaption": caption,
        "loop": a["loop"],
        "intro": intro,
        "notice": notice,
        "action": action,
        "moreTips": more,
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")

print("articles:", len(articles))
for a in articles:
    assert a["takeaway"] and a["intro"] and a["action"], a["slug"]
    assert 2 <= len(a["notice"]) <= 4, (a["slug"], len(a["notice"]))
    assert len(a["moreTips"]) == 2, a["slug"]
    assert a["animation"].startswith(STORAGE) and a["cover"].startswith(STORAGE), a["slug"]
print("longest action:", max(len(a["action"]) for a in articles))
print("longest title:", max(len(a["title"]) for a in articles))
print("no updated:", [a["n"] for a in articles if not a["updated"]])

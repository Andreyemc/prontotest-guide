# -*- coding: utf-8 -*-
"""Собирает раздел ProntoTest · Guide: хаб и 20 страниц статей.

Разметка и значения — из макета Pronto.pen, тексты — из ProntoTest-Guia-spec.md
(data/guide.json). Тексты переносятся дословно, без редактуры.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPRITE = (ROOT / "assets" / "icons.svg").read_text(encoding="utf-8").strip()
ARTICLES = json.loads((ROOT / "data" / "guide.json").read_text(encoding="utf-8"))

CANON = "https://prontotest.net"
PER_PAGE = 9

# ---------------------------------------------------------------- категории ---
# В контент-спеке категорий нет, в макете они есть у десяти статей — здесь
# сохранены макетные и по той же логике проставлены остальные.
CATEGORY = {
    "averia-en-autovia-baliza-v16": "road-safety",
    "glorieta-dos-carriles-salida": "right-of-way",
    "adelantar-ciclista-prohibido-adelantar": "manoeuvres",
    "luces-antiniebla-cuando-encender": "lights",
    "margen-de-velocidad-sobre-el-limite": "speed",
    "parada-o-estacionamiento-bajarse-del-coche": "traffic-rules",
    "stop-sin-visibilidad-parar-dos-veces": "traffic-signs",
    "semaforo-verde-no-significa-entrar": "right-of-way",
    "carril-de-aceleracion-decidir-al-principio": "manoeuvres",
    "aquaplaning-agua-en-la-rodada": "road-safety",
    "glorieta-preferencia-quien-circula-dentro": "right-of-way",
    "estrechamiento-prioridad-sentido-contrario": "right-of-way",
    "entrada-prohibida-navegador": "traffic-signs",
    "paso-a-nivel-no-detenerse-en-las-vias": "road-safety",
    "carril-bus-girar-a-la-derecha": "traffic-rules",
    "ambulancia-detras-semaforo-en-rojo": "right-of-way",
    "zona-coexistencia-peaton-prioridad": "right-of-way",
    "zona-escolar-ninos-entre-coches": "road-safety",
    "giro-derecha-peatones-cruzando-en-verde": "right-of-way",
    "carril-bici-girar-a-la-derecha": "right-of-way",
}

CATEGORIES = [
    ("traffic-rules", "Traffic rules", "book-cover"),
    ("traffic-signs", "Traffic signs", "warning-diamond"),
    ("right-of-way", "Right of way", "traffic"),
    ("speed", "Speed", "speedometer"),
    ("manoeuvres", "Manoeuvres", "arrow-right"),
    ("lights", "Lights", "energy"),
    ("road-safety", "Road safety & accidents", "warning"),
    ("documents", "Documents", "book-cover"),
]
CAT_LABEL = {k: (label, icon) for k, label, icon in CATEGORIES}

CHIPS = [("all", "All")] + [(k, "Road safety" if k == "road-safety" else label)
                            for k, label, _ in CATEGORIES]

NAV = [
    ("Free DGT test", "#", False),
    ("Guide", "{base}index.html", True),
    ("Benefits", "#", False),
    ("For whom", "#", False),
    ("Reviews", "#", False),
    ("Prices", "#", False),
    ("FAQ", "#", False),
    ("Team", "#", False),
]

FOOTER_COLS = [
    ("Product", ["Free DGT test", "Complete category B mock exam", "Traffic rules",
                 "Right of way", "Speed", "Download app"]),
    ("ProntoTest", ["Home", "Guide", "Team", "Support"]),
    ("Social", ["YouTube", "X", "LinkedIn", "Instagram"]),
    ("Legal", ["Privacy Policy", "Terms of Service", "Cookie settings"]),
]

DISCLAIMER = ("ProntoTest is an independent study service and is not affiliated with the DGT. "
              "Question bank reviewed by hand · July 2026 · Juan Manuel Llergo, driving "
              "instructor. Passing our mock exams does not guarantee passing the official test.")

HUB_TITLE = "Useful tips from ProntoTest"
HUB_DESC = ("Real road situations in Spain explained step by step: what to look for, "
            "what to do and why, with official sources.")
HUB_META_TITLE = "Useful driving tips for Spain | ProntoTest"
HUB_META_DESC = ("Practical ProntoTest tips for real situations at the wheel: roundabouts, "
                 "cyclists, lights, breakdowns and more, with official DGT and BOE sources.")

CTA_EYEBROW = "Free DGT test"
CTA_TITLE = "Read the tips, then check yourself in the free category B mock exam"
CTA_BUTTON = "Practise with free tests"
CTA_ARTICLE_BUTTON = "Keep practising with free tests"


# ------------------------------------------------------------------ helpers ---

def e(s):
    return html.escape(s, quote=True)


def icon(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def eyebrow(icon_name, label, cls=""):
    c = f" {cls}" if cls else ""
    return (f'<span class="eyebrow{c}"><span class="eyebrow__tile">{icon(icon_name)}</span>'
            f'<span class="eyebrow__label">{e(label)}</span></span>')


SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[“"(A-Z0-9])')


def to_steps(paragraph):
    """Делит «What to do» на шаги по границам предложений, не меняя текст."""
    guarded = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + "\x00" + m.group(2), paragraph)
    parts = [p.replace("\x00", ".").strip() for p in SENT_SPLIT.split(guarded)]
    return [p for p in parts if p]


def fmt_dates(a):
    out = f'<time datetime="{a["publishedIso"]}">{e(a["published"])}</time>'
    if a["updated"]:
        out += f' · Updated <time datetime="{a["updatedIso"]}">{e(a["updated"])}</time>'
    return out


def article_href(slug, base):
    return f"{base}guia/{slug}.html"


# ------------------------------------------------------------------ partials ---

def head(*, title, description, canonical, base, extra=""):
    nois = '<meta name="robots" content="noindex,follow">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
{nois}
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="es" href="{canonical.replace('/en/', '/')}">
<link rel="alternate" hreflang="en" href="{canonical}">
<link rel="alternate" hreflang="ru" href="{canonical.replace('/en/', '/ru/')}">
<link rel="alternate" hreflang="x-default" href="{canonical.replace('/en/', '/')}">
<meta name="theme-color" content="#F1F5F9">
<link rel="preload" href="{base}assets/fonts/geist-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/mplusu-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/css/styles.css">
<link rel="preconnect" href="https://storage.prontotest.net" crossorigin>
{extra}</head>
<body>
{SPRITE}
"""


def header(base):
    links = "\n".join(
        '        <a class="nav__link{cls}" href="{href}"{cur}>{label}</a>'.format(
            cls=" is-active" if active else "",
            href=href.format(base=base),
            cur=' aria-current="page"' if active else "",
            label=e(label))
        for label, href, active in NAV)
    return f"""  <header class="header" data-header>
    <div class="header__inner">
      <a class="logo" href="{base}index.html">PRONTOTEST</a>
      <div class="header__right">
        <nav class="nav" aria-label="Main">
{links}
        </nav>
        <div class="header__buttons">
          <button class="btn-glass btn-glass--icon" type="button" aria-label="Change language" data-ua="globe">{icon("globe")}</button>
          <a class="btn-glass" href="#">Get app</a>
        </div>
      </div>
    </div>
  </header>

  <header class="header-m" data-header>
    <div class="header-m__inner">
      <a class="logo" href="{base}index.html">PRONTOTEST</a>
      <div class="header-m__icons">
        <button class="icon-round" type="button" aria-label="Search">{icon("search")}</button>
        <button class="icon-round" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu" data-menu-toggle data-ua="menu-v4"><span class="burger" aria-hidden="true"><span></span><span></span><span></span></span></button>
      </div>
    </div>
  </header>
"""


GLOW = """    <div class="glow" aria-hidden="true">
      <div class="glow__stage">
        <span class="glow__blob glow__b1"></span>
        <span class="glow__blob glow__b2"></span>
        <span class="glow__blob glow__b3"></span>
        <span class="glow__blob glow__b4"></span>
        <span class="glow__blob glow__b5"></span>
        <span class="glow__blob glow__b6"></span>
        <span class="glow__blob glow__b7"></span>
        <span class="glow__blob glow__b8"></span>
      </div>
      <span class="glow__fade"></span>
    </div>
"""


def footer(base):
    cols = []
    for title, items in FOOTER_COLS:
        lis = "\n".join(f'            <li><a class="footer__link" href="#">{e(i)}</a></li>'
                        for i in items)
        cols.append(f"""        <div class="footer__col">
          <h2 class="footer__col-title">{title.upper()}</h2>
          <ul>
{lis}
          </ul>
        </div>""")
    cols = "\n".join(cols)
    return f"""  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <div class="footer__links">
{cols}
        </div>
        <div class="footer__right">
          <button class="lang" type="button" data-ua="globe">{icon("globe")}<span>EN</span></button>
          <div class="badges">
            <a href="#"><img src="{base}assets/images/badges/appstore.png" alt="Download on the App Store" width="149" height="44" loading="lazy"></a>
            <a href="#"><img src="{base}assets/images/badges/googleplay.png" alt="Get it on Google Play" width="149" height="44" loading="lazy"></a>
          </div>
        </div>
      </div>

      <div class="wordmark">
        <span class="u-visually-hidden">ProntoTest</span>
        <svg viewBox="0 0 1200 156" aria-hidden="true" focusable="false">
          <text x="0" y="128" font-size="173" textLength="1200" lengthAdjust="spacingAndGlyphs">PRONTOTEST</text>
        </svg>
      </div>

      <div class="footer__legal">
        <p class="footer__copy">2026 © ProntoTest. All rights reserved</p>
        <p class="footer__disclaimer">{e(DISCLAIMER)}</p>
      </div>
    </div>
  </footer>
"""


def menu(base):
    items = "\n".join(
        '        <a class="menu__item{cls}" href="{href}" style="--i:{n}"><span>{label}</span>{chev}</a>'.format(
            cls=" is-active" if active else "", href=href.format(base=base),
            n=n, label=e(label), chev=icon("chevron-right"))
        for n, (label, href, active) in enumerate(NAV))
    return f"""  <div class="menu" id="menu" hidden>
    <nav class="menu__nav" aria-label="Mobile">
{items}
    </nav>
    <div class="menu__footer">
      <a class="menu__cta" href="#">Get the app</a>
      <div class="menu__utility">
        <div class="badges">
          <a href="#"><img src="{base}assets/images/badges/appstore.png" alt="Download on the App Store" width="108" height="32" loading="lazy"></a>
          <a href="#"><img src="{base}assets/images/badges/googleplay.png" alt="Get it on Google Play" width="108" height="32" loading="lazy"></a>
        </div>
        <button class="lang" type="button" data-ua="globe">{icon("globe")}<span>EN</span></button>
      </div>
    </div>
  </div>
"""


def tail(base, script="app.js"):
    return f"""  <script src="{base}assets/js/{script}" defer></script>
</body>
</html>
"""


def promo(base, button_label):
    return f"""      <div class="promo">
        <div class="promo__top">
          {eyebrow("checkmark-in-circle", CTA_EYEBROW)}
          <p class="promo__title">{e(CTA_TITLE)}</p>
        </div>
        <a class="btn-pill" href="#">{e(button_label)}</a>
      </div>"""


# ----------------------------------------------------------------- шаблоны ----
# Раскладка bento из макета: ряд из двух больших, ряд из трёх малых,
# фича во всю ширину, ещё ряд из трёх малых. Один цикл — девять карточек.
ROWS = [
    [("large", "img", "", False), ("large", "img", "", True)],
    [("small", "solid", "soft", False), ("small", "img", "ink", False),
     ("small", "img", "", False)],
    [("full", "feature", "", True)],
    [("small", "solid", "primary", True), ("small", "img", "", False),
     ("small", "solid", "sun", False)],
]


def tile_classes(i):
    """Классы плитки по её позиции среди видимых карточек."""
    flat = [c for row in ROWS for c in row]
    size, kind, tone, display = flat[i % len(flat)]
    cls = ["tile", f"tile--{size}", f"tile--{kind}"]
    if tone:
        cls.append(f"tile--{tone}")
    if display:
        cls.append("tile--display")
    return " ".join(cls)


def render_card(a, base, pos, hidden):
    cat = CATEGORY[a["slug"]]
    label, ic = CAT_LABEL[cat]
    hid = " hidden" if hidden else ""
    return f"""        <a class="{tile_classes(pos)}" href="{article_href(a['slug'], base)}" data-card data-category="{cat}"{hid}>
          <span class="tile__media"><img src="{a['cover']}" alt="" width="1200" height="675" loading="lazy" decoding="async"></span>
          <span class="tile__scrim"></span>
          <span class="tile__body">
            <span class="tile__top">
              {eyebrow(ic, label)}
              <span class="tile__title">{e(a['title'])}</span>
            </span>
            <time class="tile__date" datetime="{a['publishedIso']}">{e(a['published'])}</time>
          </span>
        </a>"""



# --------------------------------------------------------------------- хаб ----

def build_hub():
    total_pages = -(-len(ARTICLES) // PER_PAGE)
    chips = "\n".join(
        '          <button class="chip{cls}" type="button" data-chip="{k}" aria-pressed="{p}">{label}</button>'.format(
            cls=" is-active" if k == "all" else "", k=k,
            p="true" if k == "all" else "false", label=e(label))
        for k, label in CHIPS)

    cards = "\n".join(render_card(a, "", i % PER_PAGE, hidden=i >= PER_PAGE)
                      for i, a in enumerate(ARTICLES))

    pages = "\n".join(
        f'        <a class="pager__item{" is-active" if n == 1 else ""}" href="#" data-page="{n}"'
        f'{" aria-current=&#34;page&#34;" if n == 1 else ""} aria-label="Page {n}">{n}</a>'
        for n in range(1, total_pages + 1))
    # aria-current задаётся скриптом, в статической разметке только на первой
    pages = pages.replace(' aria-current=&#34;page&#34;', ' aria-current="page"')

    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "name": "ProntoTest", "legalName": "DevArch OÜ",
             "email": "info@prontotest.net", "url": CANON},
            {"@type": "WebSite", "name": "ProntoTest", "url": CANON},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{CANON}/en/"},
                {"@type": "ListItem", "position": 2, "name": "Guide", "item": f"{CANON}/en/guia"},
            ]},
            {"@type": "CollectionPage", "name": HUB_TITLE, "description": HUB_META_DESC,
             "url": f"{CANON}/en/guia"},
        ],
    }, ensure_ascii=False)

    og = f"""<meta property="og:type" content="website">
<meta property="og:title" content="{e(HUB_TITLE)}">
<meta property="og:description" content="{e(HUB_META_DESC)}">
<meta property="og:url" content="{CANON}/en/guia">
<meta property="og:image" content="{CANON}/assets/test_dgt-98c29666.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ld}</script>
"""

    return (head(title=HUB_META_TITLE, description=HUB_META_DESC,
                 canonical=f"{CANON}/en/guia", base="", extra=og)
            + f"""  <div class="page">
{GLOW}
{header("")}
    <main class="body container">
      <div class="page-head">
        <h1 class="page-head__title">{e(HUB_TITLE)}</h1>
        <p class="page-head__desc">{e(HUB_DESC)}</p>
      </div>

      <div class="filters">
        <div class="chips" role="group" aria-label="Topics">
{chips}
        </div>
        <label class="search">
          {icon("search")}
          <input type="search" placeholder="Search tips" aria-label="Search tips">
        </label>
      </div>

      <div class="bento" data-bento data-per-page="{PER_PAGE}">
{cards}
      </div>

{promo("", CTA_BUTTON)}

      <nav class="pager" aria-label="Tip pages" data-pager>
        <a class="pager__item is-disabled" href="#" data-page="prev" aria-disabled="true" data-ua="arrow-left">{icon("arrow-left")}<span>Previous</span></a>
{pages}
        <a class="pager__item" href="#" data-page="next" data-ua="arrow-right"><span>Next</span>{icon("arrow-right")}</a>
      </nav>
    </main>
{menu("")}
  </div>

{footer("")}
{tail("")}""")


# ------------------------------------------------------------------ статья ----

def build_article(a):
    base = "../"
    cat = CATEGORY[a["slug"]]
    label, ic = CAT_LABEL[cat]
    canonical = f"{CANON}/en/guia/{a['slug']}"

    notice = "\n".join(f'            <li>{icon("warning")}<span>{e(b)}</span></li>'
                       for b in a["notice"])
    steps = "\n".join(
        f'            <li><span class="steps__num">{n}</span><span>{e(s)}</span></li>'
        for n, s in enumerate(to_steps(a["action"]), 1))

    by_n = {x["n"]: x for x in ARTICLES}
    more = "\n".join(f"""          <a class="mini reveal" href="{article_href(m['slug'], base)}" style="--delay:{i * 60}ms">
            {eyebrow(CAT_LABEL[CATEGORY[m['slug']]][1], CAT_LABEL[CATEGORY[m['slug']]][0], "eyebrow--plain")}
            <h3 class="mini__title">{e(m['title'])}</h3>
            <figure class="mini__figure"><img src="{m['cover']}" alt="" width="1200" height="675" loading="lazy"></figure>
          </a>""" for i, m in enumerate(by_n[n] for n in a["moreTips"]))

    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "name": "ProntoTest", "legalName": "DevArch OÜ",
             "email": "info@prontotest.net", "url": CANON},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{CANON}/en/"},
                {"@type": "ListItem", "position": 2, "name": "Guide", "item": f"{CANON}/en/guia"},
                {"@type": "ListItem", "position": 3, "name": a["title"], "item": canonical},
            ]},
            {"@type": "ImageObject", "contentUrl": a["cover"], "caption": a["coverCaption"],
             "width": 1200, "height": 675},
            {"@type": "Article", "headline": a["title"], "description": a["takeaway"],
             "image": a["cover"], "datePublished": a["publishedIso"],
             "dateModified": a["updatedIso"] or a["publishedIso"],
             "author": {"@type": "Organization", "name": "ProntoTest"},
             "publisher": {"@type": "Organization", "name": "ProntoTest"},
             "mainEntityOfPage": canonical},
        ],
    }, ensure_ascii=False)

    og_img = f"{CANON}/og/guia/{a['slug']}.en.png"
    og = f"""<meta property="og:type" content="article">
<meta property="og:title" content="{e(a['title'])}">
<meta property="og:description" content="{e(a['takeaway'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:alt" content="ProntoTest card: {e(a['title'])}">
<meta property="article:published_time" content="{a['publishedIso']}">
<meta property="article:modified_time" content="{a['updatedIso'] or a['publishedIso']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(a['title'])}">
<meta name="twitter:description" content="{e(a['takeaway'])}">
<meta name="twitter:image" content="{og_img}">
<script type="application/ld+json">{ld}</script>
"""

    share = f"""            <div class="head-actions">
              <button class="btn-secondary" type="button" data-share data-ua="share">{icon("share")}<span>Share</span></button>
              <button class="btn-secondary" type="button" data-copy-link data-ua="copy">{icon("link")}<span>Copy link</span></button>
            </div>"""

    return (head(title=a["metaTitle"], description=a["takeaway"],
                 canonical=canonical, base=base, extra=og)
            + f"""  <div class="page">
{GLOW}
{header(base)}
    <main class="article-body container">
      <article class="panel">
        <header class="article-head measure">
          {eyebrow(ic, f"Guide · {label}")}
          <p class="article-dates">{fmt_dates(a)}</p>
          <h1 class="article-title">{e(a['title'])}</h1>
          <p class="article-lede">{e(a['takeaway'])}</p>
          <div class="head-row">
            <div class="author">
              <span class="author__avatar">{icon("energy")}</span>
              <span class="author__name">By ProntoTest</span>
            </div>
{share}
          </div>
        </header>

        <figure class="article-hero">
          <img src="{a['animation']}" alt="{e(a['animationAlt'])}" width="1200" height="675">
        </figure>

        <div class="article-column measure">
          <p class="caption">{e(a['coverCaption'])}</p>

          <div class="text-block">
            <p>{e(a['intro'])}</p>

            <h2>What to notice</h2>
            <ul class="bullets">
{notice}
            </ul>

            <h2>What to do</h2>
            <ol class="steps">
{steps}
            </ol>
          </div>

          <div class="head-row head-row--end">
{share}
          </div>
        </div>
      </article>

{promo(base, CTA_ARTICLE_BUTTON)}

      <section class="more">
        <div class="more__head">
          <h2 class="more__title">More tips</h2>
          <a class="more__link" href="{base}index.html">All tips{icon("chevron-right")}</a>
        </div>
        <div class="more__row more__row--two">
{more}
        </div>
      </section>
    </main>
{menu(base)}
  </div>

{footer(base)}
{tail(base)}""")


# -------------------------------------------------------------------- main ----

if __name__ == "__main__":
    (ROOT / "index.html").write_text(build_hub(), encoding="utf-8")
    out = ROOT / "guia"
    out.mkdir(exist_ok=True)
    for a in ARTICLES:
        (out / f"{a['slug']}.html").write_text(build_article(a), encoding="utf-8")
    old = ROOT / "article.html"
    if old.exists():
        old.unlink()
    print("hub + ", len(ARTICLES), "articles")
    counts = [len(to_steps(a["action"])) for a in ARTICLES]
    print("steps per article:", counts)

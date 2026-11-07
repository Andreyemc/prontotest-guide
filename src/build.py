# -*- coding: utf-8 -*-
"""Собирает статические страницы ProntoTest · Guide из общих частей."""
import os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPRITE = (ROOT / "assets" / "icons.svg").read_text(encoding="utf-8").strip()


def icon(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


NAV = [
    ("Free DGT test", "#", False),
    ("Guide", "index.html", True),
    ("Benefits", "#", False),
    ("For whom", "#", False),
    ("Reviews", "#", False),
    ("Prices", "#", False),
    ("FAQ", "#", False),
    ("Team", "#", False),
]


def head(title, description, css_extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#F1F5F9">
<link rel="preload" href="assets/fonts/geist-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/mplusu-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css">{css_extra}
</head>
<body>
{SPRITE}
"""


def header():
    links = "\n".join(
        '        <a class="nav__link{cls}" href="{href}"{cur}>{label}</a>'.format(
            cls=" is-active" if active else "",
            href=href,
            cur=' aria-current="page"' if active else "",
            label=label,
        )
        for label, href, active in NAV
    )
    return f"""  <header class="header" data-header>
    <div class="header__inner">
      <a class="logo" href="index.html">PRONTOTEST</a>
      <div class="header__right">
        <nav class="nav" aria-label="Main">
{links}
        </nav>
        <div class="header__buttons">
          <button class="btn-glass btn-glass--icon" type="button" aria-label="Change language">{icon("globe")}</button>
          <a class="btn-glass" href="#">Get app</a>
        </div>
      </div>
    </div>
  </header>

  <header class="header-m" data-header>
    <div class="header-m__inner">
      <a class="logo" href="index.html">PRONTOTEST</a>
      <div class="header-m__icons">
        <button class="icon-round" type="button" aria-label="Search">{icon("search")}</button>
        <button class="icon-round" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu" data-menu-open>{icon("menu")}</button>
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

FOOTER_COLS = [
    ("Product", ["Free DGT test", "Category B mock exam", "Traffic rules", "Right of way", "Speed", "Download app"]),
    ("ProntoTest", ["Home", "Guide", "Team", "Support"]),
    ("Social", ["YouTube", "X", "LinkedIn", "Instagram"]),
    ("Legal", ["Privacy Policy", "Terms of Service", "Cookie settings"]),
]

DISCLAIMER = ("ProntoTest is an independent study service and is not affiliated with the DGT. "
              "Questions are reviewed by hand against the official question bank · July 2026 · "
              "Juan Martínez, driving instructor. Passing our mock exams does not guarantee "
              "passing the official test.")


def footer():
    cols = []
    for title, items in FOOTER_COLS:
        lis = "\n".join(f'            <li><a class="footer__link" href="#">{i}</a></li>' for i in items)
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
          <button class="lang" type="button">{icon("globe")}<span>EN</span></button>
          <div class="badges">
            <a href="#"><img src="assets/images/badges/appstore.png" alt="Download on the App Store" width="149" height="44" loading="lazy"></a>
            <a href="#"><img src="assets/images/badges/googleplay.png" alt="Get it on Google Play" width="149" height="44" loading="lazy"></a>
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
        <p class="footer__disclaimer">{DISCLAIMER}</p>
      </div>
    </div>
  </footer>
"""


def menu():
    items = "\n".join(
        f'        <a class="menu__item{" is-active" if active else ""}" href="{href}" style="--i:{n}">'
        f'<span>{label}</span>{icon("chevron-right")}</a>'
        for n, (label, href, active) in enumerate(NAV)
    )
    return f"""  <div class="menu" id="menu" hidden>
    <div class="menu__header">
      <a class="logo" href="index.html">PRONTOTEST</a>
      <div class="header-m__icons">
        <button class="icon-round" type="button" aria-label="Search">{icon("search")}</button>
        <button class="icon-round" type="button" aria-label="Close menu" data-menu-close>
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>
        </button>
      </div>
    </div>
    <nav class="menu__nav" aria-label="Mobile">
{items}
    </nav>
    <div class="menu__footer">
      <a class="menu__cta" href="#">Get the app</a>
      <div class="menu__utility">
        <div class="badges">
          <a href="#"><img src="assets/images/badges/appstore.png" alt="Download on the App Store" width="108" height="32" loading="lazy"></a>
          <a href="#"><img src="assets/images/badges/googleplay.png" alt="Get it on Google Play" width="108" height="32" loading="lazy"></a>
        </div>
        <button class="lang" type="button">{icon("globe")}<span>EN</span></button>
      </div>
    </div>
  </div>
"""


TAIL = """  <script src="assets/js/app.js" defer></script>
</body>
</html>
"""

IMG = "assets/images/pronto/"

# ---------------------------------------------------------------- listing ---

CHIPS = ["All", "Traffic rules", "Traffic signs", "Right of way", "Speed",
         "Manoeuvres", "Lights", "Road safety", "Documents"]

TILES = [
    dict(kind="image", size="large", slug="glorieta-dos-carriles-salida",
         icon="traffic", cat="Right of way",
         title="Why you leave a roundabout only from the right-hand lane",
         display=False, date="2026-10-28", date_label="28 October 2026",
         alt="Top view of a two-lane roundabout with a car taking the exit from the right-hand lane"),
    dict(kind="image", size="large", slug="adelantar-ciclista-prohibido-adelantar",
         icon="arrow-right", cat="Manoeuvres",
         title="A solid line and a cyclist ahead: overtake or wait?",
         display=True, date="2026-09-23", date_label="23 September 2026",
         alt="A car behind a cyclist on a road with a solid centre line"),
    dict(kind="solid", tone="soft", size="small", icon="book-cover", cat="Traffic rules",
         title="Stepped out of the car “for a minute”? For the law, that’s already parking",
         display=False, date="2026-10-21", date_label="21 October 2026"),
    dict(kind="image", size="small", dark=True, slug="stop-sin-visibilidad-parar-dos-veces",
         icon="warning-diamond", cat="Traffic signs",
         title="A STOP sign and you can't see the road: why you stop twice",
         display=False, date="2026-10-14", date_label="14 October 2026",
         alt="A junction with a STOP sign where buildings block the view of the main road"),
    dict(kind="image", size="small", slug="luces-antiniebla-cuando-encender",
         icon="energy", cat="Lights",
         title="Fog lights in a downpour: when the rear one helps and when it dazzles",
         display=False, date="2026-10-07", date_label="7 October 2026",
         alt="Cars in heavy rain with rear fog lights on"),
    dict(kind="feature", slug="averia-en-autovia-baliza-v16",
         icon="warning", cat="Road safety & accidents",
         title="Broken down on the motorway: beacon on the roof, everyone behind the barrier",
         date="2026-11-04", date_label="4 November 2026",
         alt="An orange car on the hard shoulder of a motorway with a V-16 beacon on its roof"),
    dict(kind="solid", tone="primary", size="small", icon="traffic", cat="Right of way",
         title="Green, but you can't go: how not to get stuck in the middle of a junction",
         display=True, date="2026-09-30", date_label="30 September 2026"),
    dict(kind="image", size="small", slug="carril-de-aceleracion-decidir-al-principio",
         icon="arrow-right", cat="Manoeuvres",
         title="Joining the motorway: why it's all decided at the start of the acceleration lane",
         display=False, date="2026-09-16", date_label="16 September 2026",
         alt="A car accelerating along a slip road to merge onto a motorway"),
    dict(kind="solid", tone="sun", size="small", icon="speedometer", cat="Speed",
         title="The instructor says “speed up”, the sign says 30: who do you listen to?",
         display=False, date="2026-09-09", date_label="9 September 2026"),
    dict(kind="image", size="large", slug="aquaplaning-agua-en-la-rodada",
         icon="warning", cat="Road safety & accidents",
         title="Steering suddenly gone light? That's how aquaplaning starts",
         display=True, date="2026-09-02", date_label="2 September 2026",
         alt="A car driving through standing water in the wheel ruts of a wet road"),
    dict(kind="cta"),
]


def eyebrow(name, label):
    return (f'<div class="eyebrow"><span class="eyebrow__tile">{icon(name)}</span>'
            f'<span class="eyebrow__label">{label}</span></div>')


def render_tile(t, i):
    delay = f"--delay:{min(i * 60, 300)}ms"
    if t["kind"] == "cta":
        return f"""        <div class="tile tile--large tile--cta reveal" style="{delay}">
          <div class="tile__top">
            {eyebrow("checkmark-in-circle", "Free DGT test")}
            <h3 class="tile__title">Read the tips, then check yourself in the free category B mock exam</h3>
          </div>
          <a class="btn-pill" href="#">Practise with free tests</a>
        </div>"""

    if t["kind"] == "feature":
        return f"""        <a class="tile tile--full tile--feature reveal" href="article.html" style="{delay}">
          <span class="tile__media"><img src="{IMG}{t['slug']}.webp" alt="{t['alt']}" width="1200" height="600" loading="lazy"></span>
          <span class="tile__scrim"></span>
          {eyebrow(t["icon"], t["cat"])}
          <h3 class="tile__title">{t['title']}</h3>
          <time class="tile__date" datetime="{t['date']}">{t['date_label']}</time>
        </a>"""

    size = "tile--large" if t["size"] == "large" else "tile--small"
    title_cls = "tile__title tile__title--display" if t.get("display") else "tile__title"

    if t["kind"] == "solid":
        tone = {"soft": "tile--soft", "primary": "tile--primary", "sun": "tile--sun"}[t["tone"]]
        return f"""        <a class="tile {size} tile--solid {tone} reveal" href="article.html" style="{delay}">
          <div class="tile__top">
            {eyebrow(t["icon"], t["cat"])}
            <h3 class="{title_cls}">{t['title']}</h3>
          </div>
          <time class="tile__date" datetime="{t['date']}">{t['date_label']}</time>
        </a>"""

    dark = " tile--dark" if t.get("dark") else ""
    h = 326 if t["size"] == "large" else (230 if t.get("dark") else 210)
    return f"""        <a class="tile {size}{dark} reveal" href="article.html" style="{delay}">
          <figure class="tile__figure"><img class="tile__img" src="{IMG}{t['slug']}.webp" alt="{t['alt']}" width="580" height="{h}" loading="lazy"></figure>
          <div class="tile__body">
            <div class="tile__top">
              {eyebrow(t["icon"], t["cat"])}
              <h3 class="{title_cls}">{t['title']}</h3>
            </div>
            <time class="tile__date" datetime="{t['date']}">{t['date_label']}</time>
          </div>
        </a>"""


def build_index():
    chips = "\n".join(
        '          <button class="chip{cls}" type="button" aria-pressed="{p}">{c}</button>'.format(
            cls=" is-active" if n == 0 else "",
            p="true" if n == 0 else "false",
            c=c,
        )
        for n, c in enumerate(CHIPS)
    )
    tiles = "\n".join(render_tile(t, i) for i, t in enumerate(TILES))

    return (head("Useful tips from ProntoTest · Guide",
                 "Real road situations in Spain explained step by step: what to look for, "
                 "what to do and why, with official sources.")
            + f"""  <div class="page">
{GLOW}
{header()}
    <main class="body container">
      <div class="page-head">
        <h1 class="page-head__title">Useful tips from ProntoTest</h1>
        <p class="page-head__desc">Real road situations in Spain explained step by step: what to look for, what to do and why, with official sources.</p>
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

      <div class="bento">
{tiles}
      </div>

      <nav class="pager" aria-label="Pagination">
        <a class="pager__item is-disabled" href="#" aria-disabled="true">{icon("arrow-left")}<span>Previous</span></a>
        <a class="pager__item is-active" href="#" aria-current="page">1</a>
        <a class="pager__item" href="#">2</a>
        <a class="pager__item" href="#">3</a>
        <a class="pager__item" href="#"><span>Next</span>{icon("arrow-right")}</a>
      </nav>
    </main>
  </div>

{footer()}
{menu()}
{TAIL}""")


# ---------------------------------------------------------------- article ---

BULLETS = [
    "At dusk a car on the shoulder is spotted late: the traffic behind will be level with you within seconds.",
    "Someone will only swerve round you at the last moment and may clip you.",
    "Nobody has to stop and help: count on the breakdown service and 112.",
    "If someone does stop beside you “to help”, they'll end up in the middle of the shoulder and become a hazard themselves.",
]

STEPS = [
    "While the car is still rolling, get it out of the running lanes: take the exit if there is one; if not, stop on the right-hand shoulder as far to the right as you can.",
    "Switch on the hazard lights and sidelights, and put the vest on while you're still inside.",
    "Switch the beacon on and put it on the roof through the window without getting out: that's why it belongs in the glovebox, not the boot. The beacon must be a connected one (sending data to DGT 3.0): since 1 January 2026 only these are valid, and warning triangles are no longer used.",
    "Everyone gets out through the right-hand doors, the driver too, and goes straight behind the barrier.",
    "If there's no safe place behind the barrier, stay in the car with your seatbelts on and call 112.",
]

MORE = [
    ("book-cover", "Traffic rules",
     "Stepped out of the car “for a minute”? For the law, that’s already parking",
     "parada-o-estacionamiento-bajarse-del-coche",
     "A driver stepping out of a car parked at the kerb"),
    ("warning-diamond", "Traffic signs",
     "A STOP sign and you can't see the road: why you stop twice",
     "stop-sin-visibilidad-parar-dos-veces",
     "A junction with a STOP sign and blocked visibility"),
    ("energy", "Lights",
     "Fog lights in a downpour: when the rear one helps and when it dazzles",
     "luces-antiniebla-cuando-encender",
     "Cars in heavy rain with rear fog lights on"),
]


def build_article():
    bullets = "\n".join(
        f'            <li>{icon("warning")}<span>{b}</span></li>' for b in BULLETS)
    steps = "\n".join(
        f'            <li><span class="steps__num">{n}</span><span>{s}</span></li>'
        for n, s in enumerate(STEPS, 1))
    more = "\n".join(f"""        <a class="mini reveal" href="#" style="--delay:{i * 60}ms">
          {eyebrow(ic, cat)}
          <h3 class="mini__title">{title}</h3>
          <figure class="mini__figure"><img src="{IMG}{slug}.webp" alt="{alt}" width="313" height="150" loading="lazy"></figure>
        </a>""" for i, (ic, cat, title, slug, alt) in enumerate(MORE))

    return (head("Broken down on the motorway: beacon on the roof, everyone behind the barrier · ProntoTest",
                 "Put the beacon on the roof from inside the car. Then everyone gets behind the "
                 "barrier instead of standing on the shoulder.")
            + f"""  <div class="page">
{GLOW}
{header()}
    <main class="article-body container">
      <article class="panel">
        <header class="article-head measure">
          {eyebrow("warning", "Guide · Road safety &amp; accidents")}
          <p class="article-dates"><time datetime="2026-09-06">6 September 2026</time> · Updated <time datetime="2026-11-04">4 November 2026</time></p>
          <h1 class="article-title">Broken down on the motorway: beacon on the roof, everyone behind the barrier</h1>
          <p class="article-lede">Put the beacon on the roof from inside the car. Then everyone gets behind the barrier instead of standing on the shoulder.</p>
          <div class="head-row">
            <div class="author">
              <span class="author__avatar">{icon("energy")}</span>
              <span class="author__name">By ProntoTest</span>
            </div>
            <div class="head-actions">
              <button class="btn-secondary" type="button">{icon("share")}<span>Share</span></button>
              <button class="btn-secondary" type="button" data-copy-link>{icon("link")}<span>Copy link</span></button>
            </div>
          </div>
        </header>

        <figure class="article-hero">
          <img src="{IMG}averia-en-autovia-baliza-v16.webp" alt="Top view: an orange car on the right-hand shoulder of an autovía with a V-16 beacon on its roof" width="980" height="551">
        </figure>

        <div class="article-column measure">
          <p class="caption">Top view: an orange car pulls onto the right-hand shoulder of an autovía, a V-16 beacon lights up on its roof and the people move behind the barrier</p>

          <div class="text-block">
            <p>You're driving along an autovía (a Spanish dual carriageway) at dusk. The car loses power, the next exit is a long way off, and you coast onto the right-hand shoulder. Behind you the traffic is doing 120 km/h. You have two passengers with you, and the V-16 beacon and the hi-vis vest are in the glovebox.</p>

            <h2>What to notice</h2>
            <ul class="bullets">
{bullets}
            </ul>

            <h2>What to do</h2>
            <ol class="steps">
{steps}
            </ol>
          </div>
        </div>

        <figure class="article-anim">
          <img src="{IMG}averia-anim.png" alt="Animation frames: hard shoulder, beacon on the roof, everyone behind the barrier" width="980" height="551" loading="lazy">
        </figure>

        <div class="article-end measure">
          <p class="caption">Animation · 14 s. Step by step: shoulder, beacon on the roof, everyone behind the barrier.</p>
        </div>
      </article>

      <div class="promo">
        <div class="promo__top">
          {eyebrow("checkmark-in-circle", "Free DGT test")}
          <p class="promo__title">Read the tips, then check yourself in the free category B mock exam</p>
        </div>
        <a class="btn-pill" href="#">Practise with free tests</a>
      </div>

      <section class="more">
        <div class="more__head">
          <h2 class="more__title">More tips</h2>
          <a class="more__link" href="index.html">All tips{icon("chevron-right")}</a>
        </div>
        <div class="more__row">
{more}
        </div>
      </section>
    </main>
  </div>

{footer()}
{menu()}
{TAIL}""")


if __name__ == "__main__":
    (ROOT / "index.html").write_text(build_index(), encoding="utf-8")
    (ROOT / "article.html").write_text(build_article(), encoding="utf-8")
    print("built", os.path.getsize(ROOT / "index.html"), os.path.getsize(ROOT / "article.html"))

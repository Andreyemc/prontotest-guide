# -*- coding: utf-8 -*-
import asyncio, sys
sys.path.insert(0, "/home/claude/src")
from audit import run

F = "/Pronto Web · Guide listing · B (bento)"
A = "/Pronto Web · Guide article · B (bento)"
M = "/Pronto Mobile · Guide listing · B (bento)"
MENU = "/Pronto Mobile · Guide listing · Menu open"
FT = "/PW Footer · B"

LISTING = [
 (F+"/Header B", ".header .header__inner", {"gap"}),
 (F+"/Header B/Logo", ".header .logo", None),
 (F+"/Header B/Header Right", ".header .header__right", {"gap"}),
 (F+"/Header B/Header Right/Header Nav", ".header .nav", {"gap"}),
 (F+"/Header B/Header Right/Header Nav/Nav Guide", ".header .nav__link.is-active", None),
 (F+"/Header B/Header Right/Header Nav/Nav Benefits", ".header .nav__link:not(.is-active)", None),
 (F+"/Header B/Header Right/Header Buttons", ".header .header__buttons", {"gap"}),
 (F+"/Header B/Header Right/Header Buttons/Language", ".header .btn-glass--icon", {"backgroundColor","borderRadius"}),
 (F+"/Header B/Header Right/Header Buttons/Get App", ".header .btn-glass:not(.btn-glass--icon)", {"backgroundColor","borderRadius","padding","gap"}),
 (F+"/Header B/Header Right/Header Buttons/Get App/Get App Label", ".header .btn-glass:not(.btn-glass--icon)", {"fontSize","fontWeight","letterSpacing","color","fontFamily"}),
 (F+"/Body", "main.body", {"gap"}),
 (F+"/Body/Page Head", ".page-head", {"gap"}),
 (F+"/Body/Page Head/Page Title", ".page-head__title", None),
 (F+"/Body/Page Head/Page Desc", ".page-head__desc", None),
 (F+"/Body/Filter Row", ".filters", {"borderRadius","padding","gap","backgroundColor"}),
 (F+"/Body/Filter Row/Topic Chips", ".chips", {"gap"}),
 (F+"/Body/Filter Row/Topic Chips/Chip All", ".chip.is-active", {"backgroundColor","borderRadius","padding"}),
 (F+"/Body/Filter Row/Topic Chips/Chip All/Chip Label", ".chip.is-active", {"fontSize","fontWeight","letterSpacing","color","fontFamily"}),
 (F+"/Body/Filter Row/Search", ".search", {"backgroundColor","borderRadius","padding","gap"}),
 (F+"/Body/Filter Row/Search/Search Placeholder", ".search input", {"fontSize","fontWeight","letterSpacing","fontFamily"}),
 (F+"/Body/Bento Grid", ".bento", {"gap"}),
 (F+"/Body/Bento Grid/Row 1", ".bento", {"gap"}),
 (F+"/Body/Bento Grid/Row 1/Tile · glorieta", ".bento > .tile--large", {"backgroundColor","borderRadius"}),
 (F+"/Body/Bento Grid/Row 1/Tile · glorieta/Tile Body", ".bento > .tile--large .tile__body", {"padding"}),
 (F+"/Body/Bento Grid/Row 1/Tile · glorieta/Tile Body/Tile Top", ".bento > .tile--large .tile__top", {"gap"}),
 (F+"/Body/Bento Grid/Row 1/Tile · glorieta/Tile Body/Tile Top/Eyebrow", ".bento > .tile--large .eyebrow", {"gap"}),
 (F+"/Body/Bento Grid/Row 1/Tile · glorieta/Tile Body/Tile Top/Eyebrow/Eyebrow Tile", ".bento > .tile--large .eyebrow__tile", {"backgroundColor","borderRadius"}),
 (F+"/Body/Bento Grid/Row 1/Tile · glorieta/Tile Body/Tile Top/Eyebrow/Category", ".bento > .tile--large .eyebrow__label", {"fontSize","fontWeight","letterSpacing","color","fontFamily"}),
 (F+"/Body/Bento Grid/Row 1/Tile · glorieta/Tile Body/Tile Top/Tile Title", ".bento > .tile--large:not(.tile--display) .tile__title", None),
 (F+"/Body/Bento Grid/Row 1/Tile · glorieta/Tile Body/Date", ".bento > .tile--large .tile__date", None),
 (F+"/Body/Bento Grid/Row 1/Tile · adelantar/Tile Body/Tile Top/Tile Title", ".bento > .tile--large.tile--display .tile__title", None),
 (F+"/Body/Bento Grid/Row 2/Tile · parada", ".bento > .tile--soft", {"backgroundColor","borderRadius"}),
 (F+"/Body/Bento Grid/Row 2/Tile · parada/Tile Top/Tile Title", ".bento > .tile--soft .tile__title", None),
 (F+"/Body/Bento Grid/Row 2/Tile · parada/Date", ".bento > .tile--soft .tile__date", None),
 (F+"/Body/Bento Grid/Row 2/Tile · stop", ".bento > .tile--ink", {"backgroundColor","borderRadius"}),
 (F+"/Body/Bento Grid/Row 2/Tile · stop/Tile Body/Tile Top/Eyebrow/Eyebrow Tile", ".bento > .tile--ink .eyebrow__tile", {"backgroundColor"}),
 (F+"/Body/Bento Grid/Row 2/Tile · stop/Tile Body/Tile Top/Eyebrow/Category", ".bento > .tile--ink .eyebrow__label", {"color","fontSize","fontWeight"}),
 (F+"/Body/Bento Grid/Row 2/Tile · stop/Tile Body/Date", ".bento > .tile--ink .tile__date", {"color","fontSize","fontWeight"}),
 (F+"/Body/Bento Grid/Row 3/Tile · averia", ".tile--feature", {"borderRadius"}),
 (F+"/Body/Bento Grid/Row 3/Tile · averia/Tile Title", ".tile--feature .tile__title", None),
 (F+"/Body/Bento Grid/Row 3/Tile · averia/Date", ".tile--feature .tile__date", None),
 (F+"/Body/Bento Grid/Row 3/Tile · averia/Eyebrow/Category", ".tile--feature .eyebrow__label", {"color","fontSize","fontWeight","letterSpacing"}),
 (F+"/Body/Bento Grid/Row 4/Tile · semaforo", ".bento > .tile--primary", {"backgroundColor","borderRadius"}),
 (F+"/Body/Bento Grid/Row 4/Tile · semaforo/Tile Top/Tile Title", ".bento > .tile--primary .tile__title", None),
 (F+"/Body/Bento Grid/Row 4/Tile · semaforo/Date", ".bento > .tile--primary .tile__date", {"color","fontSize","fontWeight"}),
 (F+"/Body/Bento Grid/Row 4/Tile · margen", ".bento > .tile--sun", {"backgroundColor"}),
 (F+"/Body/Bento Grid/Row 5/Tile · Free test", ".tile--cta", {"backgroundColor","borderRadius"}),
 (F+"/Body/Bento Grid/Row 5/Tile · Free test/CTA Top", ".tile--cta .tile__top", {"gap"}),
 (F+"/Body/Bento Grid/Row 5/Tile · Free test/CTA Top/Tile Title", ".tile--cta .tile__title", None),
 (F+"/Body/Bento Grid/Row 5/Tile · Free test/CTA Top/Tile Eyebrow/Eyebrow Label", ".tile--cta .eyebrow__label", None),
 (F+"/Body/Bento Grid/Row 5/Tile · Free test/Practise Button", ".tile--cta .btn-pill", {"backgroundColor","borderRadius","padding"}),
 (F+"/Body/Bento Grid/Row 5/Tile · Free test/Practise Button/Label", ".tile--cta .btn-pill", {"fontSize","fontWeight","color"}),
 (F+"/Body/Pager", ".pager", {"gap"}),
 (F+"/Body/Pager/Page 1", ".pager__item.is-active", {"backgroundColor","borderRadius","padding","gap"}),
 (F+"/Body/Pager/Page 1/Page Label", ".pager__item.is-active", {"fontSize","fontWeight","color"}),
 (F+"/Body/Pager/Page 2", ".pager__item:not(.is-active):not([data-page='prev']):not([data-page='next'])", {"backgroundColor"}),
]

FOOTER = [
 (FT, ".footer", {"backgroundColor"}),
 (FT+"/Footer Top/Footer Links", ".footer__links", {"gap"}),
 (FT+"/Footer Top/Footer Links/Link Col PRODUCT", ".footer__col", {"gap"}),
 (FT+"/Footer Top/Footer Links/Link Col PRODUCT/Col Title", ".footer__col-title", None),
 (FT+"/Footer Top/Footer Links/Link Col PRODUCT/Links", ".footer__col ul", {"gap"}),
 (FT+"/Footer Top/Footer Links/Link Col PRODUCT/Links/Link", ".footer__col .footer__link", None),
 (FT+"/Footer Top/Footer Right", ".footer__right", {"gap"}),
 (FT+"/Footer Top/Footer Right/Language", ".footer .lang", {"backgroundColor","borderRadius","padding","gap"}),
 (FT+"/Footer Top/Footer Right/Language/Lang Label", ".footer .lang", {"fontSize","fontWeight","color"}),
 (FT+"/Footer Top/Footer Right/Store Badges", ".footer .badges", {"gap"}),
 (FT+"/Wordmark", ".wordmark", {"padding"}),
 (FT+"/Legal", ".footer__legal", {"gap"}),
 (FT+"/Legal/Legal 1", ".footer__copy", None),
 (FT+"/Legal/Legal 2", ".footer__disclaimer", None),
]

ARTICLE = [
 (A+"/Body", "main.article-body", {"gap"}),
 (A+"/Body/Article Panel", ".panel", {"backgroundColor","borderRadius"}),
 (A+"/Body/Article Panel/Page Head", ".article-head", {"padding","gap"}),
 (A+"/Body/Article Panel/Page Head/Eyebrow/Category", ".article-head .eyebrow__label", None),
 (A+"/Body/Article Panel/Page Head/Article Dates", ".article-dates", None),
 (A+"/Body/Article Panel/Page Head/H1", ".article-title", None),
 (A+"/Body/Article Panel/Page Head/Lede", ".article-lede", None),
 (A+"/Body/Article Panel/Page Head/Head Row/Author Row", ".author", {"gap"}),
 (A+"/Body/Article Panel/Page Head/Head Row/Author Row/Author Avatar", ".author__avatar", {"backgroundColor","borderRadius"}),
 (A+"/Body/Article Panel/Page Head/Head Row/Author Row/Author Text/Author Name", ".author__name", {"fontSize","fontWeight","color"}),
 (A+"/Body/Article Panel/Page Head/Head Row/Head Actions", ".head-actions", {"gap"}),
 (A+"/Body/Article Panel/Page Head/Head Row/Head Actions/Secondary Button", ".btn-secondary", {"backgroundColor","borderRadius","padding","gap"}),
 (A+"/Body/Article Panel/Body Column", ".article-column", {"padding","gap"}),
 (A+"/Body/Article Panel/Body Column/Hero Caption", ".caption", None),
 (A+"/Body/Article Panel/Body Column/Text Block", ".text-block", {"gap"}),
 (A+"/Body/Article Panel/Body Column/Text Block/Paragraph", ".text-block p", None),
 (A+"/Body/Article Panel/Body Column/Text Block/H2", ".text-block h2", None),
 (A+"/Body/Article Panel/Body Column/Text Block/Bullet List", ".bullets", {"gap"}),
 (A+"/Body/Article Panel/Body Column/Text Block/Bullet List/Bullet", ".bullets li", {"gap"}),
 (A+"/Body/Article Panel/Body Column/Text Block/Bullet List/Bullet/Bullet Text", ".bullets li span", None),
 (A+"/Body/Article Panel/Body Column/Text Block/Steps", ".steps", {"gap"}),
 (A+"/Body/Article Panel/Body Column/Text Block/Steps/Step", ".steps li", {"gap"}),
 (A+"/Body/Article Panel/Body Column/Text Block/Steps/Step/Step Number", ".steps__num", {"backgroundColor","borderRadius"}),
 (A+"/Body/Article Panel/Body Column/Text Block/Steps/Step/Step Number/Step Num", ".steps__num", {"fontSize","fontWeight","color"}),
 (A+"/Body/Article Panel/Body Column/Text Block/Steps/Step/Step Text", ".steps li > span:last-child", None),
 (A+"/Body/Article Panel/End Column", ".article-end", {"padding"}),
 (A+"/Body/Tile · Free test", ".promo", {"backgroundColor","borderRadius","padding","gap"}),
 (A+"/Body/Tile · Free test/CTA Top/Tile Title", ".promo__title", None),
 (A+"/Body/More Tips", ".more", {"gap"}),
 (A+"/Body/More Tips/More Heading/More Title", ".more__title", None),
 (A+"/Body/More Tips/More Heading/More Link/More Link Label", ".more__link", {"fontSize","fontWeight","color"}),
 (A+"/Body/More Tips/More Row", ".more__row", {"gap"}),
 (A+"/Body/More Tips/More Row/Tile · Traffic rules", ".mini", {"backgroundColor","borderRadius","padding","gap"}),
 (A+"/Body/More Tips/More Row/Tile · Traffic rules/Tile Title", ".mini__title", None),
 (A+"/Body/More Tips/More Row/Tile · Traffic rules/Tile Eyebrow/Eyebrow Label", ".mini .eyebrow__label", None),
]

MOBILE = [
 (M+"/Header M", ".header-m__inner", {"padding"}),
 (M+"/Header M/Logo", ".header-m .logo", None),
 (M+"/Header M/Header Icons", ".header-m__icons", {"gap"}),
 (M+"/Header M/Header Icons/Search", ".header-m .icon-round", {"backgroundColor","borderRadius"}),
 (M+"/Body", "main.body", {"gap"}),
 (M+"/Body/Page Head", ".page-head", {"gap"}),
 (M+"/Body/Page Head/Page Title", ".page-head__title", None),
 (M+"/Body/Page Head/Page Desc", ".page-head__desc", None),
 (M+"/Body/Topic Chips", ".chips", {"gap"}),
 (M+"/Body/Topic Chips/Chip All", ".chip.is-active", {"backgroundColor","borderRadius","padding"}),
 (M+"/Body/Topic Chips/Chip All/Chip Label", ".chip.is-active", {"fontSize","fontWeight","color"}),
 (M+"/Body/Topic Chips/Chip Traffic rules", ".chip:not(.is-active)", {"backgroundColor"}),
 (M+"/Body/Tile Stack", ".bento", {"gap"}),
 (M+"/Body/Tile Stack/Tile · glorieta", ".bento > .tile--large", {"backgroundColor","borderRadius"}),
 (M+"/Body/Tile Stack/Tile · glorieta/Tile Body", ".bento > .tile--large .tile__body", {"padding","gap"}),
 (M+"/Body/Tile Stack/Tile · glorieta/Tile Body/Tile Top/Eyebrow/Eyebrow Tile", ".eyebrow__tile", {"backgroundColor","borderRadius"}),
 (M+"/Body/Tile Stack/Tile · glorieta/Tile Body/Tile Top/Eyebrow/Category", ".bento > .tile--large .eyebrow__label", None),
 (M+"/Body/Tile Stack/Tile · glorieta/Tile Body/Tile Top/Tile Title", ".bento > .tile--large:not(.tile--display) .tile__title", None),
 (M+"/Body/Tile Stack/Tile · glorieta/Tile Body/Date", ".bento > .tile--large .tile__date", None),
 (M+"/Body/Pager", ".pager", {"gap"}),
]

MENU_PAIRS = [
 (MENU+"/Menu Overlay", "#menu", {"backgroundColor"}),
 (MENU+"/Menu Overlay/Menu Nav", ".menu__nav", {"padding"}),
 (MENU+"/Menu Overlay/Menu Nav/Menu Item Guide", ".menu__item.is-active", None),
 (MENU+"/Menu Overlay/Menu Nav/Menu Item Guide/Menu Label", ".menu__item.is-active", {"fontSize","fontWeight","letterSpacing","color"}),
 (MENU+"/Menu Overlay/Menu Nav/Menu Item Benefits/Menu Label", ".menu__item:not(.is-active)", {"fontSize","fontWeight","letterSpacing","color"}),
 (MENU+"/Menu Overlay/Menu Footer", ".menu__footer", {"padding","gap"}),
 (MENU+"/Menu Overlay/Menu Footer/Get App Button", ".menu__cta", {"backgroundColor","borderRadius"}),
 (MENU+"/Menu Overlay/Menu Footer/Get App Button/Label", ".menu__cta", {"fontSize","fontWeight","color"}),
 (MENU+"/Menu Overlay/Menu Footer/Menu Utility", ".menu__utility", None),
 (MENU+"/Menu Overlay/Menu Footer/Menu Utility/Store Badges", ".menu__utility .badges", {"gap"}),
]

async def main():
    bad = 0
    bad += await run("index.html", LISTING, 1280, "Листинг · десктоп 1280")
    bad += await run("index.html", FOOTER, 1280, "Футер · десктоп")
    bad += await run("guia/averia-en-autovia-baliza-v16.html", ARTICLE, 1280, "Статья · десктоп 1280")
    bad += await run("index.html", MOBILE, 390, "Листинг · мобильный 390")
    bad += await run("index.html", MENU_PAIRS, 390, "Бургер-меню · 390", setup="[data-menu-toggle]")
    print(f"\nИТОГО расхождений: {bad}")

asyncio.run(main())

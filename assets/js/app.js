/* ProntoTest · Guide — поведение и микроанимации (раздел 10 спецификации макета). */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Sticky header: фон и высота после 24px скролла ---- */

  var headers = Array.prototype.slice.call(document.querySelectorAll("[data-header]"));

  var stuck = false;

  function onScroll() {
    /* гистерезис: включаем после 24px, выключаем только ниже 16px,
       иначе на границе шапка моргает при инерционном скролле */
    var y = window.scrollY;
    var next = stuck ? y > 16 : y > 24;
    if (next === stuck) return;
    stuck = next;
    headers.forEach(function (h) { h.classList.toggle("is-stuck", stuck); });
  }

  if (headers.length) {
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Появление элементов: IntersectionObserver, 15%, один раз ---- */

  var io = null;

  function reveal(nodes) {
    if (reduced || !("IntersectionObserver" in window)) {
      nodes.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    if (!io) {
      io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        });
      }, { threshold: 0.15 });
    }
    nodes.forEach(function (el) { io.observe(el); });
  }

  reveal(Array.prototype.slice.call(document.querySelectorAll(".reveal")));

  /* ---- Хаб: фильтр по темам и пагинация ----
     Раскладка bento из макета: ряд из двух больших, ряд из трёх малых, фича во
     всю ширину, ещё ряд из трёх малых. Классы раздаются по позиции, поэтому
     сетка остаётся целой при любом числе карточек. */

  var bento = document.querySelector("[data-bento]");

  if (bento) {
    var ROWS = [
      [["large", "img", "", false], ["large", "img", "", true]],
      [["small", "solid", "soft", false], ["small", "img", "ink", false],
       ["small", "img", "", false]],
      [["full", "feature", "", true]],
      [["small", "solid", "primary", true], ["small", "img", "", false],
       ["small", "solid", "sun", false]]
    ];
    var SPAN_FOR_COUNT = { 1: "tile--span6", 2: "tile--span3" };

    var cards = Array.prototype.slice.call(bento.querySelectorAll("[data-card]"));
    var perPage = parseInt(bento.getAttribute("data-per-page"), 10) || 9;
    var pager = document.querySelector("[data-pager]");
    var chipGroup = document.querySelector(".chips");
    var empty = null;
    var state = { category: "all", page: 1 };

    function setTile(el, spec, spanOverride) {
      el.className = "tile tile--" + spec[0] + " tile--" + spec[1] +
        (spec[2] ? " tile--" + spec[2] : "") +
        (spec[3] ? " tile--display" : "") +
        (spanOverride ? " " + spanOverride : "") +
        " reveal";
    }

    function matching() {
      return cards.filter(function (c) {
        return state.category === "all" ||
          c.getAttribute("data-category") === state.category;
      });
    }

    function renderPager(totalPages) {
      if (!pager) return;
      pager.hidden = totalPages <= 1;
      var prev = pager.querySelector('[data-page="prev"]');
      var next = pager.querySelector('[data-page="next"]');

      Array.prototype.slice.call(pager.querySelectorAll("[data-page]")).forEach(function (el) {
        var v = el.getAttribute("data-page");
        if (v === "prev" || v === "next") return;
        el.remove();
      });

      for (var n = 1; n <= totalPages; n++) {
        var a = document.createElement("a");
        a.className = "pager__item" + (n === state.page ? " is-active" : "");
        a.href = "#";
        a.setAttribute("data-page", String(n));
        a.setAttribute("aria-label", "Page " + n);
        if (n === state.page) a.setAttribute("aria-current", "page");
        a.textContent = String(n);
        pager.insertBefore(a, next);
      }

      if (prev) prev.setAttribute("aria-disabled", state.page === 1 ? "true" : "false");
      if (next) {
        next.setAttribute("aria-disabled",
          state.page >= totalPages ? "true" : "false");
      }
    }

    function render() {
      var visible = matching();
      var totalPages = Math.max(1, Math.ceil(visible.length / perPage));
      if (state.page > totalPages) state.page = totalPages;

      var slice = visible.slice((state.page - 1) * perPage, state.page * perPage);

      cards.forEach(function (c) { c.hidden = true; });

      var i = 0;
      var row = 0;
      var fresh = [];
      while (i < slice.length) {
        var spec = ROWS[row % ROWS.length];
        var take = Math.min(spec.length, slice.length - i);
        var override = take < spec.length ? SPAN_FOR_COUNT[take] : "";
        for (var k = 0; k < take; k++) {
          var el = slice[i + k];
          setTile(el, spec[k], override);
          el.style.setProperty("--delay", Math.min((i + k) * 60, 300) + "ms");
          el.hidden = false;
          fresh.push(el);
        }
        i += take;
        row++;
      }

      if (empty) { empty.remove(); empty = null; }
      if (!slice.length) {
        empty = document.createElement("p");
        empty.className = "bento__empty";
        empty.textContent = "No tips in this topic yet.";
        bento.appendChild(empty);
      }

      reveal(fresh);
      renderPager(totalPages);
    }

    if (chipGroup) {
      chipGroup.addEventListener("click", function (ev) {
        var chip = ev.target.closest(".chip");
        if (!chip) return;
        chipGroup.querySelectorAll(".chip").forEach(function (c) {
          var on = c === chip;
          c.classList.toggle("is-active", on);
          c.setAttribute("aria-pressed", on ? "true" : "false");
        });
        state.category = chip.getAttribute("data-chip") || "all";
        state.page = 1;
        render();
      });
    }

    if (pager) {
      pager.addEventListener("click", function (ev) {
        var item = ev.target.closest("[data-page]");
        if (!item) return;
        ev.preventDefault();
        if (item.getAttribute("aria-disabled") === "true") return;
        var v = item.getAttribute("data-page");
        var totalPages = Math.max(1, Math.ceil(matching().length / perPage));
        if (v === "prev") state.page = Math.max(1, state.page - 1);
        else if (v === "next") state.page = Math.min(totalPages, state.page + 1);
        else state.page = parseInt(v, 10);
        render();
        bento.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
      });
    }

    render();
  }

  /* ---- Скелетон первого экрана (раздел 12) ----
     Показываем, только если первый экран не готов за 120 мс; держим не меньше
     300 мс, чтобы не мигал; прячем за 150 мс и запускаем каскад появления. */

  var skeleton = document.querySelector("[data-skeleton]");

  if (skeleton) {
    var scope = skeleton.parentElement;
    var SHOW_AFTER = 120, MIN_SHOW = 300, CAP = 4000;
    var shownAt = 0;
    var finished = false;

    var watched = Array.prototype.slice.call(
      scope.querySelectorAll(".tile:not([hidden]) img, .article-hero img"));

    function pending() {
      return watched.some(function (img) {
        return img.offsetParent !== null && !(img.complete && img.naturalWidth);
      });
    }

    function show() {
      if (finished || !pending()) return;
      shownAt = Date.now();
      skeleton.hidden = false;
      scope.classList.add("is-preloading");
    }

    function hide() {
      if (finished) return;
      finished = true;
      if (!shownAt) { skeleton.remove(); return; }
      var wait = Math.max(0, MIN_SHOW - (Date.now() - shownAt));
      window.setTimeout(function () {
        skeleton.classList.add("is-out");
        scope.classList.remove("is-preloading");
        window.setTimeout(function () { skeleton.remove(); }, 150);
        replay();
      }, wait);
    }

    function replay() {
      if (reduced) return;
      var items = Array.prototype.slice.call(
        scope.querySelectorAll(".tile:not([hidden]).reveal"));
      items.forEach(function (el) { el.classList.remove("is-in"); });
      void scope.offsetWidth;
      items.forEach(function (el) { el.classList.add("is-in"); });
    }

    window.setTimeout(show, SHOW_AFTER);
    window.setTimeout(hide, CAP);

    if (!watched.length || !pending()) hide();
    else {
      var left = watched.length;
      watched.forEach(function (img) {
        var done = function () { if (--left <= 0) hide(); };
        if (img.complete && img.naturalWidth) done();
        else {
          img.addEventListener("load", done, { once: true });
          img.addEventListener("error", done, { once: true });
        }
      });
    }
  }

  /* ---- Бургер-меню ---- */

  var menu = document.getElementById("menu");
  var toggleBtn = document.querySelector("[data-menu-toggle]");

  function openMenu() {
    if (!menu) return;
    menu.hidden = false;
    requestAnimationFrame(function () { menu.classList.add("is-open"); });
    document.body.classList.add("is-locked", "is-menu-open");
    if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "true");
  }

  function closeMenu() {
    if (!menu || !menu.classList.contains("is-open")) return;
    menu.classList.remove("is-open");
    document.body.classList.remove("is-locked", "is-menu-open");
    if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "false");
    window.setTimeout(function () {
      if (!menu.classList.contains("is-open")) menu.hidden = true;
    }, reduced ? 150 : 240);
  }

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
      if (menu && menu.classList.contains("is-open")) closeMenu();
      else openMenu();
    });
  }

  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") closeMenu();
  });

  if (menu) {
    menu.addEventListener("click", function (ev) {
      if (ev.target.closest(".menu__item")) closeMenu();
    });
  }

  /* ---- Анимированные иконки useAnimations ----
     Lottie-плеер грузится лениво и только если движение не отключено;
     до этого и при prefers-reduced-motion работают статичные SVG. */

  var UA_BASE = "https://useanimations.com/icons/";
  var UA_PLAYER = "https://cdn.jsdelivr.net/npm/lottie-web@5.13.0/build/player/lottie_light.min.js";

  var UA = {
    "globe": { mode: "hover" },
    "share": { mode: "hover" },
    "copy": { mode: "click" },
    "arrow-left": { mode: "hover" },
    "arrow-right": { mode: "hover" },
    "menu-v4": { mode: "toggle", speed: 2.9 }
  };

  function loadPlayer() {
    if (window.__uaPlayer) return window.__uaPlayer;
    window.__uaPlayer = new Promise(function (resolve, reject) {
      var sc = document.createElement("script");
      sc.src = UA_PLAYER;
      sc.async = true;
      sc.onload = function () { resolve(window.lottie); };
      sc.onerror = reject;
      document.head.appendChild(sc);
    });
    return window.__uaPlayer;
  }

  function mountIcon(host, lottie) {
    var id = host.getAttribute("data-ua");
    var cfg = UA[id];
    if (!cfg) return;

    var box = document.createElement("span");
    box.className = "ua";
    box.setAttribute("aria-hidden", "true");
    var ref = host.querySelector(".icon, .burger");
    host.insertBefore(box, ref || host.firstChild);

    var anim = lottie.loadAnimation({
      container: box,
      renderer: "svg",
      loop: false,
      autoplay: false,
      path: UA_BASE + id + ".json"
    });

    if (cfg.speed) anim.setSpeed(cfg.speed);

    anim.addEventListener("DOMLoaded", function () {
      host.classList.add("has-ua");
      anim.goToAndStop(0, true);
    });

    if (cfg.mode === "hover") {
      host.addEventListener("mouseenter", function () {
        if (!anim.isPaused) return;
        anim.goToAndPlay(0, true);
      });
      host.addEventListener("focus", function () { anim.goToAndPlay(0, true); });
    } else if (cfg.mode === "click") {
      host.addEventListener("click", function () { anim.goToAndPlay(0, true); });
    } else if (cfg.mode === "toggle") {
      var on = false;
      host.addEventListener("click", function () {
        on = !on;
        anim.setDirection(on ? 1 : -1);
        anim.play();
      });
    }
  }

  function upgradeIcons() {
    if (reduced) return;
    var hosts = Array.prototype.slice.call(document.querySelectorAll("[data-ua]"));
    if (!hosts.length) return;
    loadPlayer().then(function (lottie) {
      if (!lottie) return;
      hosts.forEach(function (h) { mountIcon(h, lottie); });
    }).catch(function () { /* остаются статичные иконки */ });
  }

  if ("requestIdleCallback" in window) requestIdleCallback(upgradeIcons, { timeout: 2500 });
  else window.setTimeout(upgradeIcons, 1200);

  /* ---- Share и Copy link ----
     В шаринг уходит канонический URL статьи, а не адрес этого стенда. */

  function canonicalUrl() {
    var link = document.querySelector('link[rel="canonical"]');
    return link ? link.href : window.location.href;
  }

  function flash(btn, text) {
    var label = btn.querySelector("span");
    if (!label) return;
    var prev = label.textContent;
    label.textContent = text;
    window.setTimeout(function () { label.textContent = prev; }, 1600);
  }

  document.querySelectorAll("[data-share]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var data = { title: document.title, url: canonicalUrl() };
      if (navigator.share) navigator.share(data).catch(function () {});
      else copy(btn);
    });
  });

  function copy(btn) {
    var url = canonicalUrl();
    if (!navigator.clipboard) { window.prompt("Tip link", url); return; }
    navigator.clipboard.writeText(url).then(
      function () { flash(btn, "Link copied"); },
      function () { window.prompt("Couldn't copy automatically. Copy the link:", url); }
    );
  }

  document.querySelectorAll("[data-copy-link]").forEach(function (btn) {
    btn.addEventListener("click", function () { copy(btn); });
  });
})();

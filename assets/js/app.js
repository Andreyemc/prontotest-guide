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
      }, { threshold: 0.15, rootMargin: "0px 0px 12% 0px" });
    }
    nodes.forEach(function (el) { io.observe(el); });
  }

  reveal(Array.prototype.slice.call(document.querySelectorAll(".reveal")));

  /* После первой отрисовки каскад короче: длинная задержка уместна на монтаже
     первого экрана, но при прокрутке читается как подгрузка. */
  window.setTimeout(function () {
    document.querySelectorAll(".reveal:not(.is-in)").forEach(function (el) {
      el.classList.add("reveal--quick");
      var d = parseInt(el.style.getPropertyValue("--delay"), 10) || 0;
      el.style.setProperty("--delay-quick", Math.min(d, 120) + "ms");
    });
  }, 900);

  /* ---- Хаб: фильтр по темам и пагинация ----
     Раскладка bento из макета: ряд из двух больших, ряд из трёх малых, фича во
     всю ширину, ещё ряд из трёх малых. Классы раздаются по позиции, поэтому
     сетка остаётся целой при любом числе карточек. */

  var bento = document.querySelector("[data-bento]");

  if (bento) {
    var ROWS = [
      [["large", "img", ""], ["large", "img", ""]],
      [["small", "solid", "soft"], ["small", "img", "ink"], ["small", "img", ""]],
      [["full", "feature", ""]],
      [["small", "solid", "primary"], ["small", "img", ""], ["small", "solid", "sun"]],
      [["large", "img", ""]]
    ];
    var SPAN_FOR_COUNT = { 1: "tile--span6", 2: "tile--span3" };

    var cards = Array.prototype.slice.call(bento.querySelectorAll("[data-card]"));
    var perPage = parseInt(bento.getAttribute("data-per-page"), 10) || 9;
    var pager = document.querySelector("[data-pager]");
    var chipGroup = document.querySelector(".chips");
    var booted = false;
    window.setTimeout(function () { booted = true; }, 900);
    var state = { category: "all", page: 1 };

    function setTile(el, spec, spanOverride) {
      /* шрифт заголовка — свойство статьи, остальное задаёт позиция в сетке */
      var display = el.hasAttribute("data-display") || spec[1] === "feature";
      el.className = "tile tile--" + spec[0] + " tile--" + spec[1] +
        (spec[2] ? " tile--" + spec[2] : "") +
        (display ? " tile--display" : "") +
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
          var d = Math.min((i + k) * 60, 300);
          el.style.setProperty("--delay", d + "ms");
          if (booted) {
            el.classList.add("reveal--quick");
            el.style.setProperty("--delay-quick", Math.min(d, 120) + "ms");
          }
          el.hidden = false;
          fresh.push(el);
        }
        i += take;
        row++;
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

  /* ---- Плейсхолдеры картинок ----
     Вместо общей заглушки поверх страницы мерцает сам блок картинки: готовый
     текст, фильтры и карточки не прячутся из-за медленной иллюстрации. */

  Array.prototype.slice.call(
    document.querySelectorAll(".tile__media, .article-hero, .mini__figure")
  ).forEach(function (box) {
    var img = box.querySelector("img");
    if (!img) return;
    var done = function () { box.classList.add("is-ready"); };
    if (img.complete && img.naturalWidth) done();
    else {
      img.addEventListener("load", done, { once: true });
      img.addEventListener("error", done, { once: true });
    }
  });

  /* ---- Бургер-меню ---- */

  var menu = document.getElementById("menu");
  var toggleBtn = document.querySelector("[data-menu-toggle]");

  var pageMain = document.querySelector("main");
  var deskHeader = document.querySelector(".header");

  function setBackgroundInert(on) {
    [pageMain, deskHeader].forEach(function (el) {
      if (!el) return;
      if (on) {
        el.setAttribute("inert", "");
        el.setAttribute("aria-hidden", "true");
      } else {
        el.removeAttribute("inert");
        el.removeAttribute("aria-hidden");
      }
    });
  }

  function openMenu() {
    if (!menu) return;
    /* сперва то, что видно: переход стартует в этом же кадре */
    menu.classList.add("is-open");
    document.body.classList.add("is-menu-open");
    if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "true");

    /* остальное — следующим кадром, чтобы не задерживать первый */
    requestAnimationFrame(function () {
      document.body.classList.add("is-locked");
      setBackgroundInert(true);
      var first = menu.querySelector(".menu__item");
      if (first) first.focus({ preventScroll: true });
    });
  }

  function closeMenu() {
    if (!menu || !menu.classList.contains("is-open")) return;
    menu.classList.remove("is-open");
    document.body.classList.remove("is-locked", "is-menu-open");
    setBackgroundInert(false);
    if (toggleBtn) {
      toggleBtn.setAttribute("aria-expanded", "false");
      toggleBtn.focus({ preventScroll: true });
    }
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

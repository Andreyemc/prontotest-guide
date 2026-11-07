/* ProntoTest · Guide — поведение и микроанимации (раздел 10 спецификации). */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Sticky header: фон и высота после 24px скролла ---- */

  var headers = Array.prototype.slice.call(document.querySelectorAll("[data-header]"));

  function onScroll() {
    var stuck = window.scrollY > 24;
    headers.forEach(function (h) { h.classList.toggle("is-stuck", stuck); });
  }

  if (headers.length) {
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Появление плиток: IntersectionObserver, 15%, один раз ---- */

  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));

  if (!reveals.length) {
    /* nothing to do */
  } else if (reduced || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15 });

    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---- Чипы фильтра ---- */

  var chipGroup = document.querySelector(".chips");

  if (chipGroup) {
    chipGroup.addEventListener("click", function (e) {
      var chip = e.target.closest(".chip");
      if (!chip) return;
      chipGroup.querySelectorAll(".chip").forEach(function (c) {
        var on = c === chip;
        c.classList.toggle("is-active", on);
        c.setAttribute("aria-pressed", on ? "true" : "false");
      });
    });
  }

  /* ---- Бургер-меню ---- */

  var menu = document.getElementById("menu");
  var openBtn = document.querySelector("[data-menu-open]");
  var closeBtn = document.querySelector("[data-menu-close]");

  function openMenu() {
    if (!menu) return;
    menu.hidden = false;
    requestAnimationFrame(function () { menu.classList.add("is-open"); });
    document.body.classList.add("is-locked");
    if (openBtn) openBtn.setAttribute("aria-expanded", "true");
    if (closeBtn) closeBtn.focus();
  }

  function closeMenu() {
    if (!menu || !menu.classList.contains("is-open")) return;
    menu.classList.remove("is-open");
    document.body.classList.remove("is-locked");
    if (openBtn) {
      openBtn.setAttribute("aria-expanded", "false");
      openBtn.focus();
    }
    window.setTimeout(function () {
      if (!menu.classList.contains("is-open")) menu.hidden = true;
    }, reduced ? 150 : 240);
  }

  if (openBtn) openBtn.addEventListener("click", openMenu);
  if (closeBtn) closeBtn.addEventListener("click", closeMenu);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenu();
  });

  if (menu) {
    menu.addEventListener("click", function (e) {
      if (e.target.closest(".menu__item")) closeMenu();
    });
  }

  /* ---- Copy link ---- */

  var copyBtn = document.querySelector("[data-copy-link]");

  if (copyBtn && navigator.clipboard) {
    copyBtn.addEventListener("click", function () {
      navigator.clipboard.writeText(window.location.href).then(function () {
        var label = copyBtn.querySelector("span");
        if (!label) return;
        var prev = label.textContent;
        label.textContent = "Copied";
        window.setTimeout(function () { label.textContent = prev; }, 1600);
      }, function () {});
    });
  }
})();

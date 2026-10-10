(function () {
  "use strict";

  var start = function () { requestAnimationFrame(function () { setTimeout(init, 0); }); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
  function init() {
  var reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  var reduce = function () { return reduceMQ.matches; };
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  var toggle = document.getElementById("menu-toggle");
  var panel = document.getElementById("mobile-nav");
  if (toggle && panel) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.querySelector(".menu-toggle__label").textContent = open ? "Close" : "Menu";
      if (open) panel.removeAttribute("hidden"); else panel.setAttribute("hidden", "");
    };
    toggle.addEventListener("click", function () { setOpen(toggle.getAttribute("aria-expanded") !== "true"); });
    panel.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setOpen(false); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") { setOpen(false); toggle.focus(); }
    });
  }

  var revealEls = document.querySelectorAll(".reveal, [data-stitch], [data-sear]");
  if ("IntersectionObserver" in window && !reduce()) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  if ("IntersectionObserver" in window) {
    var loopIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.target.classList.toggle("is-offscreen", !en.isIntersecting); });
    });
    document.querySelectorAll(".x-none").forEach(function (el) { loopIO.observe(el); });
  }

  var para = document.querySelector("[data-parallax] img");
  if (para && !reduce()) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, 900);
        para.style.setProperty("--parallax", (y * 0.06).toFixed(1) + "px");
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  var tape = document.querySelector(".tape__strip");
  if (tape && !reduce()) {
    var tTick = false;
    var onTape = function () {
      if (tTick) return;
      tTick = true;
      requestAnimationFrame(function () {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
        tape.style.transform = "translateX(" + ((p - 1) * 100).toFixed(2) + "%)";
        tTick = false;
      });
    };
    window.addEventListener("scroll", onTape, { passive: true });
    onTape();
  }

  var vid = document.querySelector("[data-hero-video]");
  if (vid) {
    var vbtn = document.querySelector("[data-video-toggle]"), vlab = document.querySelector("[data-video-label]");
    var userPaused = false, vVisible = true, loaded = false;
    var vSync = function () {
      if (reduce()) { vid.pause(); vbtn.hidden = true; return; }
      if (!loaded) { var src = vid.querySelector("source"); src.src = src.dataset.src; vid.load(); loaded = true; }
      vbtn.hidden = false;
      if (vVisible && !userPaused) vid.play().catch(function () {}); else vid.pause();
      vbtn.setAttribute("aria-pressed", userPaused ? "true" : "false");
      vlab.textContent = userPaused ? "Play video" : "Pause video";
    };
    vbtn.addEventListener("click", function () { userPaused = !userPaused; vSync(); });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { vVisible = es[0].isIntersecting; vSync(); }, { threshold: 0.15 }).observe(vid);
    var mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (mq.addEventListener) mq.addEventListener("change", vSync);
    vSync();
  }

  if (finePointer && !reduce()) {
    document.querySelectorAll("[data-tilt]").forEach(function (card) {
      var raf = 0;
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(function () {
          card.classList.add("is-tilting");
          card.style.setProperty("--ry", (x * 7).toFixed(2) + "deg");
          card.style.setProperty("--rx", (-y * 7).toFixed(2) + "deg");
        });
      });
      card.addEventListener("pointerleave", function () {
        cancelAnimationFrame(raf);
        card.classList.remove("is-tilting");
        card.style.removeProperty("--rx");
        card.style.removeProperty("--ry");
      });
    });
  }

  var sig = document.querySelector("[data-sig]");
  if (sig && !reduce()) {
    sig.classList.add("is-scrub");
    sig.querySelectorAll("img[loading=lazy]").forEach(function (im) { im.loading = "eager"; });
    var q = function (sel) { return sig.querySelector(sel); };
    var chL = q(".sig__chain--l"), chR = q(".sig__chain--r"), pend = q(".sig__pendant"), fin = q(".sig__final"), copy = q(".sig__copy");
    var sparks = sig.querySelectorAll(".sig__spark"), steps = sig.querySelectorAll(".sig__steps li");
    var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
    var seg = function (p, a, b) { return clamp((p - a) / (b - a)); };
    var ease = function (t) { return 1 - Math.pow(1 - t, 3); };
    var ticking = false;
    var render = function () {
      ticking = false;
      var r = sig.getBoundingClientRect(), span = sig.offsetHeight - window.innerHeight;
      var p = span > 0 ? clamp(-r.top / span) : 1;
      var a = ease(seg(p, 0.05, 0.38)), c = ease(seg(p, 0.30, 0.62)), f = seg(p, 0.66, 0.84), t = ease(seg(p, 0.78, 0.95));
      chL.style.opacity = Math.min(1, a * 1.6) * (1 - f);
      chL.style.transform = "translate(" + (-60 * (1 - a)) + "vw," + (-30 * (1 - a)) + "vh) rotate(" + (-40 * (1 - a)) + "deg) scaleX(-1)";
      chR.style.opacity = Math.min(1, a * 1.6) * (1 - f);
      chR.style.transform = "translate(" + (60 * (1 - a)) + "vw," + (-30 * (1 - a)) + "vh) rotate(" + (40 * (1 - a)) + "deg)";
      pend.style.opacity = Math.min(1, c * 1.6) * (1 - f);
      pend.style.transform = "translateY(" + (70 * (1 - c)) + "vh) rotate(" + (180 * (1 - c)) + "deg) scale(" + (0.6 + 0.4 * c) + ")";
      fin.style.opacity = f;
      sparks.forEach(function (s) {
        var at = parseFloat(s.dataset.at), k = seg(p, at - 0.06, at + 0.06), pulse = Math.sin(k * Math.PI);
        s.style.opacity = pulse; s.style.transform = "scale(" + (0.3 + pulse) + ") rotate(" + (k * 90) + "deg)";
      });
      copy.style.opacity = t; copy.style.transform = (window.innerWidth >= 1000 ? "translateY(50%) " : "") + "translateY(" + (30 * (1 - t)) + "px)";
      var on = p < 0.34 ? 0 : p < 0.7 ? 1 : 2;
      steps.forEach(function (li, i) { li.classList.toggle("is-on", i === on); });
    };
    var onScroll = function () { if (!ticking) { ticking = true; requestAnimationFrame(render); } };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    render();
  }

  var gal = document.querySelector("[data-gallery]");
  if (gal && window.fetch && window.JSON) {
    var esc = function (v) { return String(v == null ? "" : v).replace(/[&<>"]/g, function (ch) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]; }); };
    fetch("collections.json", { cache: "no-cache" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (data) {
      if (!data || !data.items) return;
      var html = data.items.map(function (it) {
        return '<li class="gcard reveal is-in" data-tilt><div class="media media--wide"><img src="' + esc(it.image) + '"' +
          (it.image_small ? ' srcset="' + esc(it.image_small) + ' 480w, ' + esc(it.image) + ' 800w" sizes="(min-width: 1040px) 360px, (min-width: 640px) 46vw, 92vw"' : "") +
          ' width="800" height="600" alt="' + esc(it.alt) + '" loading="lazy" decoding="async">' +
          (it.illustrative ? '<span class="image-badge">' + esc(gal.dataset.badge) + '</span>' : "") +
          '</div><div class="gcard__body"><h3>' + esc(it.title) + '</h3><p class="gcard__cat">' + esc(it.category) + '</p><p>Styles and details: <mark class="ph-inline">' + esc(it.details || "To confirm") + '</mark></p></div></li>';
      }).join("");
      var ids = data.items.map(function (it) { return it.image; }).join("|");
      var cur = [].map.call(gal.querySelectorAll("img"), function (im) { return im.getAttribute("src"); }).join("|");
      if (ids !== cur) gal.innerHTML = html;   // only touch the DOM when the file differs from the built page (no layout shift otherwise)
    }).catch(function () {});
  }

  // ---------- Reviews carousel ----------
  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    var slides = [].slice.call(root.querySelectorAll("[data-slide]"));
    var dots = [].slice.call(root.querySelectorAll("[data-dot]"));
    var viewport = root.querySelector(".carousel__viewport");
    var pauseBtn = root.querySelector("[data-pause]");
    var pauseLabel = root.querySelector("[data-pause-label]");
    var current = 0, timer = null, userPaused = reduce(), hoverPause = false;
    var DELAY = 7000;
    var show = function (i) {
      current = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) {
        s.classList.toggle("is-active", k === current);
        s.classList.toggle("is-before", k < current);
        s.setAttribute("aria-hidden", k === current ? "false" : "true");
      });
      dots.forEach(function (d, k) { if (k === current) d.setAttribute("aria-current", "true"); else d.removeAttribute("aria-current"); });
    };
    var running = function () { return !userPaused && !hoverPause && !reduce(); };
    var schedule = function () {
      clearTimeout(timer);
      viewport.setAttribute("aria-live", running() ? "off" : "polite");
      if (running()) timer = setTimeout(function () { show(current + 1); schedule(); }, DELAY);
    };
    var setPaused = function (p) {
      userPaused = p;
      pauseLabel.textContent = p ? "Play" : "Pause";
      pauseBtn.querySelector("svg").outerHTML = p
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 4.5v15l12-7.5z"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M8 5v14M16 5v14"/></svg>';
      schedule();
    };
    root.querySelector("[data-prev]").addEventListener("click", function () { show(current - 1); schedule(); });
    root.querySelector("[data-next]").addEventListener("click", function () { show(current + 1); schedule(); });
    dots.forEach(function (d) { d.addEventListener("click", function () { show(+d.getAttribute("data-dot")); schedule(); }); });
    pauseBtn.addEventListener("click", function () { setPaused(!userPaused); });
    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { show(current + 1); schedule(); e.preventDefault(); }
      else if (e.key === "ArrowLeft") { show(current - 1); schedule(); e.preventDefault(); }
    });
    // Pause while hovered or while keyboard focus is inside (WCAG 2.2.2).
    root.addEventListener("mouseenter", function () { hoverPause = true; schedule(); });
    root.addEventListener("mouseleave", function () { hoverPause = false; schedule(); });
    root.addEventListener("focusin", function () { hoverPause = true; schedule(); });
    root.addEventListener("focusout", function (e) { if (!root.contains(e.relatedTarget)) { hoverPause = false; schedule(); } });
    // Only rotate while the carousel is on screen and the tab is visible.
    var visible = false;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) schedule(); else clearTimeout(timer); }).observe(root);
    }
    document.addEventListener("visibilitychange", function () { if (document.hidden) clearTimeout(timer); else if (visible) schedule(); });
    reduceMQ.addEventListener && reduceMQ.addEventListener("change", function () { if (reduce()) { setPaused(true); pauseBtn.hidden = true; } });
    if (userPaused) { setPaused(true); pauseBtn.hidden = true; }
    show(0);
  });
  }
})();

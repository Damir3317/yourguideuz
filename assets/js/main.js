/* ==========================================================================
   YourGuideUz — shared behaviour
   Vanilla JS, no dependencies. Progressive enhancement: all markup is
   readable/functional without JS; this layer adds motion + interactivity.
   ========================================================================== */
(function () {
  "use strict";

  var WHATSAPP_NUMBER = "998907433317";
  var TELEGRAM_HANDLE = "sds_1904";
  var contactChoiceOpener = null;

  function currentLang() {
    return document.documentElement.getAttribute("lang") === "ru" ? "ru" : "en";
  }

  document.addEventListener("DOMContentLoaded", function () {
    initHeader();
    initMobileNav();
    initAnalytics();
    initLanguage();
    initReveal();
    initCounters();
    initTestimonials();
    initAccordion();
    initModals();
    initBackToTop();
    initContactForm();
    initFooterYear();
    initFabLinks();
    initFilters();
    initContactChoice();
    initLightbox();
    initFabScrollHide();
  });

  /* ---------------------------------------------------------------------- */
  function initHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 40);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------------------------------------------------------------- */
  function initMobileNav() {
    var toggle = document.querySelector(".nav-toggle");
    var scrim = document.querySelector(".nav-scrim");
    if (!toggle) return;
    var close = function () { document.body.classList.remove("nav-open"); };
    toggle.addEventListener("click", function () {
      document.body.classList.toggle("nav-open");
    });
    if (scrim) scrim.addEventListener("click", close);
    document.querySelectorAll(".main-nav .nav-links a").forEach(function (a) {
      a.addEventListener("click", close);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  /* ---------------------------------------------------------------------- */
  function trackContactClick(method) {
    if (typeof window.gtag === "function") {
      window.gtag("event", "contact_click", { method: method });
    }
  }

  function initAnalytics() {
    document.addEventListener("click", function (e) {
      var link = e.target.closest ? e.target.closest("a") : null;
      if (!link) return;
      var href = link.getAttribute("href") || "";

      if (/^https:\/\/(wa\.me|api\.whatsapp\.com)\//i.test(href)) trackContactClick("whatsapp");
      else if (/^https:\/\/t\.me\//i.test(href)) trackContactClick("telegram");
      else if (/^tel:/i.test(href)) trackContactClick("phone");
      else if (/^mailto:/i.test(href)) trackContactClick("email");
      else if (href === "/contact" && link.classList.contains("btn")) trackContactClick("booking_button");
    });
  }

  /* ---------------------------------------------------------------------- */
  function initLanguage() {
    var stored = null;
    try { stored = localStorage.getItem("yg_lang"); } catch (e) {}
    // Travel Guide pages have one fixed language per URL (for search engines).
    // There the EN/RU buttons load the translated URL in the background and
    // swap the text in place (same structure on both), keeping the reading
    // position; a full page load is the fallback.
    var fixed = document.body.hasAttribute("data-fixed-lang") ? document.documentElement.getAttribute("lang") : null;
    var lang = fixed || stored || "en";
    applyLanguage(lang);
    if (fixed) {
      restoreReadingPosition();
      var warm = function () { fetchAlternate(fixed === "ru" ? "en" : "ru"); };
      if (document.readyState === "complete") setTimeout(warm, 300);
      else window.addEventListener("load", function () { setTimeout(warm, 300); }, { once: true });
    }

    var busy = false;
    document.querySelectorAll(".lang-switch button").forEach(function (btn) {
      var warmUp = function () {
        var t = btn.getAttribute("data-lang");
        if (fixed && t !== fixed) fetchAlternate(t);
      };
      btn.addEventListener("pointerdown", warmUp, { passive: true });
      btn.addEventListener("touchstart", warmUp, { passive: true });
      btn.addEventListener("click", function () {
        var target = btn.getAttribute("data-lang");
        if (fixed && target !== fixed) {
          var path = alternatePath(target);
          if (!path || busy) return;
          busy = true;
          try { localStorage.setItem("yg_lang", target); } catch (e) {}
          var pos = captureReadingPosition(path);
          var fallback = function () {
            try { sessionStorage.setItem(READ_POS_KEY, JSON.stringify(pos)); } catch (e) {}
            window.location.href = path;
          };
          var request = fetchAlternate(target);
          if (!request) { fallback(); return; }
          request.then(function (html) {
            if (!html || !swapToTranslation(html, path)) { fallback(); return; }
            fixed = target;
            try { history.pushState({ ygLang: target }, "", path); } catch (e) { fallback(); return; }
            applyLanguage(target);
            scrollToReading(pos);
            if (!popstateBound) {
              popstateBound = true;
              window.addEventListener("popstate", function () { window.location.reload(); });
            }
            busy = false;
            fetchAlternate(target === "ru" ? "en" : "ru");
          });
          return;
        }
        applyLanguage(target);
      });
    });
  }

  var popstateBound = false;
  var altPages = {};

  function alternatePath(lang) {
    var alt = document.querySelector('link[rel="alternate"][hreflang="' + lang + '"]');
    return alt ? new URL(alt.getAttribute("href"), window.location.href).pathname : null;
  }

  // Fetches (once) the other-language version of the current page as HTML text.
  function fetchAlternate(lang) {
    var path = alternatePath(lang);
    if (!path || !window.fetch || !window.DOMParser || !window.Promise) return null;
    if (!altPages[path]) {
      altPages[path] = fetch(path, { credentials: "same-origin" })
        .then(function (r) { return r.ok ? r.text() : null; })
        .catch(function () { return null; })
        .then(function (html) { if (!html) delete altPages[path]; return html; });
    }
    return altPages[path];
  }

  var SWAP_SKIP_ATTRS = { "class": 1, "style": 1, "open": 1, "aria-expanded": 1, "aria-hidden": 1, "hidden": 1 };

  function swapChildren(el) {
    return Array.prototype.filter.call(el.children, function (c) {
      return c.tagName !== "SCRIPT" && c.tagName !== "NOSCRIPT";
    });
  }

  function sameShape(a, b) {
    if (a.tagName !== b.tagName) return false;
    var ac = swapChildren(a), bc = swapChildren(b);
    if (ac.length !== bc.length) return false;
    for (var i = 0; i < ac.length; i++) if (!sameShape(ac[i], bc[i])) return false;
    return true;
  }

  // Copies texts and attributes from b into the live element a, keeping a's
  // elements (and their event listeners / UI state) in place.
  // Relative URLs in the fetched page belong to *its* address, not the current
  // one, so they are made absolute before being copied over.
  var SWAP_URL_ATTRS = { src: 1, href: 1, poster: 1, action: 1 };
  var swapBase = null;

  function absUrl(value) {
    if (!value || /^(#|[a-z][a-z0-9+.-]*:|\/\/)/i.test(value)) return value;
    try {
      var u = new URL(value, swapBase);
      return u.origin === window.location.origin ? u.pathname + u.search + u.hash : u.href;
    } catch (e) { return value; }
  }

  function absSrcset(value) {
    return value.split(",").map(function (part) {
      var bits = part.trim().split(/\s+/);
      bits[0] = absUrl(bits[0]);
      return bits.join(" ");
    }).join(", ");
  }

  function syncInto(a, b) {
    Array.prototype.forEach.call(b.attributes, function (attr) {
      if (SWAP_SKIP_ATTRS[attr.name]) return;
      var value = attr.value;
      if (SWAP_URL_ATTRS[attr.name]) value = absUrl(value);
      else if (attr.name === "srcset") value = absSrcset(value);
      if (a.getAttribute(attr.name) !== value) a.setAttribute(attr.name, value);
    });
    var ac = swapChildren(a);
    Array.prototype.slice.call(a.childNodes).forEach(function (n) { if (n.nodeType === 3) a.removeChild(n); });
    var i = 0;
    Array.prototype.forEach.call(b.childNodes, function (n) {
      if (n.nodeType === 3) a.insertBefore(document.createTextNode(n.nodeValue), ac[i] || null);
      else if (n.nodeType === 1 && n.tagName !== "SCRIPT" && n.tagName !== "NOSCRIPT") syncInto(ac[i++], n);
    });
  }

  function swapToTranslation(html, path) {
    var doc;
    try { doc = new DOMParser().parseFromString(html, "text/html"); } catch (e) { return false; }
    if (!doc.body || !doc.body.hasAttribute("data-fixed-lang") || !sameShape(document.body, doc.body)) return false;

    // <head>: title, meta tags, canonical, structured data.
    document.title = doc.title;
    doc.head.querySelectorAll("meta[name], meta[property]").forEach(function (m) {
      var key = m.getAttribute("name") ? 'meta[name="' + m.getAttribute("name") + '"]' : 'meta[property="' + m.getAttribute("property") + '"]';
      var live = document.head.querySelector(key);
      if (live) live.setAttribute("content", m.getAttribute("content") || "");
    });
    var canon = doc.head.querySelector('link[rel="canonical"]');
    var liveCanon = document.head.querySelector('link[rel="canonical"]');
    if (canon && liveCanon) liveCanon.setAttribute("href", canon.getAttribute("href"));
    var ld = doc.querySelectorAll('script[type="application/ld+json"]');
    var liveLd = document.querySelectorAll('script[type="application/ld+json"]');
    if (ld.length === liveLd.length) ld.forEach(function (s, i) { liveLd[i].textContent = s.textContent; });

    swapBase = new URL(path, window.location.href).href;
    syncInto(document.body, doc.body);
    document.documentElement.setAttribute("lang", doc.documentElement.getAttribute("lang") || "en");
    document.querySelectorAll(".accordion-item.open .accordion-panel").forEach(function (p) {
      p.style.maxHeight = p.scrollHeight + "px";
    });
    return true;
  }

  // EN and RU versions of a fixed-language page share the same structure, so
  // the reading position is kept as "element N, X% into it" rather than pixels.
  var READ_POS_KEY = "yg_read_pos";
  var READ_POS_SEL = "main h1, main h2, main h3, main h4, main p, main figure, main li, main summary, main blockquote, main table";

  function headerOffset() {
    var h = document.querySelector(".site-header");
    return h ? h.getBoundingClientRect().height : 0;
  }

  // Layout position (offsetTop ignores the transforms used by reveal animations).
  function layoutTop(el) {
    var y = 0;
    while (el) { y += el.offsetTop; el = el.offsetParent; }
    return y;
  }

  function captureReadingPosition(targetPath) {
    var els = document.querySelectorAll(READ_POS_SEL);
    var line = headerOffset() + 8;
    var data = { path: targetPath, count: els.length, idx: -1, frac: 0,
      ratio: window.scrollY / Math.max(1, document.documentElement.scrollHeight - window.innerHeight) };
    if (window.scrollY > 0) {
      for (var i = 0; i < els.length; i++) {
        var h = els[i].offsetHeight;
        var t = layoutTop(els[i]) - window.scrollY;
        if (h > 0 && t + h > line) {
          data.idx = i;
          data.frac = Math.min(1, Math.max(0, (line - t) / h));
          break;
        }
      }
    }
    return data;
  }

  function scrollToReading(data) {
    var els = document.querySelectorAll(READ_POS_SEL);
    var top;
    if (data.idx < 0) {
      top = 0;
    } else if (els.length === data.count && els[data.idx]) {
      var el = els[data.idx];
      top = layoutTop(el) + data.frac * el.offsetHeight - headerOffset() - 8;
    } else {
      top = data.ratio * (document.documentElement.scrollHeight - window.innerHeight);
    }
    window.scrollTo({ top: Math.max(0, top), behavior: "instant" });
  }

  function restoreReadingPosition() {
    var data = null;
    try {
      data = JSON.parse(sessionStorage.getItem(READ_POS_KEY) || "null");
      sessionStorage.removeItem(READ_POS_KEY);
    } catch (e) {}
    if (!data || data.path !== window.location.pathname) return;
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    scrollToReading(data);
    // Re-apply once fonts/images settle the layout, unless the reader has scrolled.
    var userMoved = false;
    var markMoved = function () { userMoved = true; };
    ["wheel", "touchstart", "keydown"].forEach(function (ev) {
      window.addEventListener(ev, markMoved, { once: true, passive: true });
    });
    var again = function () { if (!userMoved) scrollToReading(data); };
    window.addEventListener("load", again, { once: true });
    setTimeout(again, 400);
  }

  function applyLanguage(lang) {
    if (lang !== "en" && lang !== "ru") lang = "en";
    document.documentElement.setAttribute("lang", lang);

    document.querySelectorAll("[data-en]").forEach(function (el) {
      var value = el.getAttribute("data-" + lang) || el.getAttribute("data-en");
      if (value !== null) el.textContent = value;
    });
    document.querySelectorAll("[data-en-html]").forEach(function (el) {
      var value = el.getAttribute("data-" + lang + "-html") || el.getAttribute("data-en-html");
      if (value !== null) el.innerHTML = value;
    });
    document.querySelectorAll('a[href="/travel-guide"], a[href="/ru/travel-guide"]').forEach(function (el) {
      el.setAttribute("href", lang === "ru" ? "/ru/travel-guide" : "/travel-guide");
    });
    document.querySelectorAll("[data-en-href]").forEach(function (el) {
      var value = el.getAttribute("data-" + lang + "-href") || el.getAttribute("data-en-href");
      if (value !== null) el.setAttribute("href", value);
    });
    document.querySelectorAll("[data-en-content]").forEach(function (el) {
      var value = el.getAttribute("data-" + lang + "-content") || el.getAttribute("data-en-content");
      if (value !== null) el.setAttribute("content", value);
    });
    document.querySelectorAll("[data-en-placeholder]").forEach(function (el) {
      var value = el.getAttribute("data-" + lang + "-placeholder") || el.getAttribute("data-en-placeholder");
      if (value !== null) el.setAttribute("placeholder", value);
    });

    document.querySelectorAll(".lang-switch button").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-lang") === lang);
    });

    try { localStorage.setItem("yg_lang", lang); } catch (e) {}
  }

  /* ---------------------------------------------------------------------- */
  function initReveal() {
    var items = document.querySelectorAll(".reveal, .reveal-scale");
    if (!items.length) return;

    document.querySelectorAll(".stagger").forEach(function (group) {
      Array.prototype.forEach.call(group.children, function (child, i) {
        child.style.setProperty("--i", i);
      });
    });

    if (!("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("visible"); });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    items.forEach(function (el) { observer.observe(el); });
  }

  /* ---------------------------------------------------------------------- */
  function initCounters() {
    var counters = document.querySelectorAll("[data-count-to]");
    if (!counters.length) return;

    var animate = function (el) {
      var target = parseFloat(el.getAttribute("data-count-to"));
      var duration = 1600;
      var start = null;
      var decimals = el.getAttribute("data-decimals") ? parseInt(el.getAttribute("data-decimals"), 10) : 0;

      var step = function (ts) {
        if (start === null) start = ts;
        var progress = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        var value = target * eased;
        el.textContent = decimals ? value.toFixed(decimals) : Math.round(value).toString();
        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = decimals ? target.toFixed(decimals) : target.toString();
      };
      requestAnimationFrame(step);
    };

    if (!("IntersectionObserver" in window)) {
      counters.forEach(animate);
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animate(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.6 }
    );
    counters.forEach(function (el) { observer.observe(el); });
  }

  /* ---------------------------------------------------------------------- */
  function initTestimonials() {
    var track = document.querySelector(".testimonial-slides");
    if (!track) return;
    var slides = Array.prototype.slice.call(track.children);
    var dotsWrap = document.querySelector(".testimonial-dots");
    var prevBtn = document.querySelector(".t-arrow.prev");
    var nextBtn = document.querySelector(".t-arrow.next");
    var index = 0;
    var timer = null;

    slides.forEach(function (_, i) {
      var dot = document.createElement("button");
      dot.type = "button";
      dot.setAttribute("aria-label", "Go to testimonial " + (i + 1));
      if (i === 0) dot.classList.add("active");
      dot.addEventListener("click", function () { goTo(i); resetTimer(); });
      if (dotsWrap) dotsWrap.appendChild(dot);
    });
    var dots = dotsWrap ? Array.prototype.slice.call(dotsWrap.children) : [];

    function goTo(i) {
      index = (i + slides.length) % slides.length;
      track.style.transform = "translateX(-" + index * 100 + "%)";
      dots.forEach(function (d, di) { d.classList.toggle("active", di === index); });
    }

    function resetTimer() {
      if (timer) clearInterval(timer);
      timer = setInterval(function () { goTo(index + 1); }, 6000);
    }

    if (prevBtn) prevBtn.addEventListener("click", function () { goTo(index - 1); resetTimer(); });
    if (nextBtn) nextBtn.addEventListener("click", function () { goTo(index + 1); resetTimer(); });

    var wrap = document.querySelector(".testimonial-track");
    if (wrap) {
      wrap.addEventListener("mouseenter", function () { if (timer) clearInterval(timer); });
      wrap.addEventListener("mouseleave", resetTimer);
    }

    goTo(0);
    resetTimer();
  }

  /* ---------------------------------------------------------------------- */
  function initAccordion() {
    document.querySelectorAll(".accordion-item").forEach(function (item) {
      var trigger = item.querySelector(".accordion-trigger");
      var panel = item.querySelector(".accordion-panel");
      if (!trigger || !panel) return;
      trigger.addEventListener("click", function () {
        var isOpen = item.classList.contains("open");
        item.parentElement.querySelectorAll(".accordion-item.open").forEach(function (other) {
          if (other !== item) {
            other.classList.remove("open");
            other.querySelector(".accordion-panel").style.maxHeight = null;
          }
        });
        item.classList.toggle("open", !isOpen);
        panel.style.maxHeight = !isOpen ? panel.scrollHeight + "px" : null;
      });
    });
  }

  /* ---------------------------------------------------------------------- */
  function initModals() {
    var openers = document.querySelectorAll("[data-modal-open]");
    // #modal-lightbox and #modal-contact-choice manage their own open/close
    // logic (initLightbox / initContactChoice) since they can be triggered
    // from inside another already-open modal. Binding their close buttons
    // here too would close whichever tour modal is still tracked as
    // "current" underneath them.
    var closeButtons = document.querySelectorAll(".modal-overlay:not(#modal-lightbox):not(#modal-contact-choice) [data-modal-close]");
    var current = null;

    var open = function (modal) {
      if (!modal) return;
      modal.classList.add("open");
      document.body.style.overflow = "hidden";
      current = modal;
    };
    var close = function () {
      if (!current) return;
      current.classList.remove("open");
      document.body.style.overflow = "";
      current = null;
    };

    openers.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-modal-open");
        open(document.getElementById(id));
      });
    });
    closeButtons.forEach(function (btn) { btn.addEventListener("click", close); });
    document.querySelectorAll(".modal-overlay:not(#modal-lightbox):not(#modal-contact-choice)").forEach(function (overlay) {
      overlay.addEventListener("click", function (e) {
        if (e.target === overlay) close();
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      var lightbox = document.getElementById("modal-lightbox");
      var contactChoice = document.getElementById("modal-contact-choice");
      if ((lightbox && lightbox.classList.contains("open")) || (contactChoice && contactChoice.classList.contains("open"))) return;
      close();
    });
  }

  /* ---------------------------------------------------------------------- */
  function initBackToTop() {
    var btn = document.querySelector(".fab-top");
    if (!btn) return;
    window.addEventListener(
      "scroll",
      function () { btn.classList.toggle("visible", window.scrollY > 500); },
      { passive: true }
    );
    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------------------------------------------------------------------- */
  function initFabLinks() {
    var wa = document.querySelector(".fab-whatsapp");
    if (wa) wa.href = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent("Hi YourGuideUz! I'd like to know more about your tours.");
    var tg = document.querySelector(".fab-telegram");
    if (tg) tg.href = "https://t.me/" + TELEGRAM_HANDLE;
  }

  /* ---------------------------------------------------------------------- */
  function initContactForm() {
    var form = document.querySelector("#contact-form");
    if (!form) return;
    var success = document.querySelector(".form-success");

    var LABELS = {
      en: { greeting: "Hello YourGuideUz! I'd like to plan a trip.", name: "Name", tour: "Tour of interest", travelers: "Travelers", dates: "Preferred dates", message: "Message" },
      ru: { greeting: "Здравствуйте, YourGuideUz! Хочу спланировать поездку.", name: "Имя", tour: "Интересующий тур", travelers: "Количество туристов", dates: "Предпочтительные даты", message: "Сообщение" }
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var name = (data.get("name") || "").toString().trim();
      var travelers = (data.get("travelers") || "").toString().trim();
      var tour = (data.get("tour") || "").toString().trim();
      var dates = (data.get("dates") || "").toString().trim();
      var message = (data.get("message") || "").toString().trim();
      var t = LABELS[currentLang()];

      var lines = [
        t.greeting,
        t.name + ": " + (name || "-"),
        tour ? t.tour + ": " + tour : null,
        travelers ? t.travelers + ": " + travelers : null,
        dates ? t.dates + ": " + dates : null,
        message ? t.message + ": " + message : null
      ].filter(Boolean);

      var fullMessage = lines.join("\n");

      trackContactClick("form");

      if (success) success.classList.add("visible");
      form.reset();

      if (typeof contactChoiceOpener === "function") {
        contactChoiceOpener(fullMessage);
      } else {
        var url = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(fullMessage);
        window.open(url, "_blank", "noopener");
      }
    });
  }

  /* ---------------------------------------------------------------------- */
  function initFilters() {
    var chips = document.querySelectorAll(".filter-chip");
    var cards = document.querySelectorAll("[data-category]");
    if (!chips.length || !cards.length) return;

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        chips.forEach(function (c) { c.classList.remove("active"); });
        chip.classList.add("active");
        var filter = chip.getAttribute("data-filter");

        cards.forEach(function (card) {
          var match = filter === "all" || card.getAttribute("data-category") === filter;
          card.style.display = match ? "" : "none";
        });
      });
    });
  }

  /* ---------------------------------------------------------------------- */
  function initContactChoice() {
    var modal = document.getElementById("modal-contact-choice");
    if (!modal) return;
    var tgLink = modal.querySelector("[data-contact-telegram]");
    var waLink = modal.querySelector("[data-contact-whatsapp]");
    var closeButtons = modal.querySelectorAll("[data-modal-close]");
    var triggers = document.querySelectorAll('a.btn[href="/contact"]');

    var BOOK_PREFIX = { en: "Hello YourGuideUz! I'd like to book: ", ru: "Здравствуйте, YourGuideUz! Хочу забронировать: " };
    var DEFAULT_MSG = { en: "Hello YourGuideUz! I'd like to plan a trip.", ru: "Здравствуйте, YourGuideUz! Хочу спланировать поездку." };

    var openModal = function (message) {
      if (tgLink) tgLink.href = "https://t.me/" + TELEGRAM_HANDLE;
      if (waLink) waLink.href = "https://wa.me/" + WHATSAPP_NUMBER + (message ? "?text=" + encodeURIComponent(message) : "");
      modal.classList.add("open");
      document.body.style.overflow = "hidden";
    };
    contactChoiceOpener = openModal;
    var closeModal = function () {
      modal.classList.remove("open");
      document.body.style.overflow = "";
    };

    triggers.forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var lang = currentLang();
        var message = DEFAULT_MSG[lang];
        var modalBody = btn.closest(".modal-body");
        if (modalBody) {
          var h3 = modalBody.querySelector("h3");
          if (h3 && h3.textContent.trim()) {
            message = BOOK_PREFIX[lang] + h3.textContent.trim();
          }
        }
        openModal(message);
      });
    });

    closeButtons.forEach(function (btn) { btn.addEventListener("click", closeModal); });
    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeModal();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.classList.contains("open")) closeModal();
    });
  }

  /* ---------------------------------------------------------------------- */
  function initLightbox() {
    var modal = document.getElementById("modal-lightbox");
    if (!modal) return;
    var img = modal.querySelector("img");
    var prevBtn = modal.querySelector(".lightbox-prev");
    var nextBtn = modal.querySelector(".lightbox-next");
    var closeButtons = modal.querySelectorAll("[data-modal-close]");
    var triggers = document.querySelectorAll(".review-shot-card img, .tour-gallery img");
    if (!triggers.length) return;

    var group = [];
    var index = 0;

    var show = function (i) {
      index = (i + group.length) % group.length;
      var thumb = group[index];
      img.src = thumb.src;
      img.alt = thumb.alt;
      var multiple = group.length > 1;
      if (prevBtn) prevBtn.style.display = multiple ? "" : "none";
      if (nextBtn) nextBtn.style.display = multiple ? "" : "none";
    };

    var openModal = function (thumb) {
      var container = thumb.closest(".tour-gallery, .review-shots-grid");
      group = container ? Array.prototype.slice.call(container.querySelectorAll("img")) : [thumb];
      show(group.indexOf(thumb));
      modal.classList.add("open");
      document.body.style.overflow = "hidden";
    };
    var closeModal = function () {
      modal.classList.remove("open");
      document.body.style.overflow = "";
      img.src = "";
    };

    triggers.forEach(function (thumb) {
      thumb.addEventListener("click", function () {
        openModal(thumb);
      });
    });

    if (prevBtn) prevBtn.addEventListener("click", function (e) { e.stopPropagation(); show(index - 1); });
    if (nextBtn) nextBtn.addEventListener("click", function (e) { e.stopPropagation(); show(index + 1); });

    closeButtons.forEach(function (btn) { btn.addEventListener("click", closeModal); });
    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeModal();
    });
    document.addEventListener("keydown", function (e) {
      if (!modal.classList.contains("open")) return;
      if (e.key === "Escape") closeModal();
      else if (e.key === "ArrowLeft") show(index - 1);
      else if (e.key === "ArrowRight") show(index + 1);
    });

    var touchStartX = 0;
    var touchStartY = 0;
    modal.addEventListener("touchstart", function (e) {
      touchStartX = e.changedTouches[0].clientX;
      touchStartY = e.changedTouches[0].clientY;
    }, { passive: true });
    modal.addEventListener("touchend", function (e) {
      var dx = e.changedTouches[0].clientX - touchStartX;
      var dy = e.changedTouches[0].clientY - touchStartY;
      if (Math.abs(dx) < 40 || Math.abs(dx) < Math.abs(dy)) return;
      if (dx < 0) show(index + 1);
      else show(index - 1);
    }, { passive: true });
  }

  /* ---------------------------------------------------------------------- */
  function initFabScrollHide() {
    var mq = window.matchMedia("(max-width: 640px)");
    var hideTimer = null;
    var onScroll = function () {
      if (!mq.matches) return;
      document.body.classList.add("is-scrolling");
      if (hideTimer) clearTimeout(hideTimer);
      hideTimer = setTimeout(function () {
        document.body.classList.remove("is-scrolling");
      }, 500);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------------------------------------------------------------- */
  function initFooterYear() {
    var el = document.querySelector("#year");
    if (el) el.textContent = new Date().getFullYear().toString();
  }
})();

/* Shared by the English and Spanish pages. Strings are chosen from the document's
   own lang attribute, so there is one copy of the behaviour and no chance of the
   two pages drifting apart.

   Everything that touches the DOM lives in an init function called from boot(),
   because switching language replaces the page content in place and every binding
   has to be remade against the new nodes. Window and document listeners are
   registered with an AbortSignal so a re-boot cannot stack duplicates. */
(function () {
  'use strict';

  var STRINGS = {
    en: {
      sending: 'Sending…',
      ok: "You're on the list. We'll write when there's something real to report.",
      failed: 'That did not go through. Try again in a moment.',
      unreachable: 'Could not reach the server. Try again in a moment.',
      signedUp: 'Signed up',
      close: 'Close'
    },
    es: {
      sending: 'Enviando…',
      ok: 'Ya estás en la lista. Te escribiremos cuando haya algo real que contar.',
      failed: 'No se pudo enviar. Inténtalo de nuevo en un momento.',
      unreachable: 'No se pudo conectar con el servidor. Inténtalo de nuevo en un momento.',
      signedUp: 'Listo',
      close: 'Cerrar'
    }
  };

  var ENDPOINT = 'https://ccdc.blaha.io/api/signup';
  function T() { return STRINGS[document.documentElement.lang] || STRINGS.en; }
  function reduced() { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }

  /* ---- water-comparison bars fill as they scroll into view ---- */
  function initBars() {
    var bars = document.querySelectorAll('.bar-fill');
    if (!bars.length) return;
    function fill(el) { el.style.width = el.getAttribute('data-w') + '%'; }
    if (reduced() || !('IntersectionObserver' in window)) {
      bars.forEach(fill);
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        setTimeout(function () { fill(el); }, Array.prototype.indexOf.call(bars, el) * 130);
        io.unobserve(el);
      });
    }, { threshold: 0.4 });
    bars.forEach(function (b) { io.observe(b); });
  }

  /* ---- signup modal ----
     Without JS the anchors still work via the :target rule. This adds what CSS
     cannot: focus trap, Esc, scroll lock, focus returned to the trigger, and no
     leftover #signup in the URL. */
  function initModal(signal) {
    var modal = document.getElementById('signup');
    if (!modal) return;
    var card = modal.querySelector('.modal-card');
    var lastTrigger = null;

    function focusables() {
      return Array.prototype.filter.call(
        card.querySelectorAll('a[href], button, input:not([type="hidden"]), textarea, [tabindex]:not([tabindex="-1"])'),
        function (el) { return el.offsetParent !== null && !el.disabled; }
      );
    }
    function open(trigger) {
      lastTrigger = trigger || null;
      modal.classList.add('is-open');
      document.body.classList.add('modal-open');
      var first = card.querySelector('#contact');
      if (first) first.focus();
    }
    function close() {
      modal.classList.remove('is-open');
      document.body.classList.remove('modal-open');
      if (location.hash === '#signup') {
        history.replaceState(null, '', location.pathname + location.search);
      }
      if (lastTrigger) { lastTrigger.focus(); lastTrigger = null; }
    }

    document.querySelectorAll('a[href="#signup"]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); open(a); });
    });
    modal.addEventListener('click', function (e) {
      if (e.target.closest('.modal-close, [data-modal-close]') || e.target.classList.contains('modal-scrim')) {
        e.preventDefault();
        close();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (!modal.classList.contains('is-open')) return;
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key !== 'Tab') return;
      var f = focusables();
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }, { signal: signal });

    if (location.hash === '#signup') open(null);
  }

  /* ---- signup submit: fetch for an inline result; native POST without JS ---- */
  function initSignup() {
    var form = document.querySelector('form[action="' + ENDPOINT + '"]');
    if (!form) return;
    var msg = document.getElementById('form-msg');
    var stamp = document.getElementById('t');
    if (stamp) stamp.value = String(Date.now() / 1000);

    function say(text, kind) {
      msg.textContent = text;
      msg.className = 'form-msg show ' + kind;
    }

    form.addEventListener('submit', function (e) {
      if (!window.fetch) return;
      e.preventDefault();
      var t = T();
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = t.sending;

      fetch(ENDPOINT, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'fetch', 'Accept': 'application/json' }
      })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
        .then(function (res) {
          if (res.ok && res.d.ok) {
            form.reset();
            say(t.ok, 'ok');
            btn.textContent = t.signedUp;
            var cancel = form.querySelector('[data-modal-close]');
            if (cancel) cancel.textContent = t.close;
            return;
          }
          say(res.d.error || t.failed, 'err');
          btn.disabled = false;
          btn.textContent = original;
        })
        .catch(function () {
          say(t.unreachable, 'err');
          btn.disabled = false;
          btn.textContent = original;
        });
    });
  }

  /* ---- reason tabs ----
     The panels are all visible and stacked without JS, and the tablist is hidden
     by CSS because it would do nothing. Adding .js-tabs opts into the collapsed
     presentation, so no content is ever hidden from a reader who has no JS. */
  function initTabs(restoreIndex) {
    var wrap = document.getElementById('reason-tabs');
    if (!wrap) return;
    var tabs = Array.prototype.slice.call(wrap.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    if (!tabs.length || panels.indexOf(null) !== -1) return;

    function stickTop() {
      var v = getComputedStyle(document.documentElement).getPropertyValue('--stick-top');
      return parseFloat(v) || 0;
    }
    // Put the newly revealed panel directly under the sticky tab bar, so switching
    // tabs never leaves you reading from the middle of a panel.
    function scrollToContent() {
      var y = wrap.getBoundingClientRect().top + window.scrollY - stickTop();
      window.scrollTo({ top: Math.max(0, y), behavior: reduced() ? 'auto' : 'smooth' });
    }
    function select(i, focus, scroll) {
      tabs.forEach(function (t, j) {
        t.setAttribute('aria-selected', String(j === i));
        t.setAttribute('tabindex', j === i ? '0' : '-1');
        panels[j].hidden = j !== i;
      });
      if (focus) tabs[i].focus();
      if (scroll) scrollToContent();
    }

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i, false, true); });
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (d) { e.preventDefault(); select((i + d + tabs.length) % tabs.length, true, true); return; }
        if (e.key === 'Home') { e.preventDefault(); select(0, true, true); }
        if (e.key === 'End') { e.preventDefault(); select(tabs.length - 1, true, true); }
      });
    });

    wrap.classList.add('js-tabs');
    var start = 0;
    if (typeof restoreIndex === 'number' && restoreIndex > 0 && restoreIndex < tabs.length) start = restoreIndex;
    select(start, false, false);

    // A link to a specific reason should open that reason, not scroll past it.
    var deep = tabs.map(function (t) { return '#' + t.getAttribute('aria-controls'); }).indexOf(location.hash);
    if (deep !== -1) select(deep, false, true);
  }

  function selectedTabIndex() {
    var tabs = document.querySelectorAll('#reason-tabs [role="tab"]');
    for (var i = 0; i < tabs.length; i++) {
      if (tabs[i].getAttribute('aria-selected') === 'true') return i;
    }
    return 0;
  }

  /* ---- keep --stick-top honest: the sticky tablist sits under the section nav
         only while that nav is itself stuck to the top ---- */
  function initStickTop(signal) {
    var nav = document.querySelector('.sectionnav');
    if (!nav) return;
    function measure() {
      var stuck = getComputedStyle(nav).position === 'sticky';
      document.documentElement.style.setProperty(
        '--stick-top', stuck ? nav.getBoundingClientRect().height + 'px' : '0px');
    }
    measure();
    window.addEventListener('resize', measure, { signal: signal });
  }

  /* ---- section nav: mark the section currently in view ---- */
  function initSpy(signal) {
    var nav = document.querySelector('.sectionnav');
    if (!nav || !('IntersectionObserver' in window)) return;
    // Excludes the mark: it points at the hero, which is not an entry in the list.
    // Left in, it became the first spy target and took aria-current at the top of
    // the page, so no section entry was ever marked there.
    var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]:not(.nav-brand)'));
    var byId = {};
    links.forEach(function (a) {
      var el = document.getElementById(a.getAttribute('href').slice(1));
      if (el) byId[el.id] = a;
    });
    var targets = Object.keys(byId).map(function (id) { return document.getElementById(id); });
    if (!targets.length) return;

    function mark(a) {
      links.forEach(function (l) { l.removeAttribute('aria-current'); });
      if (a) a.setAttribute('aria-current', 'true');
    }
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting ? e.intersectionRatio : 0; });
      // Topmost intersecting section wins, so scrolling reads in document order.
      var best = null;
      targets.forEach(function (t) { if (!best && visible[t.id] > 0) best = t; });
      mark(best ? byId[best.id] : null);
    }, { rootMargin: '-25% 0px -60% 0px', threshold: [0, 0.01] });
    targets.forEach(function (t) { io.observe(t); });
    if (signal) signal.addEventListener('abort', function () { io.disconnect(); });
  }

  /* ---- reveal the rail's language flag once the hero switcher has scrolled away ----
     A direct scroll handler rather than requestAnimationFrame: this is one
     getBoundingClientRect and a class toggle, and rAF does not run in a tab that
     is not rendering, which made an earlier version untestable. */
  function initLangDock(signal) {
    var rail = document.querySelector('.sectionnav');
    var docked = rail && rail.querySelector('.nav-lang');
    var hero = document.querySelector('.hero .langbar');
    if (!rail || !docked || !hero) return;
    var wide = window.matchMedia('(min-width: 84rem)');
    var on = null;

    function apply() {
      var next = hero.getBoundingClientRect().bottom < 0;
      if (next === on) return;
      on = next;
      rail.classList.toggle('has-lang', next);
      // Exactly one switcher is exposed at a time, so a screen reader never meets
      // two language controls.
      if (wide.matches) {
        docked.setAttribute('aria-hidden', next ? 'false' : 'true');
        hero.setAttribute('aria-hidden', next ? 'true' : 'false');
        docked.querySelectorAll('a').forEach(function (a) {
          if (next) { a.removeAttribute('tabindex'); } else { a.setAttribute('tabindex', '-1'); }
        });
      }
    }
    function narrowHandover() {
      // Below 84rem the hero switcher is display:none and the nav flag is the only
      // control, so it must be the live one regardless of scroll position.
      docked.setAttribute('aria-hidden', 'false');
      hero.setAttribute('aria-hidden', 'true');
      docked.querySelectorAll('a').forEach(function (a) { a.removeAttribute('tabindex'); });
    }

    window.addEventListener('scroll', apply, { passive: true, signal: signal });
    window.addEventListener('resize', apply, { signal: signal });
    if (!wide.matches) narrowHandover();
    wide.addEventListener('change', function () {
      if (!wide.matches) { narrowHandover(); } else { on = null; }
      apply();
    }, { signal: signal });
    apply();
  }

  /* ---- language switch in place ----
     Swaps the page for the other language without a navigation, keeping the reader
     where they were. Section ids differ per language, so the position is recorded
     against data-section keys, which are identical on both pages, plus the offset
     into that section. Any failure falls back to a normal navigation, so the links
     always work. */

  function rememberChoice(lang) {
    // A deliberate click outranks Accept-Language on later visits. The server reads
    // this cookie before deciding whether to redirect.
    try {
      document.cookie = 'lang=' + lang + '; path=/; max-age=31536000; samesite=lax';
    } catch (e) { /* cookies disabled: the server falls back to Accept-Language */ }
  }

  function currentAnchor() {
    var secs = Array.prototype.slice.call(document.querySelectorAll('[data-section]'));
    for (var i = secs.length - 1; i >= 0; i--) {
      var r = secs[i].getBoundingClientRect();
      if (r.top <= 1) return { key: secs[i].getAttribute('data-section'), offset: -r.top };
    }
    return { key: 'hero', offset: 0 };
  }

  function restoreAnchor(a) {
    var el = document.querySelector('[data-section="' + a.key + '"]');
    if (!el) { window.scrollTo({ top: 0, behavior: 'auto' }); return; }
    var top = el.getBoundingClientRect().top + window.scrollY + a.offset;
    window.scrollTo({ top: Math.max(0, top), behavior: 'auto' });
  }

  function swapTo(url, push) {
    var anchor = currentAnchor();
    var tab = selectedTabIndex();
    return fetch(url, { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.text() : Promise.reject(new Error(r.status)); })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, 'text/html');
        if (!doc.body || !doc.querySelector('[data-section]')) throw new Error('unexpected document');
        // Keep our own script element; replace everything else in the body.
        var keep = document.querySelector('script[src]');
        Array.prototype.slice.call(document.body.children).forEach(function (el) {
          if (el !== keep) el.remove();
        });
        Array.prototype.slice.call(doc.body.children).forEach(function (el) {
          if (el.tagName === 'SCRIPT') return;
          document.body.insertBefore(document.importNode(el, true), keep);
        });
        var lang = doc.documentElement.lang || 'en';
        document.documentElement.lang = lang;
        document.title = doc.title;
        rememberChoice(lang);
        if (push) history.pushState({ ccdc: lang }, '', url);
        boot(tab);
        restoreAnchor(anchor);
      })
      .catch(function () { window.location.href = url; });
  }

  function initLangSwap(signal) {
    if (!window.fetch || !window.DOMParser || !history.pushState) return;
    document.querySelectorAll('a[hreflang]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
        e.preventDefault();
        swapTo(a.href, true);
      });
    });
    window.addEventListener('popstate', function () { swapTo(location.href, false); }, { signal: signal });
  }

  /* ---- the rail's mark returns to the top ----
     A real #top anchor, so it works with scripting off. With JS it scrolls smoothly
     and leaves no hash behind, matching how the modal cleans up after itself. */
  function initBrand() {
    var brand = document.querySelector('.sectionnav a.nav-brand');
    if (!brand) return;
    brand.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: reduced() ? 'auto' : 'smooth' });
      if (location.hash) history.replaceState(null, '', location.pathname + location.search);
    });
  }

  var ac = null;
  function boot(restoreTab) {
    if (ac) ac.abort();
    ac = new AbortController();
    var signal = ac.signal;
    initBars();
    initStickTop(signal);
    initModal(signal);
    initSignup();
    initTabs(restoreTab);
    initSpy(signal);
    initLangDock(signal);
    initLangSwap(signal);
    initBrand();
  }

  boot();
})();

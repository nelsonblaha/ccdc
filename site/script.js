/* Shared by the English and Spanish pages. Strings are chosen from the
   document's own lang attribute, so there is one copy of the behaviour and no
   chance of the two pages drifting apart. */
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

  var T = STRINGS[document.documentElement.lang] || STRINGS.en;
  var ENDPOINT = 'https://ccdc.blaha.io/api/signup';

  /* ---- water-comparison bars fill as they scroll into view ---- */
  (function () {
    var bars = document.querySelectorAll('.bar-fill');
    if (!bars.length) return;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function fill(el) { el.style.width = el.getAttribute('data-w') + '%'; }
    if (reduce || !('IntersectionObserver' in window)) {
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
  })();

  /* ---- signup modal ----
     Without JS the anchors still work via the :target rule. This adds what CSS
     cannot: focus trap, Esc, scroll lock, focus returned to the trigger, and no
     leftover #signup in the URL. */
  (function () {
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
      // :target would keep it open even after the class is gone.
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
    });

    // Someone arriving on a shared /#signup link gets the scripted modal.
    if (location.hash === '#signup') open(null);
  })();

  /* ---- signup submit: fetch for an inline result; native POST without JS ---- */
  (function () {
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
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = T.sending;

      fetch(ENDPOINT, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'fetch', 'Accept': 'application/json' }
      })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
        .then(function (res) {
          if (res.ok && res.d.ok) {
            form.reset();
            say(T.ok, 'ok');
            btn.textContent = T.signedUp;
            var cancel = form.querySelector('[data-modal-close]');
            if (cancel) cancel.textContent = T.close;
            return;
          }
          say(res.d.error || T.failed, 'err');
          btn.disabled = false;
          btn.textContent = original;
        })
        .catch(function () {
          say(T.unreachable, 'err');
          btn.disabled = false;
          btn.textContent = original;
        });
    });
  })();
  /* ---- reason tabs ----
     The panels are all visible and stacked without JS, and the tablist is hidden
     by CSS because it would do nothing. Adding .js-tabs opts into the collapsed
     presentation, so no content is ever hidden from a reader who has no JS. */
  (function () {
    var wrap = document.getElementById('reason-tabs');
    if (!wrap) return;
    var tabs = Array.prototype.slice.call(wrap.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    if (!tabs.length || panels.indexOf(null) !== -1) return;

    function stickTop() {
      var v = getComputedStyle(document.documentElement).getPropertyValue('--stick-top');
      return parseFloat(v) || 0;
    }

    // Put the newly revealed panel directly under the sticky tab bar, so
    // switching tabs never leaves you reading from the middle of a panel.
    function scrollToContent() {
      var y = wrap.getBoundingClientRect().top + window.scrollY - stickTop();
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: Math.max(0, y), behavior: reduce ? 'auto' : 'smooth' });
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
    select(0, false, false);

    // A link to a specific reason should open that reason, not scroll past it.
    var deep = tabs.map(function (t) { return '#' + t.getAttribute('aria-controls'); }).indexOf(location.hash);
    if (deep !== -1) select(deep, false, true);
  })();

  /* ---- keep --stick-top honest: the sticky tablist sits under the section nav
         only while that nav is itself stuck to the top ---- */
  (function () {
    var nav = document.querySelector('.sectionnav');
    if (!nav) return;
    function measure() {
      var stuck = getComputedStyle(nav).position === 'sticky';
      document.documentElement.style.setProperty(
        '--stick-top', stuck ? nav.getBoundingClientRect().height + 'px' : '0px');
    }
    measure();
    window.addEventListener('resize', measure);
  })();

  /* ---- section nav: mark the section currently in view ---- */
  (function () {
    var nav = document.querySelector('.sectionnav');
    if (!nav || !('IntersectionObserver' in window)) return;
    var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
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
  })();
  /* ---- reveal the rail's language flag once the hero switcher has scrolled away ----
     A direct scroll handler rather than requestAnimationFrame: this is one
     getBoundingClientRect and a class toggle, and rAF does not run in a tab that
     is not rendering, which made the previous version untestable. */
  (function () {
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

    window.addEventListener('scroll', apply, { passive: true });
    window.addEventListener('resize', apply);
    wide.addEventListener('change', function () {
      if (!wide.matches) {
        docked.setAttribute('aria-hidden', 'true');
        hero.setAttribute('aria-hidden', 'false');
      }
      on = null;
      apply();
    });
    apply();
  })();
})();

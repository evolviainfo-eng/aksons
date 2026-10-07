/* signature-web · base/motion.js (from the AKMIRA reference build, 2026-10-01)
   Studio motion as behaviour only; the look stays per client.
   Markup hooks: [data-nav] header, [data-hero] first screen, .rv text/UI blocks (never photos),
   [data-par="4"] wrapper around a framed photo (amplitude in percent), .intro overlay with .intro__mark,
   [data-menu], [data-menu-open], [data-menu-close], gallery: [data-lb] dialog, [data-open="key"][data-index],
   window.GALLERY = { key: [{src,w,h}] }, window.GALLERY_TITLES = { key: 'Title · Place' }.
   Load lenis.min.js before this file (defer both). In <head>, before any CSS paints:
   <script>(function(d){d.classList.add('js');var r=matchMedia('(prefers-reduced-motion: reduce)').matches,s;try{s=sessionStorage.getItem('intro-seen')}catch(e){}if(r||s)d.classList.add('no-intro')})(document.documentElement)</script>
   Without the .intro element the page simply skips it. */
(function () {
  var root = document.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var nav = document.querySelector('[data-nav]');
  var hero = document.querySelector('[data-hero]');
  var hasIntro = !!document.querySelector('.intro');
  if (!hasIntro) root.classList.add('no-intro');

  /* smooth scroll: wheel only, touch stays native */
  var lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  var navH = function () { return nav ? nav.offsetHeight : 0; };
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]'); if (!a) return;
    var id = a.getAttribute('href'); if (id.length < 2) return;
    var t = document.querySelector(id); if (!t) return;
    e.preventDefault();
    var off = (hero && t === hero) ? 0 : -navH() + 1;
    if (lenis) lenis.scrollTo(t, { offset: off, duration: 1.4 }); else window.scrollTo({ top: t.getBoundingClientRect().top + scrollY + off, behavior: reduce ? 'auto' : 'smooth' });
  });

  /* reveals: text and UI only, once; the hero waits for the intro */
  var els = [].slice.call(document.querySelectorAll('.rv'));
  var heroEls = els.filter(function (el) { return hero && hero.contains(el); });
  var restEls = els.filter(function (el) { return heroEls.indexOf(el) < 0; });
  var show = function (el) { el.classList.add('in'); };
  if (reduce || !('IntersectionObserver' in window)) { els.forEach(show); }
  else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting || e.boundingClientRect.top < 0) { show(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    restEls.forEach(function (el) { io.observe(el); });
    var sweep = function () { restEls.forEach(function (el) { var r = el.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) show(el); }); };
    setTimeout(sweep, 3200);
    addEventListener('pageshow', sweep);
    addEventListener('beforeprint', function () { els.forEach(show); });
  }

  /* intro: the client's mark once per session, then the hero settles */
  var ready = function () {
    root.classList.add('is-ready');
    setTimeout(function () { heroEls.forEach(show); }, root.classList.contains('no-intro') ? 120 : 380);
    try { sessionStorage.setItem('intro-seen', '1'); } catch (e) {}
  };
  var fontsReady = (document.fonts && document.fonts.ready) ? document.fonts.ready : Promise.resolve();
  if (root.classList.contains('no-intro')) { fontsReady.then(function () { requestAnimationFrame(ready); }); }
  else {
    if (lenis) lenis.stop();
    var t0 = Date.now();
    Promise.race([fontsReady, new Promise(function (r) { setTimeout(r, 2000); })]).then(function () {
      setTimeout(function () { ready(); if (lenis) lenis.start(); }, Math.max(0, 1250 - (Date.now() - t0)));
    });
  }
  setTimeout(function () { if (!root.classList.contains('is-ready')) { ready(); if (lenis) lenis.start(); } }, 3500);

  /* parallax inside the frame: desktop with a fine pointer only */
  var pars = [].slice.call(document.querySelectorAll('[data-par]'));
  var parOn = !reduce && finePointer && innerWidth >= 1024 && pars.length;
  var updatePar = function () {
    var vh = innerHeight;
    for (var i = 0; i < pars.length; i++) {
      var el = pars[i], box = el.parentElement.getBoundingClientRect();
      if (box.bottom < -100 || box.top > vh + 100) continue;
      var p = ((box.top + box.height / 2) - vh / 2) / (vh / 2 + box.height / 2);
      el.style.setProperty('--py', (-p * (+(el.getAttribute('data-par') || 4))).toFixed(3) + '%');
    }
  };
  if (parOn) { root.classList.add('has-par'); updatePar(); }

  /* nav: solid after the hero, steps away while reading down, returns on the way up */
  var lastY = scrollY, menuOpen = false;
  var onScroll = function (y) {
    if (parOn) updatePar();
    if (!nav) return;
    nav.classList.toggle('is-solid', hero ? hero.getBoundingClientRect().bottom <= navH() + 1 : true);
    var dy = y - lastY;
    if (!menuOpen && !reduce) {
      if (y > innerHeight * 0.9 && dy > 4) nav.classList.add('is-away');
      else if (dy < -4 || y < innerHeight * 0.5) nav.classList.remove('is-away');
    }
    lastY = y;
  };
  if (lenis) lenis.on('scroll', function (l) { onScroll(l.scroll); });
  else addEventListener('scroll', function () { onScroll(scrollY); }, { passive: true });
  addEventListener('resize', function () { onScroll(scrollY); });
  onScroll(scrollY);
  nav && nav.addEventListener('focusin', function () { nav.classList.remove('is-away'); });

  /* menu */
  var menu = document.querySelector('[data-menu]');
  var openBtn = document.querySelector('[data-menu-open]');
  var setMenu = function (open) {
    if (!menu) return;
    menuOpen = open; menu.hidden = !open;
    openBtn && openBtn.setAttribute('aria-expanded', String(open));
    if (lenis) { open ? lenis.stop() : lenis.start(); } else document.body.style.overflow = open ? 'hidden' : '';
    if (open) { var first = menu.querySelector('a'); first && first.focus(); } else { openBtn && openBtn.focus(); }
  };
  openBtn && openBtn.addEventListener('click', function () { setMenu(true); });
  menu && menu.addEventListener('click', function (e) { if (e.target.closest('[data-menu-close]')) setMenu(false); });
  addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu && !menu.hidden) setMenu(false); });

  /* gallery */
  var G = window.GALLERY || {}, titles = window.GALLERY_TITLES || {};
  var lb = document.querySelector('[data-lb]');
  if (!lb || typeof lb.showModal !== 'function') return;
  var img = lb.querySelector('[data-lb-img]'), tEl = lb.querySelector('[data-lb-title]'), cEl = lb.querySelector('[data-lb-count]');
  var cur = { key: null, i: 0 };
  var render = function () {
    var list = G[cur.key] || []; if (!list.length) return;
    var it = list[cur.i];
    img.classList.add('is-loading');
    var pre = new Image(); pre.onload = pre.onerror = function () { img.src = it.src; img.width = it.w; img.height = it.h; img.classList.remove('is-loading'); };
    pre.src = it.src;
    img.alt = (titles[cur.key] || '') + ', ' + (cur.i + 1) + ' / ' + list.length;
    if (tEl) tEl.textContent = titles[cur.key] || '';
    if (cEl) cEl.textContent = (cur.i + 1) + ' / ' + list.length;
    var nx = list[(cur.i + 1) % list.length]; if (nx) { var p2 = new Image(); p2.src = nx.src; }
  };
  var go = function (d) { var n = (G[cur.key] || []).length; if (!n) return; cur.i = (cur.i + d + n) % n; render(); };
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-open]'); if (!a) return;
    var key = a.getAttribute('data-open'); if (!G[key]) return;
    e.preventDefault(); cur.key = key; cur.i = +a.getAttribute('data-index') || 0; render();
    lb.showModal(); if (lenis) lenis.stop(); else document.body.style.overflow = 'hidden';
  });
  var q = function (s) { return lb.querySelector(s); };
  q('[data-lb-prev]') && q('[data-lb-prev]').addEventListener('click', function () { go(-1); });
  q('[data-lb-next]') && q('[data-lb-next]').addEventListener('click', function () { go(1); });
  q('[data-lb-close]') && q('[data-lb-close]').addEventListener('click', function () { lb.close(); });
  lb.addEventListener('close', function () { if (lenis) lenis.start(); else document.body.style.overflow = ''; });
  lb.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') go(1); if (e.key === 'ArrowLeft') go(-1); });
  var sx = null;
  lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1); sx = null; });
})();

/* AK & Sons · site behaviour: before/during/after slider, work filter, photo rail, quote tab and action bar, form. */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- before / during / after on the aligned hallway photographs ---- */
  [].forEach.call(document.querySelectorAll('[data-ba]'), function (ba) {
    var range = ba.querySelector('.ba__range'), a = ba.querySelector('.ba__a'), tag = ba.querySelector('[data-ba-tag]');
    var scope = ba.closest('section') || document;
    var btns = [].slice.call(scope.querySelectorAll('[data-stage]'));
    var showing = 'before';
    var set = function (v, anim) {
      if (anim && !reduce) { ba.classList.add('is-anim'); clearTimeout(ba._t); ba._t = setTimeout(function () { ba.classList.remove('is-anim'); }, 380); }
      ba.style.setProperty('--pos', v + '%'); range.value = v;
    };
    var swap = function (which) {
      if (showing === which) return;
      showing = which; a.srcset = ba.getAttribute('data-srcset-' + which);
      tag.textContent = which === 'during' ? 'During' : 'Before';
      a.alt = which === 'during' ? 'During: understairs panelling fitted and the pull-out shoe rack open, before the new spindles' : 'Before: the hallway with the open understairs and the old staircase, Worksop';
    };
    var press = function (s) { btns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-stage') === s)); }); };
    range.addEventListener('input', function () { set(range.value, false); press(''); });
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var s = b.getAttribute('data-stage');
        if (s === 'after') set(0, true); else { swap(s); set(100, true); }
        press(s);
      });
    });
  });

  /* ---- /work/ filter ---- */
  var filters = document.querySelector('[data-filters]'), grid = document.querySelector('[data-grid]');
  if (filters && grid) {
    var cards = [].slice.call(grid.querySelectorAll('.card'));
    var apply = function (f, push) {
      [].forEach.call(filters.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-filter') === f)); });
      cards.forEach(function (c) { c.hidden = !(f === 'all' || (' ' + c.getAttribute('data-cats') + ' ').indexOf(' ' + f + ' ') >= 0); });
      grid.classList.toggle('is-filtered', f !== 'all');
      if (push && history.replaceState) history.replaceState(null, '', f === 'all' ? location.pathname : '?type=' + f);
    };
    filters.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) apply(b.getAttribute('data-filter'), true); });
    var q = new URLSearchParams(location.search).get('type');
    if (q && filters.querySelector('[data-filter="' + q + '"]')) apply(q, false);
  }

  /* ---- project photo rail ---- */
  var rail = document.querySelector('[data-rail]');
  if (rail) {
    var step = function (d) { var first = rail.querySelector('a'); var w = first ? first.getBoundingClientRect().width + 16 : 400; rail.scrollBy({ left: d * w, behavior: reduce ? 'auto' : 'smooth' }); };
    var p = document.querySelector('[data-rail-prev]'), n = document.querySelector('[data-rail-next]');
    p && p.addEventListener('click', function () { step(-1); });
    n && n.addEventListener('click', function () { step(1); });
  }

  /* ---- quote tab (desktop) and action bar (phone): after the first screen, gone at the form ---- */
  var qtab = document.querySelector('[data-qtab]'), bar = document.querySelector('[data-actbar]');
  var hero = document.querySelector('[data-hero]'), quote = document.querySelector('[data-quote]');
  var pastHero = !hero, atQuote = false;
  var paint = function () {
    var on = pastHero && !atQuote;
    qtab && qtab.classList.toggle('is-off', !on);
    bar && bar.classList.toggle('is-on', on);
  };
  if ('IntersectionObserver' in window) {
    if (hero) new IntersectionObserver(function (es) { pastHero = !es[0].isIntersecting; paint(); }, { rootMargin: '-40% 0px 0px 0px' }).observe(hero);
    if (quote) new IntersectionObserver(function (es) { atQuote = es[0].isIntersecting; paint(); }, { rootMargin: '0px 0px -30% 0px' }).observe(quote);
  }
  if (!hero) { var y0 = function () { pastHero = scrollY > innerHeight * .4 || document.documentElement.scrollHeight < innerHeight * 1.6; paint(); }; addEventListener('scroll', y0, { passive: true }); y0(); }
  paint();

  /* ---- pocket door clip: still under reduced motion ---- */
  [].forEach.call(document.querySelectorAll('video[autoplay]'), function (v) { if (reduce) { v.removeAttribute('autoplay'); v.pause(); v.controls = true; } });

  /* ---- enquiry form: fold extras on the phone, check before sending, return to our thank-you page ---- */
  [].forEach.call(document.querySelectorAll('[data-form]'), function (f) {
    var next = f.querySelector('[data-next]'); if (next && /^https?:/.test(location.origin)) next.value = location.origin + '/thanks/';
    var fold = f.querySelector('[data-fold]'); if (fold && matchMedia('(max-width: 759px)').matches) fold.open = false;
    var msg = function (el, t) { var fd = el.closest('.field'); if (!fd) return; fd.setAttribute('data-state', t ? 'error' : ''); var m = fd.querySelector('.msg'); if (m) m.textContent = t || ''; };
    var check = function (el) {
      var v = (el.value || '').trim(), t = '';
      if (el.required && !v) t = el.name === 'name' ? 'Please add your name.' : el.name === 'email' ? 'Please add your email address so we can reply.' : 'A few words about the job, please.';
      else if (el.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) t = 'Please check the email address.';
      else if (el.type === 'file' && el.files && el.files[0] && el.files[0].size > 5 * 1024 * 1024) t = 'That photo is over 5 MB. Please pick a smaller one or email it to us.';
      msg(el, t); return !t;
    };
    [].forEach.call(f.querySelectorAll('input, textarea'), function (el) {
      el.addEventListener('blur', function () { if (el.value) check(el); });
      el.addEventListener('input', function () { if (el.closest('.field') && el.closest('.field').getAttribute('data-state') === 'error') check(el); });
      el.addEventListener('change', function () { if (el.type === 'file') check(el); });
    });
    f.addEventListener('submit', function (e) {
      var ok = true, first = null;
      [].forEach.call(f.querySelectorAll('input:not([type=hidden]):not(.hp), textarea'), function (el) { if (!check(el)) { ok = false; if (!first) first = el; } });
      if (!ok) { e.preventDefault(); if (fold && first && fold.contains(first)) fold.open = true; first && first.focus(); return; }
      var btn = f.querySelector('[type=submit]'); if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
    });
  });
})();

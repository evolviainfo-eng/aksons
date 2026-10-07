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

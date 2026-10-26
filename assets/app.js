/* Finezja – ruch strony. Każdy blok w try/catch: awaria jednego nie zatrzymuje reszty. */
(function () {
  var d = document.documentElement;
  var RM = false;
  try { RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { }
  var FINE = false;
  try { FINE = window.matchMedia('(hover: hover) and (pointer: fine)').matches; } catch (e) { }
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var vh = function () { return window.innerHeight || d.clientHeight; };
  var sy = function () { return window.pageYOffset || d.scrollTop || 0; };

  /* 1. Płynne przewijanie – tylko mysz/gładzik, telefon przewija natywnie */
  var lenis = null;
  try {
    if (!RM && FINE && window.Lenis) {
      lenis = new window.Lenis({ lerp: 0.09, wheelMultiplier: 0.95, smoothWheel: true });
      var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
      if (d.classList.contains('d-closed')) lenis.stop();
    }
  } catch (e) { lenis = null; }

  /* 2. Słowa nagłówków w maskach */
  try {
    $$('.split').forEach(function (el) {
      var n = 0, base = parseFloat(el.getAttribute('data-delay') || 0);
      var walk = function (node) {
        [].slice.call(node.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var parts = c.textContent.split(/(\s+)/), f = document.createDocumentFragment();
            parts.forEach(function (p) {
              if (!p) return;
              if (/^\s+$/.test(p)) { f.appendChild(document.createTextNode(' ')); return; }
              var o = document.createElement('span'), i = document.createElement('span');
              o.className = 'sw'; i.textContent = p; i.style.transitionDelay = (base + n * 0.055).toFixed(3) + 's'; n++;
              o.appendChild(i); f.appendChild(o);
            });
            node.replaceChild(f, c);
          } else if (c.nodeType === 1 && c.tagName !== 'BR') walk(c);
        });
      };
      walk(el);
    });
  } catch (e) { }

  /* 3. Drzwi: wejście (raz na sesję), otwarcie po każdym przejściu, zamknięcie przy kliknięciu w podstronę */
  var otworz = function () {
    if (d.classList.contains('ready')) return;
    d.classList.remove('d-closed', 'd-intro');
    setTimeout(function () { d.classList.add('ready'); try { if (lenis) lenis.start(); } catch (e) { } }, RM ? 0 : 380);
  };
  try {
    if (d.classList.contains('d-closed')) {
      var intro = d.classList.contains('d-intro');
      var start = Date.now(), MIN = intro ? 1500 : 250;
      var poczekaj = function () { setTimeout(otworz, Math.max(0, MIN - (Date.now() - start))); };
      if (document.readyState === 'complete') poczekaj(); else window.addEventListener('load', poczekaj);
      setTimeout(otworz, intro ? 3200 : 1600);
    } else otworz();
    try { sessionStorage.setItem('fz_in', '1'); sessionStorage.removeItem('fz_nav'); } catch (e) { }
    var BASE = (location.pathname.match(/^\/[^\/]+\//) || ['/'])[0];
    document.addEventListener('click', function (ev) {
      var a = ev.target.closest && ev.target.closest('a[href]');
      if (!a || RM || ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
      if (a.target && a.target !== '_self') return;
      if (a.hasAttribute('download') || a.hasAttribute('data-nodoor')) return;
      var u; try { u = new URL(a.href, location.href); } catch (e) { return; }
      if (u.origin !== location.origin || u.pathname.indexOf(BASE) !== 0) return;
      if (u.pathname === location.pathname && u.search === location.search) return;
      if (/\.(jpg|jpeg|png|webp|mp4|pdf)$/i.test(u.pathname)) return;
      ev.preventDefault();
      try { sessionStorage.setItem('fz_nav', '1'); } catch (e) { }
      d.classList.remove('menu-open');
      d.classList.add('d-leave');
      setTimeout(function () { location.href = u.href; }, 760);
    });
    window.addEventListener('pageshow', function (e) { if (e.persisted) { d.classList.remove('d-leave', 'd-closed', 'd-intro'); d.classList.add('ready'); } });
  } catch (e) { otworz(); }

  /* 4. Odsłanianie przy przewijaniu */
  try {
    var rv = $$('.fade,.reveal,.wipe,.split:not(.on-ready)');
    var pokaz = function (el) { el.classList.add('in'); };
    if ('IntersectionObserver' in window && !RM) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { pokaz(e.target); io.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -9% 0px', threshold: 0.12 });
      rv.forEach(function (el) { io.observe(el); });
      /* bezpiecznik: co jest już nad dolną krawędzią, pokaż nawet bez zdarzenia obserwatora */
      var bez = function () { rv.forEach(function (el) { if (!el.classList.contains('in') && el.getBoundingClientRect().top < vh() * 0.92) pokaz(el); }); };
      window.addEventListener('scroll', function () { requestAnimationFrame(bez); }, { passive: true });
      setTimeout(bez, 2500);
    } else rv.forEach(pokaz);
    var hs = $$('.split.on-ready');
    var gotowe = function () { hs.forEach(pokaz); };
    if (d.classList.contains('ready')) gotowe();
    else new MutationObserver(function (m, o) { if (d.classList.contains('ready')) { gotowe(); o.disconnect(); } }).observe(d, { attributes: true, attributeFilter: ['class'] });
  } catch (e) { $$('.fade,.reveal,.wipe,.split').forEach(function (el) { el.classList.add('in'); }); }

  /* 5. Pasek, przyklejony telefon, hero przy przewijaniu, proces, paralaksa */
  try {
    var head = $('.head'), sc = $('.sticky-call'), hero = $('.hero,.phead');
    var heroIn = hero && $('.hero-in', hero), heroMedia = hero && $('.hero-media', hero);
    var steps = $('.steps'), bar = steps && $('.bar', steps), stepLi = steps ? $$('li', steps) : [];
    var par = $$('[data-par]');
    var last = 0, tik = false;
    var licz = function () {
      tik = false;
      var y = sy(), h = vh();
      if (head) {
        head.classList.toggle('is-scrolled', y > 30);
        if (!d.classList.contains('menu-open')) {
          if (y > last + 4 && y > 640) head.classList.add('is-hidden');
          else if (y < last - 4 || y < 640) head.classList.remove('is-hidden');
        }
      }
      if (sc) sc.classList.toggle('on', y > (hero ? hero.offsetHeight * 0.55 : 300));
      if (!RM && hero && y < hero.offsetHeight) {
        if (heroIn) { heroIn.style.transform = 'translate3d(0,' + (y * 0.22).toFixed(1) + 'px,0)'; heroIn.style.opacity = clamp(1 - y / (h * 0.85), 0, 1).toFixed(3); }
        if (heroMedia) heroMedia.style.transform = 'translate3d(0,' + (y * 0.32).toFixed(1) + 'px,0)';
      }
      if (steps) {
        var r = steps.getBoundingClientRect(), p = clamp((h * 0.8 - r.top) / (h * 0.55), 0, 1);
        if (bar) bar.style.setProperty('--p', p.toFixed(3));
        stepLi.forEach(function (li, i) { li.classList.toggle('on', p >= i / stepLi.length + 0.02 || RM); });
      }
      if (!RM) par.forEach(function (el) {
        var r = el.getBoundingClientRect(); if (r.bottom < -200 || r.top > h + 200) return;
        var c = r.top + r.height / 2 - h / 2;
        el.style.transform = 'translate3d(0,' + (c * parseFloat(el.getAttribute('data-par'))).toFixed(1) + 'px,0)';
      });
      last = y;
    };
    var zglos = function () { if (!tik) { tik = true; requestAnimationFrame(licz); } };
    window.addEventListener('scroll', zglos, { passive: true });
    window.addEventListener('resize', zglos, { passive: true });
    licz();
  } catch (e) { }

  /* 6. Menu na telefonie */
  try {
    var bg = $('.burger');
    if (bg) {
      bg.addEventListener('click', function () {
        var on = !d.classList.contains('menu-open');
        d.classList.toggle('menu-open', on); bg.setAttribute('aria-expanded', on ? 'true' : 'false');
        try { if (lenis) { if (on) lenis.stop(); else lenis.start(); } } catch (e) { }
        $$('.mnav>ul>li>a').forEach(function (a, i) { a.style.transitionDelay = on ? (0.25 + i * 0.05) + 's' : '0s'; });
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && d.classList.contains('menu-open')) bg.click(); });
    }
  } catch (e) { }

  /* 7. Liczniki */
  try {
    var cs = $$('[data-count]');
    var fmt = function (v) { return String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };
    var run = function (el) {
      var to = parseFloat(el.getAttribute('data-count')), dec = (el.getAttribute('data-count').split(/[.,]/)[1] || '').length;
      if (RM) { el.textContent = dec ? to.toFixed(dec).replace('.', ',') : fmt(to); return; }
      var t0 = null, dur = 1700;
      var k = function (t) {
        if (!t0) t0 = t; var p = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - p, 4), v = to * e;
        el.textContent = dec ? v.toFixed(dec).replace('.', ',') : fmt(Math.round(v));
        if (p < 1) requestAnimationFrame(k);
      };
      requestAnimationFrame(k);
    };
    if ('IntersectionObserver' in window) {
      var cio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { run(e.target); cio.unobserve(e.target); } }); }, { threshold: 0.6 });
      cs.forEach(function (el) { el.textContent = '0'; cio.observe(el); });
    }
  } catch (e) { }

  /* 8. Jak wygląda sala – zdjęcie zmienia się razem z grupą wierszy */
  try {
    var sm = $('.spec-media');
    if (sm && 'IntersectionObserver' in window) {
      var imgs = $$('img', sm), cap = $('.cap', sm);
      var sio = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          var i = parseInt(e.target.getAttribute('data-i'), 10);
          imgs.forEach(function (im, j) { im.classList.toggle('on', j === i); });
          if (cap) cap.textContent = imgs[i] ? imgs[i].alt : '';
        });
      }, { rootMargin: '-42% 0px -42% 0px' });
      $$('.spec-grp').forEach(function (g) { sio.observe(g); });
    }
  } catch (e) { }

  /* 9. Okazje – zdjęcie płynie za kursorem */
  try {
    var occ = $('.occ'), fp = $('.float-ph');
    if (occ && fp && FINE && !RM) {
      var fi = $$('img', fp), tx = 0, ty = 0, cx = 0, cy = 0, run2 = false;
      var lerp = function () {
        cx += (tx - cx) * 0.14; cy += (ty - cy) * 0.14;
        fp.style.left = cx.toFixed(1) + 'px'; fp.style.top = cy.toFixed(1) + 'px';
        if (Math.abs(tx - cx) > 0.3 || Math.abs(ty - cy) > 0.3) requestAnimationFrame(lerp); else run2 = false;
      };
      occ.addEventListener('mousemove', function (e) { tx = e.clientX + 170; ty = e.clientY; if (!run2) { run2 = true; requestAnimationFrame(lerp); } });
      $$('li', occ).forEach(function (li, i) {
        li.addEventListener('mouseenter', function (e) {
          if (!fp.classList.contains('on')) { cx = tx = e.clientX + 170; cy = ty = e.clientY; }
          fi.forEach(function (im, j) { im.classList.toggle('on', j === i); }); fp.classList.add('on');
        });
      });
      occ.addEventListener('mouseleave', function () { fp.classList.remove('on'); });
      window.addEventListener('scroll', function () { fp.classList.remove('on'); }, { passive: true });
    }
  } catch (e) { }

  /* 10. Opinie – przewijanie przyciskami */
  try {
    $$('[data-track]').forEach(function (b) {
      var tr = document.getElementById(b.getAttribute('data-track'));
      b.addEventListener('click', function () {
        var c = tr.querySelector('.rev'); var w = c ? c.offsetWidth + 22 : 400;
        tr.scrollBy({ left: (b.getAttribute('data-dir') === 'prev' ? -1 : 1) * w, behavior: RM ? 'auto' : 'smooth' });
      });
    });
  } catch (e) { }

  /* 11. FAQ – płynne rozwijanie */
  try {
    $$('.faq details').forEach(function (dt) {
      var s = $('summary', dt), a = $('.ans', dt);
      s.addEventListener('click', function (e) {
        if (RM || !a.animate) return;
        e.preventDefault();
        if (dt.open) {
          var h = a.offsetHeight;
          a.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 420, easing: 'cubic-bezier(.2,.75,.15,1)' }).onfinish = function () { dt.open = false; };
        } else {
          dt.open = true; var h2 = a.offsetHeight;
          a.animate([{ height: '0px', opacity: 0 }, { height: h2 + 'px', opacity: 1 }], { duration: 520, easing: 'cubic-bezier(.2,.75,.15,1)' });
        }
      });
    });
  } catch (e) { }

  /* 12. Galeria: filtry i podgląd z powiększeniem od miniatury */
  try {
    var gal = $('.gal');
    if (gal) {
      $$('.gal-filter button').forEach(function (b) {
        b.addEventListener('click', function () {
          var f = b.getAttribute('data-f');
          $$('.gal-filter button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          $$('a', gal).forEach(function (a) { a.classList.toggle('hide', f !== '*' && a.getAttribute('data-c') !== f); });
        });
      });
    }
    var lb = $('.lb');
    if (lb) {
      var lim = $('img', lb), cnt = $('.cnt', lb), list = [], idx = 0, srcEl = null;
      var vis = function () { return $$('a[data-full]').filter(function (a) { return !a.classList.contains('hide'); }); };
      var show = function (i, from) {
        list = vis(); idx = (i + list.length) % list.length; var a = list[idx];
        lim.src = a.getAttribute('data-full'); lim.alt = (a.querySelector('img') || {}).alt || '';
        cnt.textContent = (idx + 1) + ' / ' + list.length;
        if (from && !RM && lim.animate) {
          var go = function () {
            var t = from.getBoundingClientRect(), r = lim.getBoundingClientRect(); if (!r.width) return;
            lim.animate([{ transform: 'translate(' + (t.left + t.width / 2 - r.left - r.width / 2) + 'px,' + (t.top + t.height / 2 - r.top - r.height / 2) + 'px) scale(' + (t.width / r.width) + ')', opacity: .5 }, { transform: 'none', opacity: 1 }], { duration: 650, easing: 'cubic-bezier(.2,.75,.15,1)' });
          };
          if (lim.complete) go(); else lim.onload = function () { lim.onload = null; go(); };
        }
      };
      $$('a[data-full]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          e.preventDefault(); srcEl = a.querySelector('img'); lb.classList.add('on'); show(vis().indexOf(a), srcEl);
          try { if (lenis) lenis.stop(); } catch (er) { }
        });
      });
      var zamknij = function () { lb.classList.remove('on'); lim.removeAttribute('src'); try { if (lenis) lenis.start(); } catch (er) { } };
      $('.x', lb).addEventListener('click', zamknij);
      $('.pv', lb).addEventListener('click', function () { show(idx - 1); });
      $('.nx', lb).addEventListener('click', function () { show(idx + 1); });
      lb.addEventListener('click', function (e) { if (e.target === lb) zamknij(); });
      document.addEventListener('keydown', function (e) {
        if (!lb.classList.contains('on')) return;
        if (e.key === 'Escape') zamknij(); if (e.key === 'ArrowLeft') show(idx - 1); if (e.key === 'ArrowRight') show(idx + 1);
      });
      var x0 = null;
      lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      lb.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); x0 = null; });
    }
  } catch (e) { }

  /* 13. Mapa (Leaflet, kafle OSM w szarości) – ładowana dopiero przy zbliżeniu */
  try {
    var mp = $('.map');
    if (mp && 'IntersectionObserver' in window) {
      var load = function () {
        var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'; document.head.appendChild(l);
        var s = document.createElement('script'); s.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        s.onload = function () {
          var lat = parseFloat(mp.getAttribute('data-lat')), lng = parseFloat(mp.getAttribute('data-lng'));
          var m = window.L.map(mp, { scrollWheelZoom: false, zoomControl: true, attributionControl: true }).setView([lat, lng], 13);
          window.L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap' }).addTo(m);
          window.L.marker([lat, lng], { icon: window.L.divIcon({ className: '', html: '<div class="pin"></div>', iconSize: [22, 22], iconAnchor: [11, 11] }) }).addTo(m).bindPopup('<b>Finezja – sala bankietowa</b><br>Kaczki Średnie 10c, 62-700 Turek');
          var fb = $('.map-fallback', mp); if (fb) fb.remove();
        };
        document.head.appendChild(s);
      };
      var mio = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { load(); mio.disconnect(); } }, { rootMargin: '400px' });
      mio.observe(mp);
    }
  } catch (e) { }

  /* 14. Wideo w hero gra tylko, gdy je widać */
  try {
    $$('video[data-auto]').forEach(function (v) {
      if (RM) { v.removeAttribute('autoplay'); v.pause(); return; }
      var p = function () { var x = v.play(); if (x && x.catch) x.catch(function () { }); };
      if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { if (es[0].isIntersecting) p(); else v.pause(); }).observe(v);
      else p();
    });
  } catch (e) { }

  /* 15. Formularz – składa wiadomość e-mail z pól */
  try {
    var fm = $('form.form');
    if (fm) fm.addEventListener('submit', function (e) {
      e.preventDefault();
      var g = function (n) { var el = fm.elements[n]; return el ? String(el.value || '').trim() : ''; };
      var body = 'Imię i nazwisko: ' + g('imie') + '\nTelefon: ' + g('tel') + '\nE-mail: ' + g('email') + '\nRodzaj przyjęcia: ' + g('rodzaj') + '\nTermin: ' + g('data') + '\nLiczba gości: ' + g('goscie') + '\n\n' + g('wiad');
      location.href = 'mailto:biuro@finezja.org?subject=' + encodeURIComponent('Zapytanie: ' + (g('rodzaj') || 'przyjęcie') + (g('data') ? ' – ' + g('data') : '')) + '&body=' + encodeURIComponent(body);
    });
  } catch (e) { }

  /* 16. Kotwice przez Lenis */
  try {
    if (lenis) $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href'); if (id.length < 2) return; var t = document.querySelector(id); if (!t) return;
        e.preventDefault(); lenis.scrollTo(t, { offset: -70, duration: 1.4 });
      });
    });
  } catch (e) { }
})();

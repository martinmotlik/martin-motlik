/* Cookie consent, shared by every page (styles: /assets/consent.css).
 *
 * The only optional tracking is Google Analytics 4. Each page's <head> sets
 * Consent Mode defaults (everything denied) and loads GA only if a valid
 * "yes" is already stored; this file shows the banner when there is no
 * choice yet, the settings dialog ([data-consent-open], e.g. "Cookie
 * settings" in the footer), and applies a new choice:
 *   accept  → analytics_storage granted, gtag.js loaded, page view sent
 *   reject  → analytics_storage denied, existing _ga cookies removed
 * The choice is kept in localStorage "mm-consent" {analytics, v, ts}; the
 * banner returns after 12 months or when VERSION changes (keep VERSION and
 * the age in step with the snippet in each page's <head>).
 */
(function () {
  var GA = 'G-LL09W3RK8L', KEY = 'mm-consent', VERSION = 1, MAX_AGE = 365 * 864e5;
  var COPY = {
    en: {
      title: 'Cookies & analytics',
      text: 'I use Google Analytics to see which pages are useful. It sets cookies only if you agree, and the site works the same either way.',
      reject: 'Reject', accept: 'Accept', settings: 'Settings', privacy: 'Privacy',
      dTitle: 'Cookie settings', close: 'Close',
      nec: 'Necessary', always: 'Always on',
      necText: 'Remembers your cookie choice and where you left off in a podcast episode. Stored only in your browser and never sent anywhere.',
      ana: 'Analytics',
      anaText: 'Google Analytics 4 (Google Ireland Limited) counts visits and page views so I can improve the content.',
      anaMeta: 'Cookies: _ga, _ga_LL09W3RK8L · stored for up to 2 years · data may be processed in the USA under the EU–US Data Privacy Framework.',
      save: 'Save choices', rejectAll: 'Reject all', acceptAll: 'Accept all', policy: 'Privacy policy',
      url: '/privacy/'
    },
    cs: {
      title: 'Cookies a analytika',
      text: 'Používám Google Analytics, abych viděl, které stránky jsou užitečné. Cookies se uloží jen s vaším souhlasem a web funguje stejně i bez nich.',
      reject: 'Odmítnout', accept: 'Přijmout', settings: 'Nastavení', privacy: 'Ochrana osobních údajů',
      dTitle: 'Nastavení cookies', close: 'Zavřít',
      nec: 'Nezbytné', always: 'Vždy aktivní',
      necText: 'Uchovává vaši volbu cookies a místo, kde jste v dílu podcastu skončili. Ukládá se jen ve vašem prohlížeči a nikam se neodesílá.',
      ana: 'Analytika',
      anaText: 'Google Analytics 4 (Google Ireland Limited) měří návštěvy a zobrazené stránky, abych mohl obsah zlepšovat.',
      anaMeta: 'Cookies: _ga, _ga_LL09W3RK8L · platnost až 2 roky · data mohou být zpracována v USA na základě EU–US Data Privacy Framework.',
      save: 'Uložit volbu', rejectAll: 'Odmítnout vše', acceptAll: 'Přijmout vše', policy: 'Ochrana osobních údajů',
      url: '/cs/ochrana-osobnich-udaju/'
    },
    de: {
      title: 'Cookies und Analyse',
      text: 'Ich nutze Google Analytics, um zu sehen, welche Seiten hilfreich sind. Cookies werden nur mit Ihrer Einwilligung gesetzt; die Website funktioniert auch ohne sie genauso.',
      reject: 'Ablehnen', accept: 'Akzeptieren', settings: 'Einstellungen', privacy: 'Datenschutz',
      dTitle: 'Cookie-Einstellungen', close: 'Schließen',
      nec: 'Notwendig', always: 'Immer aktiv',
      necText: 'Speichert Ihre Cookie-Auswahl und die Stelle, an der Sie in einer Podcast-Folge aufgehört haben. Die Daten bleiben in Ihrem Browser und werden nicht übertragen.',
      ana: 'Analyse',
      anaText: 'Google Analytics 4 (Google Ireland Limited) misst Besuche und Seitenaufrufe, damit ich die Inhalte verbessern kann.',
      anaMeta: 'Cookies: _ga, _ga_LL09W3RK8L · Speicherdauer bis zu 2 Jahre · Daten können auf Grundlage des EU-US Data Privacy Framework in den USA verarbeitet werden.',
      save: 'Auswahl speichern', rejectAll: 'Alle ablehnen', acceptAll: 'Alle akzeptieren', policy: 'Datenschutzerklärung',
      url: '/de/datenschutz/'
    }
  };
  var t = COPY[(document.documentElement.lang || 'en').slice(0, 2)] || COPY.en;
  var root = document.documentElement;
  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== 'function') window.gtag = function () { window.dataLayer.push(arguments); };

  // ── Stored choice
  function read() {
    try {
      var c = JSON.parse(localStorage.getItem(KEY));
      if (c && c.v === VERSION && Date.now() - c.ts < MAX_AGE) return c;
    } catch (e) {}
    return null;
  }
  function store(analytics) {
    try { localStorage.setItem(KEY, JSON.stringify({ analytics: !!analytics, v: VERSION, ts: Date.now() })); } catch (e) {}
  }

  // ── Google Analytics
  function grant() {
    gtag('consent', 'update', { analytics_storage: 'granted' });
    if (!window.mmGa) { window.mmGa = true; gtag('js', new Date()); gtag('config', GA); }
    if (!document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
      var s = document.createElement('script');
      s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA;
      document.head.appendChild(s);
    }
  }
  function revoke() {
    gtag('consent', 'update', { analytics_storage: 'denied' });
    var host = location.hostname, domains = ['', host, '.' + host, '.' + host.replace(/^www\./, '')];
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (!/^_ga(_|$)/.test(name)) return;
      domains.forEach(function (d) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (d ? '; domain=' + d : '');
      });
    });
  }
  function decide(analytics) {
    var before = read();
    store(analytics);
    if (analytics) grant(); else if (before && before.analytics || document.cookie.indexOf('_ga') > -1) revoke(); else gtag('consent', 'update', { analytics_storage: 'denied' });
    hideBanner();
  }

  function el(tag, attrs, html) {
    var n = document.createElement(tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  // ── Layer 1: banner (not modal; first in the tab order)
  var banner = null;
  function showBanner() {
    banner = el('div', { 'class': 'cc-banner', role: 'region', 'aria-label': t.title },
      '<p><strong>' + esc(t.title) + '.</strong> ' + esc(t.text) + '</p>' +
      '<div class="cc-choice">' +
        '<button type="button" class="cc-btn cc-btn-tint" data-cc="reject">' + esc(t.reject) + '</button>' +
        '<button type="button" class="cc-btn cc-btn-tint" data-cc="accept">' + esc(t.accept) + '</button>' +
      '</div>' +
      '<div class="cc-links">' +
        '<button type="button" class="cc-link" data-cc="settings">' + esc(t.settings) + '</button>' +
        '<a class="cc-link" href="' + t.url + '">' + esc(t.privacy) + '</a>' +
      '</div>');
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cc]');
      if (!b) return;
      var a = b.getAttribute('data-cc');
      if (a === 'accept') decide(true);
      else if (a === 'reject') decide(false);
      else openDialog(b);
    });
    document.body.insertBefore(banner, document.body.firstChild);
    root.classList.add('cc-pending');
    setTimeout(function () { if (banner) banner.classList.add('is-in'); }, 600);
  }
  // Focus must not vanish with the banner: it moves to the start of the page.
  function home() { return document.querySelector('.nav-logo') || document.body; }
  function hideBanner() {
    root.classList.remove('cc-pending');
    if (!banner) return;
    var b = banner; banner = null;
    if (b.contains(document.activeElement)) home().focus({ preventScroll: true });
    b.classList.remove('is-in'); b.classList.add('is-out');
    setTimeout(function () { b.remove(); }, 320);
  }

  // ── Layer 2: settings dialog
  var wrap = null, opener = null;
  function openDialog(from) {
    if (wrap) return;
    opener = from || document.activeElement;
    var current = read(), on = !!(current && current.analytics);
    wrap = el('div', { 'class': 'cc-wrap' },
      '<div class="cc-backdrop" data-cc="close"></div>' +
      '<div class="cc-dialog" role="dialog" aria-modal="true" aria-labelledby="cc-title">' +
        '<div class="cc-head"><h2 class="cc-title" id="cc-title">' + esc(t.dTitle) + '</h2>' +
          '<button type="button" class="cc-x" data-cc="close" aria-label="' + esc(t.close) + '">✕</button></div>' +
        '<div class="cc-cats">' +
          '<div class="cc-cat"><div class="cc-cat-txt"><p class="cc-cat-name" id="cc-nec">' + esc(t.nec) + '</p>' +
            '<p class="cc-cat-desc">' + esc(t.necText) + '</p></div>' +
            '<div class="cc-always"><span class="cc-always-l">' + esc(t.always) + '</span>' +
            '<span class="cc-locked" role="switch" aria-checked="true" aria-disabled="true" aria-labelledby="cc-nec"><span class="cc-track"><span class="cc-knob"></span></span></span></div></div>' +
          '<div class="cc-cat"><div class="cc-cat-txt"><p class="cc-cat-name" id="cc-ana">' + esc(t.ana) + '</p>' +
            '<p class="cc-cat-desc">' + esc(t.anaText) + '</p><p class="cc-cat-meta">' + esc(t.anaMeta) + '</p></div>' +
            '<button type="button" class="cc-switch" role="switch" aria-checked="' + on + '" aria-labelledby="cc-ana" data-cc="toggle">' +
            '<span class="cc-track"><span class="cc-knob"></span></span></button></div>' +
        '</div>' +
        '<div class="cc-actions">' +
          '<button type="button" class="cc-btn cc-btn-soft" data-cc="reject">' + esc(t.rejectAll) + '</button>' +
          '<button type="button" class="cc-btn cc-btn-soft" data-cc="accept">' + esc(t.acceptAll) + '</button>' +
          '<button type="button" class="cc-btn cc-btn-primary" data-cc="save">' + esc(t.save) + '</button>' +
        '</div>' +
        '<a class="cc-link cc-policy" href="' + t.url + '">' + esc(t.policy) + '</a>' +
      '</div>');
    var sw = wrap.querySelector('.cc-switch');
    wrap.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cc]');
      if (!b) return;
      var a = b.getAttribute('data-cc');
      if (a === 'toggle') sw.setAttribute('aria-checked', String(sw.getAttribute('aria-checked') !== 'true'));
      else if (a === 'close') closeDialog();
      else { decide(a === 'accept' ? true : a === 'reject' ? false : sw.getAttribute('aria-checked') === 'true'); closeDialog(); }
    });
    wrap.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); closeDialog(); return; }
      if (e.key !== 'Tab') return;                       // focus stays in the dialog
      var f = [].slice.call(wrap.querySelectorAll('button, a[href]'));
      var i = f.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
    });
    document.body.appendChild(wrap);
    behind(true);
    requestAnimationFrame(function () { requestAnimationFrame(function () { if (wrap) wrap.classList.add('is-in'); }); });
    setTimeout(function () { if (wrap) sw.focus({ preventScroll: true }); }, 60);
  }
  function closeDialog() {
    if (!wrap) return;
    var w = wrap; wrap = null;
    w.classList.remove('is-in'); w.classList.add('is-out');
    behind(false);
    setTimeout(function () { w.remove(); }, 320);
    var back = opener && document.contains(opener) && !opener.closest('.cc-banner.is-out') ? opener : home();
    if (back) back.focus({ preventScroll: true });
    opener = null;
  }
  function behind(on) {                                  // the page under the dialog is out of reach
    [].forEach.call(document.body.children, function (n) {
      if (n === wrap || /^(SCRIPT|STYLE|TEMPLATE)$/.test(n.tagName)) return;
      if ('inert' in n) n.inert = on;
    });
  }

  // "Cookie settings" anywhere on the page (footer, privacy policy)
  document.addEventListener('click', function (e) {
    var o = e.target.closest('[data-consent-open]');
    if (o) { e.preventDefault(); openDialog(o); }
  });

  if (!read()) showBanner();
})();

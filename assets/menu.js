/* Mobile menu, shared by every page (styles: /assets/menu.css).
 *
 *   #nav-hamburger   the button; aria-label is the "open" label, data-close-label
 *                    the "close" one (both translated by tools/build-i18n.py)
 *   #nav-drawer      the sheet with the links and the language switch
 *
 * Open: the sheet fades in, the page behind it is inert (no tabbing into it)
 * and does not scroll. Closes on a link, on Escape, on the button, and when the
 * window grows to the page's full navigation (the button disappears). */
(function () {
  var btn = document.getElementById('nav-hamburger'), menu = document.getElementById('nav-drawer');
  if (!btn || !menu) return;
  var root = document.documentElement, nav = btn.closest('nav') || btn.parentNode;
  var openLabel = btn.getAttribute('aria-label') || 'Open menu', closeLabel = btn.getAttribute('data-close-label') || 'Close menu';
  var isOpen = false;

  function behind(on) {                                   // everything except the header and the sheet
    [].forEach.call(document.body.children, function (el) {
      if (el === nav || el === menu || el.contains(nav) || /^(SCRIPT|STYLE|TEMPLATE)$/.test(el.tagName)) return;
      if ('inert' in el) el.inert = on;
    });
  }
  function set(open, focusButton) {
    if (open === isOpen) return;
    isOpen = open;
    // The links line up with the logo, whatever gutter this page's header uses
    var logo = nav.querySelector('.nav-logo');
    if (open && logo) menu.style.setProperty('--nd-x', Math.round(logo.getBoundingClientRect().left) + 'px');
    menu.classList.toggle('open', open);
    root.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? closeLabel : openLabel);
    if ('inert' in menu) menu.inert = !open;
    behind(open);
    if (open) { var first = menu.querySelector('a'); if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 60); }
    else if (focusButton) btn.focus({ preventScroll: true });
  }

  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('aria-controls', 'nav-drawer');
  if ('inert' in menu) menu.inert = true;
  btn.addEventListener('click', function () { set(!isOpen); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', function (e) {
    if (!isOpen) return;
    if (e.key === 'Escape') { e.preventDefault(); set(false, true); return; }
    if (e.key !== 'Tab') return;                          // keep Tab inside the button + the sheet
    var items = [btn].concat([].slice.call(menu.querySelectorAll('a, button')));
    var i = items.indexOf(document.activeElement);
    if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
    else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
  });
  // Each page switches to the full navigation at its own width: close the
  // menu once the button is gone.
  window.addEventListener('resize', function () {
    if (isOpen && getComputedStyle(btn).display === 'none') set(false);
  }, { passive: true });
})();

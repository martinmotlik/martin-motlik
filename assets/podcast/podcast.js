/* Podcast player, shared by the article pages and /insights/podcast/.
 *
 * One <audio> for the page. Episode data comes from <script id="pod-data">
 * (tools/build-podcast.py); labels from #i18n-ui on Czech / German pages,
 * English otherwise. Everything it drives is optional and found by data
 * attributes, so each page only carries the parts its design has:
 *
 *   [data-pod-toggle]          play / pause; [data-pod-label] inside gets the state label
 *   [data-pod-seek="s"]        play from s seconds (chapters, chips, transcript lines)
 *   [data-pod-chip]            chapter chip next to an H2 (active while its chapter plays)
 *   [data-pod-chapter="i"]     chapter row (active / past)
 *   [data-pod-line="i"]        transcript line (active by playback time)
 *   [data-pod-wave="n"]        waveform of n bars (default 72), click to seek
 *   [data-pod-time]            m:ss now        [data-pod-progress]  width = progress
 *   [data-pod-chapter-title]   current chapter [data-pod-chapter-line] "Chapter n of N · …"
 *   [data-pod-rate]            speed 1× → 1.25× → 1.5× → 2× → 0.75×
 *   [data-pod-transcript]      transcript accordion button
 *   #pod-mini                  floating mini player
 *
 * The position is kept per episode in localStorage, so "Resume" works across
 * pages. Other scripts use window.Podcast (audio, toggle, play, seek, now, on).
 */
(function () {
  var dataEl = document.getElementById('pod-data');
  if (!dataEl) return;
  var EP = JSON.parse(dataEl.textContent);
  var EN = {
    play_episode: 'Play episode', pause: 'Pause', resume: 'Resume', play_latest: 'Play latest episode',
    resume_latest: 'Resume episode', chip_at: 'Discussed at', chip_playing: 'Playing',
    now_playing: 'Now playing', paused: 'Paused', chapter_of: 'Chapter {n} of {total}',
    starts_with: '{total} chapters · Starts with: {title}', rate: 'Playback speed'
  };
  var ui = {};
  try { ui = JSON.parse(document.getElementById('i18n-ui').textContent); } catch (e) {}
  function t(k, vars) {
    var s = ui[k] != null ? ui[k] : EN[k];
    Object.keys(vars || {}).forEach(function (v) { s = s.replace('{' + v + '}', vars[v]); });
    return s;
  }
  function fmt(s) { s = isFinite(s) ? Math.max(0, s) : 0; return Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0'); }
  var $$ = function (sel) { return [].slice.call(document.querySelectorAll(sel)); };

  var audio = new Audio();
  audio.preload = 'metadata';
  audio.src = EP.audio;
  var KEY = 'pod:' + EP.id, RATES = [1, 1.25, 1.5, 2, 0.75], rateIdx = 0;
  var started = false, dismissed = false, pending = null, listeners = [];
  var DUR = EP.duration;

  // Where the listener left off (never fatal: storage can be blocked)
  var saved = 0;
  try { saved = +localStorage.getItem(KEY) || 0; } catch (e) {}
  if (saved > 5 && saved < DUR - 5) { pending = saved; started = true; dismissed = true; }
  function remember() {
    try { audio.currentTime > 5 && audio.currentTime < DUR - 5 ? localStorage.setItem(KEY, audio.currentTime.toFixed(1)) : localStorage.removeItem(KEY); } catch (e) {}
  }

  function now() { return pending != null ? pending : (audio.currentTime || 0); }
  function playing() { return !audio.paused && !audio.ended; }
  function chapterIndex(time) {
    var i = 0; EP.chapters.forEach(function (c, k) { if (time >= c[0]) i = k; }); return i;
  }

  function play() {
    started = true; dismissed = false;
    audio.playbackRate = RATES[rateIdx];
    if (pending != null && audio.readyState >= 1) { audio.currentTime = pending; pending = null; }
    audio.play().catch(function () { render(); });
    emit('start');
  }
  function pause() { audio.pause(); }
  function toggle() { playing() ? pause() : play(); }
  function seek(s, andPlay) {
    s = Math.max(0, Math.min(DUR - 1, s));
    if (audio.readyState >= 1) { audio.currentTime = s; pending = null; } else pending = s;
    started = true;
    if (andPlay !== false && !playing()) play(); else render();
  }
  function stop() {
    audio.pause(); audio.currentTime = 0; pending = null; started = false; dismissed = true;
    try { localStorage.removeItem(KEY); } catch (e) {}
    render(); emit('stop');
  }
  function emit(type) { listeners.forEach(function (fn) { fn(type); }); }

  // ── Waveforms ──
  $$('[data-pod-wave]').forEach(function (w) {
    for (var i = 0, n = +w.dataset.podWave || 72; i < n; i++) {
      var b = document.createElement('i');
      b.style.height = Math.round((0.28 + 0.72 * Math.abs(Math.sin(i * 1.7) * 0.6 + Math.sin(i * 0.43) * 0.4)) * 100) + '%';
      w.appendChild(b);
    }
    w.addEventListener('click', function (e) {
      var r = w.getBoundingClientRect();
      seek(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * DUR);
    });
  });

  // ── Rendering ──
  function render() {
    var time = now(), on = playing(), pct = DUR ? time / DUR : 0, ci = chapterIndex(time);
    var resumeLabel = t('resume') + ' ' + fmt(time);
    $$('[data-pod-toggle]').forEach(function (b) {
      b.classList.toggle('is-playing', on);
      var l = b.querySelector('[data-pod-label]');
      if (l) {
        var latest = b.dataset.podToggle === 'latest';
        l.textContent = on ? t('pause') : started && time > 0 ? (latest ? t('resume_latest') + ' ' + EP.number : resumeLabel) : (latest ? t('play_latest') : t('play_episode'));
      }
      if (!l) b.setAttribute('aria-label', on ? t('pause') : t('play_episode'));
    });
    $$('[data-pod-time]').forEach(function (e) { e.textContent = fmt(time); });
    $$('[data-pod-progress]').forEach(function (e) { e.style.width = (pct * 100) + '%'; });
    $$('[data-pod-chapter-title]').forEach(function (e) { e.textContent = EP.chapters[ci][1]; });
    $$('[data-pod-chapter-line]').forEach(function (e) {
      e.textContent = started ? t('chapter_of', { n: ci + 1, total: EP.chapters.length }) + ' · ' + EP.chapters[ci][1]
                              : t('starts_with', { total: EP.chapters.length, title: EP.chapters[0][1] });
    });
    $$('[data-pod-chapter]').forEach(function (b) {
      var i = +b.dataset.podChapter;
      b.classList.toggle('is-on', started && i === ci);
      b.classList.toggle('is-past', started && i < ci);
    });
    $$('[data-pod-chip]').forEach(function (b) {
      var s = +b.dataset.podSeek, active = started && EP.chapters[ci][0] === s;
      b.classList.toggle('is-on', active);
      var l = b.querySelector('.cc-l');
      if (l) l.textContent = active && on ? t('chip_playing') + ' ·' : t('chip_at');
    });
    var li = -1;
    if (started) EP.lines.forEach(function (s, k) { if (time >= s) li = k; });
    $$('[data-pod-line]').forEach(function (b) { b.classList.toggle('is-on', +b.dataset.podLine === li); });
    $$('[data-pod-wave]').forEach(function (w) {
      var pi = Math.floor(pct * w.children.length);
      [].forEach.call(w.children, function (b, i) {
        b.className = i < pi ? 'done' : (i === pi && started ? 'at' : '');
        b.style.transform = on && Math.abs(i - pi) < 3 ? 'scaleY(1.25)' : '';
      });
    });
    $$('[data-pod-rate]').forEach(function (b) { b.textContent = RATES[rateIdx] + '×'; });
    $$('[data-pod-started]').forEach(function (e) { e.classList.toggle('is-started', started); });
    document.body.classList.toggle('pod-started', started && !dismissed);
    mini();
  }

  // ── Mini player: only once started, and only past the first screenful ──
  var miniEl = document.getElementById('pod-mini');
  function mini() {
    if (!miniEl) return;
    var show = started && !dismissed && window.scrollY > 640;
    miniEl.classList.toggle('show', show);
    miniEl.setAttribute('aria-hidden', show ? 'false' : 'true');
    if ('inert' in miniEl) miniEl.inert = !show;
    var st = miniEl.querySelector('[data-pod-status]');
    if (st) st.textContent = (playing() ? t('now_playing') : t('paused')) + ' · EP ' + String(EP.number).padStart(2, '0');
  }
  window.addEventListener('scroll', mini, { passive: true });

  // ── Controls ──
  document.addEventListener('click', function (e) {
    var el;
    if ((el = e.target.closest('[data-pod-seek]'))) { seek(+el.dataset.podSeek); return; }
    if ((el = e.target.closest('[data-pod-toggle]'))) { toggle(); return; }
    if ((el = e.target.closest('[data-pod-rate]'))) {
      rateIdx = (rateIdx + 1) % RATES.length; audio.playbackRate = RATES[rateIdx]; render(); return;
    }
    if ((el = e.target.closest('[data-pod-close]'))) { stop(); return; }
    if ((el = e.target.closest('[data-pod-transcript]'))) {
      var body = document.getElementById(el.getAttribute('aria-controls')), open = el.getAttribute('aria-expanded') !== 'true';
      el.setAttribute('aria-expanded', open); body.classList.toggle('is-open', open);
      if ('inert' in body) body.inert = !open;
    }
  });
  $$('[data-pod-transcript]').forEach(function (b) {
    var body = document.getElementById(b.getAttribute('aria-controls'));
    if (body && 'inert' in body) body.inert = true;           // folded lines are not in the tab order
  });

  ['play', 'pause', 'ended', 'timeupdate', 'ratechange', 'loadedmetadata'].forEach(function (ev) { audio.addEventListener(ev, render); });
  audio.addEventListener('loadedmetadata', function () {
    if (pending != null && playing()) { audio.currentTime = pending; pending = null; }
  });
  audio.addEventListener('pause', remember);
  audio.addEventListener('ended', function () { try { localStorage.removeItem(KEY); } catch (e) {} });
  var lastSave = 0;
  audio.addEventListener('timeupdate', function () { if (Date.now() - lastSave > 3000) { lastSave = Date.now(); remember(); } });
  window.addEventListener('pagehide', remember);

  window.Podcast = {
    audio: audio, episode: EP, toggle: toggle, play: play, pause: pause, seek: seek, stop: stop,
    on: function (fn) { listeners.push(fn); }, isStarted: function () { return started; }, now: now, rate: function () { return RATES[rateIdx]; },
    cycleRate: function () { rateIdx = (rateIdx + 1) % RATES.length; audio.playbackRate = RATES[rateIdx]; render(); }
  };
  render();
})();

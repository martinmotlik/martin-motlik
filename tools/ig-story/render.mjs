// Renders the IG story frame by frame in headless Chrome over the DevTools
// protocol: seek the composition (data-om-seek-to-time-frame, sync), wait for
// paint, capture the 1080×1920 stage as PNG. No npm packages: Node's own
// WebSocket talks to the installed Google Chrome.
// usage: node render.mjs <story.html> <out dir> <fps> <seconds> [times,comma-separated]
// The viewport is 1080 × (1920 + 45): the stage keeps 44 px for its play bar,
// so the canvas renders 1:1 and lands on whole pixels (sharp text).
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const [, , HTML, OUT, FPS = '30', SECS = '20.6', ONLY] = process.argv;
const W = 1080, H = 1920, BAR = 45, PORT = 9333;
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const profile = OUT + '/.chrome-profile';
mkdirSync(OUT, { recursive: true });

const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--mute-audio', '--force-color-profile=srgb',
  '--allow-file-access-from-files', `--window-size=${W},${H + BAR}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let targets;
for (let i = 0; i < 100; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); if (targets.some((t) => t.type === 'page')) break; } catch {}
  await sleep(100);
}
const page = targets.find((t) => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map();
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.method === 'Runtime.exceptionThrown') console.log('PAGE EXC', JSON.stringify(m.params.exceptionDetails).slice(0, 600)); if (m.method === 'Runtime.consoleAPICalled' && /error|warn/.test(m.params.type)) console.log('PAGE', m.params.type, m.params.args.map(a => a.value || a.description).join(' ').slice(0, 400)); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, (m) => m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result)); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails)); return r.result.value; };

await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H + BAR, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: pathToFileURL(HTML).href });

// wait for the stage, fonts and images
for (let i = 0; i < 150; i++) {
  const ok = await ev(`!!document.querySelector('[data-om-exportable-video-with-duration-secs]')`).catch(() => false);
  if (ok) break; await sleep(200);
}
await ev(`document.fonts.ready.then(() => Promise.all([...document.images].map(i => i.decode().catch(() => null)))).then(() => true)`);
const seek = (t) => ev(`(() => { const el = document.querySelector('[data-om-exportable-video-with-duration-secs]');
  el.dispatchEvent(new CustomEvent('data-om-seek-to-time-frame', { detail: { time: ${t}, sync: true, playing: false } }));
  return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => r(el.getBoundingClientRect().toJSON())))); })()`);
await seek(0); await sleep(500);
const info = await ev(`(() => { const el = document.querySelector('[data-om-exportable-video-with-duration-secs]'); const r = el.getBoundingClientRect();
  const img = [...document.images].map(i => i.naturalWidth + 'x' + i.naturalHeight);
  return { rect: r.toJSON(), dur: el.getAttribute('data-om-exportable-video-with-duration-secs'), img, fonts: [...document.fonts].filter(f => f.status === 'loaded').length }; })()`);
console.log(JSON.stringify(info));
const { x, y, width, height } = info.rect;
if (Math.round(width) !== W || Math.round(height) !== H) throw new Error('stage is not 1:1: ' + width + 'x' + height);

const times = ONLY ? ONLY.split(',').map(Number) : Array.from({ length: Math.round(Number(SECS) * Number(FPS)) }, (_, i) => i / Number(FPS));
let n = 0;
for (const t of times) {
  await seek(t);
  const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x, y, width: W, height: H, scale: 1 }, captureBeyondViewport: false, fromSurface: true });
  const name = ONLY ? `t${t.toFixed(2)}.png` : `f${String(n).padStart(5, '0')}.png`;
  writeFileSync(`${OUT}/${name}`, Buffer.from(shot.data, 'base64'));
  if (++n % 60 === 0) console.log('frames', n, '/', times.length);
}
console.log('done', n);
ws.close(); chrome.kill();
await sleep(300);
rmSync(profile, { recursive: true, force: true });
process.exit(0);

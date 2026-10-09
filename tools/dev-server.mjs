// Local preview server for the site, with byte ranges (206) like GitHub Pages,
// so seeking in the podcast audio works locally (python -m http.server cannot).
//
//   node tools/dev-server.mjs [root] [port]      defaults: the repo, 4174
//
// Dev only: tools/podcast-cover.html posts rendered covers to
// POST /__save/<name>; they land in Sources/exports/ (gitignored).
import { createServer } from 'node:http';
import { createReadStream, existsSync, mkdirSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(process.argv[2] || path.join(path.dirname(fileURLToPath(import.meta.url)), '..'));
const PORT = +(process.argv[3] || 4174);
const SAVE = path.join(ROOT, 'Sources', 'exports');
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8', '.md': 'text/markdown; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif',
  '.gif': 'image/gif', '.ico': 'image/x-icon', '.mp3': 'audio/mpeg', '.vtt': 'text/vtt; charset=utf-8',
  '.pdf': 'application/pdf', '.woff2': 'font/woff2',
};

createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');

  if (req.method === 'POST' && url.pathname.startsWith('/__save/')) {
    const name = path.basename(decodeURIComponent(url.pathname.slice('/__save/'.length)));
    if (!name) { res.writeHead(400).end('name missing'); return; }
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      mkdirSync(SAVE, { recursive: true });
      writeFileSync(path.join(SAVE, name), Buffer.concat(chunks));
      res.writeHead(200, { 'Content-Type': 'text/plain' }).end(path.join('Sources/exports', name));
    });
    return;
  }
  if (req.method !== 'GET' && req.method !== 'HEAD') { res.writeHead(405).end(); return; }

  let file = path.join(ROOT, decodeURIComponent(url.pathname));
  if (!file.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  if (existsSync(file) && statSync(file).isDirectory()) {
    if (!url.pathname.endsWith('/')) { res.writeHead(301, { Location: url.pathname + '/' + url.search }).end(); return; }
    file = path.join(file, 'index.html');
  }
  if (!existsSync(file)) {
    const notFound = path.join(ROOT, '404.html');
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    if (existsSync(notFound)) createReadStream(notFound).pipe(res); else res.end('Not found');
    return;
  }

  const size = statSync(file).size;
  const headers = { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
                    'Accept-Ranges': 'bytes', 'Cache-Control': 'no-cache' };
  const m = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || '');
  if (m) {
    let start = m[1] === '' ? size - +m[2] : +m[1];
    let end = m[1] === '' || m[2] === '' ? size - 1 : Math.min(+m[2], size - 1);
    if (start < 0) start = 0;
    if (start > end || start >= size) { res.writeHead(416, { 'Content-Range': `bytes */${size}` }).end(); return; }
    res.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${size}`, 'Content-Length': end - start + 1 });
    if (req.method === 'HEAD') res.end(); else createReadStream(file, { start, end }).pipe(res);
    return;
  }
  res.writeHead(200, { ...headers, 'Content-Length': size });
  if (req.method === 'HEAD') res.end(); else createReadStream(file).pipe(res);
}).listen(PORT, () => console.log(`Serving ${ROOT} on http://localhost:${PORT} (byte ranges on)`));

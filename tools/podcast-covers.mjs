// Podcast cover renditions from the 3000 px PNG masters that
// tools/podcast-cover.html draws (Sources/originals/podcast/, gitignored).
//
//   node tools/podcast-covers.mjs
//
// Show cover (tag PODCAST):  cover-3000.jpg (feed, JSON-LD), cover-1200.jpg (sharing)
// Episode covers (EP NN):    cover-epNN-3000.jpg, cover-epNN-96/144/264.{avif,jpg} (pages)
import sharp from 'sharp';
import { existsSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'Sources', 'originals', 'podcast');
const OUT = path.join(ROOT, 'assets', 'podcast');
// Large files: apps and scrapers want one plain JPEG; Apple asks for 3000 px.
const BIG = { quality: 86, progressive: true, mozjpeg: true, chromaSubsampling: '4:4:4' };
// Small page renditions: the same settings as tools/build-images.mjs.
const JPEG = { quality: 76, progressive: true, mozjpeg: true, chromaSubsampling: '4:2:0' };
const AVIF = { quality: 52, effort: 6, chromaSubsampling: '4:2:0' };

async function out(master, w, name, formats) {
  const base = sharp(master).resize(w, w, { kernel: 'lanczos3' }).flatten({ background: '#ffffff' }).withMetadata({ icc: 'srgb' });
  for (const f of formats) {
    const file = path.join(OUT, `${name}.${f}`);
    if (f === 'avif') await base.clone().avif(AVIF).toFile(file);
    else await base.clone().jpeg(w >= 1200 ? BIG : JPEG).toFile(file);
    console.log(`${path.relative(ROOT, file)}  ${(statSync(file).size / 1024).toFixed(0)} kB`);
  }
}

const show = path.join(SRC, 'cover-3000.png');
if (!existsSync(show)) throw new Error(`missing ${path.relative(ROOT, show)} (draw it with tools/podcast-cover.html)`);
await out(show, 3000, 'cover-3000', ['jpg']);
await out(show, 1200, 'cover-1200', ['jpg']);

for (const f of readdirSync(SRC).filter((f) => /^cover-ep\d+-3000\.png$/.test(f)).sort()) {
  const ep = f.replace('-3000.png', ''), master = path.join(SRC, f);
  await out(master, 3000, `${ep}-3000`, ['jpg']);
  for (const w of [96, 144, 264]) await out(master, w, `${ep}-${w}`, ['avif', 'jpg']);
}

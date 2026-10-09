// Podcast cover renditions from the 3000 px PNG masters that
// tools/podcast-cover.html draws (Sources/originals/podcast/, gitignored).
//
//   node tools/podcast-covers.mjs
//
// Output names come from podcast/podcast.json, which carries the cover version
// (apps and social networks cache artwork by URL, so a new design gets a new name):
//   show.cover        3000 px JPG (feed, JSON-LD)     master: cover-3000.png
//   show.share_image  1200 px JPG (Open Graph, X)     master: cover-3000.png
//   episode.cover     <base>-3000.jpg (feed) and <base>-96/144/264.{avif,jpg} (pages)
//                                                     master: cover-epNN-3000.png
import sharp from 'sharp';
import { existsSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'Sources', 'originals', 'podcast');
const { show, episodes } = JSON.parse(readFileSync(path.join(ROOT, 'podcast', 'podcast.json'), 'utf8'));
// Large files: apps and scrapers want one plain JPEG; Apple asks for 3000 px.
const BIG = { quality: 86, progressive: true, mozjpeg: true, chromaSubsampling: '4:4:4' };
// Small page renditions: the same settings as tools/build-images.mjs.
const JPEG = { quality: 76, progressive: true, mozjpeg: true, chromaSubsampling: '4:2:0' };
const AVIF = { quality: 52, effort: 6, chromaSubsampling: '4:2:0' };

const file = (url) => path.join(ROOT, url.replace(/^\//, ''));
function master(name) {
  const p = path.join(SRC, name);
  if (!existsSync(p)) throw new Error(`missing ${path.relative(ROOT, p)} (draw it with tools/podcast-cover.html)`);
  return p;
}
async function out(src, w, target) {
  const base = sharp(src).resize(w, w, { kernel: 'lanczos3' }).flatten({ background: '#ffffff' }).withMetadata({ icc: 'srgb' });
  if (target.endsWith('.avif')) await base.avif(AVIF).toFile(target);
  else await base.jpeg(w >= 1200 ? BIG : JPEG).toFile(target);
  console.log(`${path.relative(ROOT, target)}  ${(statSync(target).size / 1024).toFixed(0)} kB`);
}

const showMaster = master('cover-3000.png');
await out(showMaster, 3000, file(show.cover));
await out(showMaster, 1200, file(show.share_image));

for (const ep of episodes) {
  const src = master(`cover-ep${String(ep.number).padStart(2, '0')}-3000.png`);
  await out(src, 3000, file(`${ep.cover}-3000.jpg`));
  for (const w of [96, 144, 264]) for (const ext of ['avif', 'jpg']) await out(src, w, file(`${ep.cover}-${w}.${ext}`));
}

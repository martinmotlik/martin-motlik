#!/usr/bin/env node
/**
 * Prints a ready-to-paste <picture> element for an image built by
 * build-images.mjs, so srcset lists never have to be typed by hand.
 *
 *   node tools/picture.mjs <slug> --sizes "100vw" --alt "…" [options]
 *
 * Options:
 *   --sizes   <value>   sizes attribute (required)
 *   --alt     <text>    alt text ("" for decorative)
 *   --title   <text>    title attribute
 *   --class   <name>    class on the <img>
 *   --eager             omit loading="lazy" and add fetchpriority="high"
 *   --max     <px>      ignore variants wider than this
 *   --indent  <n>       leading spaces (default 0)
 */

import { readFile } from 'node:fs/promises';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const args = process.argv.slice(2);
const slug = args[0];
const flag = (name, def = null) => {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? def : args[i + 1];
};
const has = (name) => args.includes(`--${name}`);

const manifest = JSON.parse(await readFile(path.join(ROOT, 'assets/img/manifest.json'), 'utf8'));
const entry = manifest[slug];
if (!entry) {
  console.error(`Neznámý slug "${slug}". Dostupné:\n  ${Object.keys(manifest).join('\n  ')}`);
  process.exit(1);
}

const max = Number(flag('max', Infinity));
const variants = entry.widths.filter((v) => v.w <= max);
if (!variants.length) {
  console.error(`Pro --max ${max} nezbyla žádná varianta.`);
  process.exit(1);
}

const sizes = flag('sizes');
if (!sizes) {
  console.error('Chybí --sizes');
  process.exit(1);
}

const pad = ' '.repeat(Number(flag('indent', 0)));
const alt = flag('alt', '');
const title = flag('title');
const cls = flag('class');
const eager = has('eager');

// Default rendition: the middle of the ladder. Browsers that understand srcset
// never fetch it; it is only there for the handful that do not.
const fallback = variants[Math.min(variants.length - 1, Math.floor(variants.length / 2))];

const srcset = (ext, indent) =>
  variants.map((v) => `/assets/img/${slug}-${v.w}.${ext} ${v.w}w`).join(`,\n${indent}`);

const attrs = [
  `src="/assets/img/${slug}-${fallback.w}.jpg"`,
  `sizes="${sizes}"`,
].join('\n' + pad + '       ');

const out = `${pad}<picture>
${pad}  <source type="image/avif" sizes="${sizes}"
${pad}          srcset="${srcset('avif', pad + '                  ')}">
${pad}  <img ${attrs}
${pad}       srcset="${srcset('jpg', pad + '               ')}"
${pad}       alt="${alt}"${title ? `\n${pad}       title="${title}"` : ''}${cls ? `\n${pad}       class="${cls}"` : ''}
${pad}       width="${fallback.w}" height="${fallback.h}"
${pad}       ${eager ? 'fetchpriority="high" decoding="async"' : 'loading="lazy" decoding="async"'}>
${pad}</picture>`;

console.log(out);

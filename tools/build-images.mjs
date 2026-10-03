#!/usr/bin/env node
/**
 * Responsive image build.
 *
 * Reads full-resolution originals from Sources/originals/ (gitignored) and emits
 * a ladder of width variants into assets/img/ in AVIF + progressive JPEG.
 *
 * The approach mirrors apple.com: several fixed-width renditions per image,
 * compressed to roughly 1.0-1.3 bits per pixel, with the browser picking the
 * right one. Apple ships JPEG only; we add AVIF on top, which cuts another
 * ~45% for the ~94% of browsers that support it.
 *
 * Usage:  node tools/build-images.mjs [--force]
 */

import sharp from 'sharp';
import { readFile, writeFile, mkdir, stat, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const SRC = path.join(ROOT, 'Sources/originals');
const OUT = path.join(ROOT, 'assets/img');
const MANIFEST = path.join(ROOT, 'assets/img/manifest.json');
const FORCE = process.argv.includes('--force');

/**
 * Width ladders per role. Each is capped at roughly 2x the largest size the
 * image is ever displayed at, measured in the browser at a 1440px viewport.
 *
 *   hero     full-bleed background, 1440x900 at desktop
 *   card     reference card in the 4-column grid, 238x397
 *   portrait about photo, 360x480
 *   gallery  reference-page thumbnail 403x269, also opened in the lightbox
 *            at up to 92vw, so the ladder runs to 2560
 */
const ROLES = {
  hero:     [640, 960, 1280, 1920, 2560],
  card:     [320, 480, 640, 960],
  portrait: [360, 540, 720, 1080],
  // 900 sits just above the 806px a 403px thumbnail needs on a 2x screen;
  // without it the browser jumps to 1280 and fetches ~2x the bytes.
  gallery:  [400, 600, 900, 1280, 1920, 2560],
};

/** source path (relative to Sources/originals) -> role */
const IMAGES = {
  'images/hero-bg.png':                        'hero',
  'images/ai-bg.jpg':                          'hero',
  'images/services-hero.png':                  'hero',
  'images/martin-motlik-portrait.png':         'portrait',
  'images/imtc.jpg':                           'card',
  'references/ifc-verify/cover.png':           'card',
  'references/nascc-card/vizualizace1.png':    'card',
  'references/mass-timber-card/render-card.png': 'card',
  'references/nascc/render-1.png':             'gallery',
  'references/nascc/photo-1.png':              'gallery',
  'references/nascc/photo-2.png':              'gallery',
  'references/nascc/photo-3.png':              'gallery',
  'references/mass-timber/render-1.png':       'gallery',
  'references/mass-timber/render-2.png':       'gallery',
  'references/mass-timber/photo-1.jpg':        'gallery',
  'references/mass-timber/photo-2.jpg':        'gallery',
  'references/rfem6-brochure/brochure-1.png':  'gallery',
  'references/rfem6-brochure/brochure-2.png':  'gallery',
  'references/rfem6-brochure/brochure-3.png':  'gallery',
  'references/rfem6-brochure/brochure-4.png':  'gallery',
};

/**
 * services-hero.png and brochure-2.png are also used as small cards on the
 * home page, so they get the card ladder in addition to their own role.
 */
const EXTRA_ROLES = {
  'images/services-hero.png': 'card',
  'references/rfem6-brochure/brochure-2.png': 'card',
  // Also a ~500px feature card on the references landing page, so it needs
  // renditions above the 960px top of the card ladder for retina screens.
  'references/ifc-verify/cover.png': 'gallery',
};

// Quality settings, tuned so the largest renditions land near 1.2 bpp -
// the same density apple.com ships.
const JPEG = { quality: 76, progressive: true, mozjpeg: true, chromaSubsampling: '4:2:0' };
const AVIF = { quality: 52, effort: 6, chromaSubsampling: '4:2:0' };

const bytes = (n) =>
  n > 1048576 ? `${(n / 1048576).toFixed(1)} MB` : `${Math.round(n / 1024)} KB`;

/** Stable slug for an original, e.g. references/nascc/photo-1.png -> nascc-photo-1 */
function slugFor(rel) {
  const dir = path.dirname(rel);
  const base = path.basename(rel, path.extname(rel));
  const prefix = dir
    .replace(/^images$/, '')
    .replace(/^references\//, '')
    .replace(/\//g, '-');
  return (prefix ? `${prefix}-${base}` : base).replace(/^-+/, '');
}

async function buildOne(rel, roles) {
  const abs = path.join(SRC, rel);
  if (!existsSync(abs)) {
    console.warn(`  ! chybí originál: ${rel}`);
    return null;
  }

  const slug = slugFor(rel);
  const input = sharp(abs, { limitInputPixels: 500e6 });
  const meta = await input.metadata();

  // Union of every ladder this image belongs to, never upscaling past the original.
  const ladder = [...new Set(roles.flatMap((r) => ROLES[r]))].sort((a, b) => a - b);
  const widths = ladder.filter((w) => w <= meta.width);

  // When the original is narrower than the top of its ladder, the largest step
  // we can emit is the original itself. Add it, so a full-bleed hero still gets
  // every pixel the source has instead of stopping at the step below.
  const topStep = ladder.at(-1);
  if (meta.width < topStep && !widths.includes(meta.width)) widths.push(meta.width);
  if (widths.length === 0) widths.push(meta.width);
  widths.sort((a, b) => a - b);

  const entry = {
    slug,
    source: rel,
    sourceWidth: meta.width,
    sourceHeight: meta.height,
    aspect: +(meta.width / meta.height).toFixed(6),
    roles,
    widths: [],
  };

  for (const w of widths) {
    const h = Math.round(w / (meta.width / meta.height));
    const pipeline = sharp(abs, { limitInputPixels: 500e6 })
      .rotate() // honour EXIF orientation before resizing
      .resize({ width: w, withoutEnlargement: true, fit: 'inside', kernel: 'lanczos3' })
      .sharpen({ sigma: 0.5 }) // restore micro-contrast lost in downscaling
      .withMetadata({ icc: 'srgb' });

    const jpgPath = path.join(OUT, `${slug}-${w}.jpg`);
    const avifPath = path.join(OUT, `${slug}-${w}.avif`);

    if (FORCE || !existsSync(jpgPath)) {
      await pipeline.clone().jpeg(JPEG).toFile(jpgPath);
    }
    if (FORCE || !existsSync(avifPath)) {
      await pipeline.clone().avif(AVIF).toFile(avifPath);
    }

    const [js, as] = await Promise.all([stat(jpgPath), stat(avifPath)]);
    const bpp = (js.size * 8) / (w * h);
    entry.widths.push({ w, h, jpg: js.size, avif: as.size, bpp: +bpp.toFixed(2) });
  }

  return entry;
}

/**
 * Social preview card. Scrapers want one fixed 1200x630 JPEG at a URL that
 * never changes, and many of them give up on anything large, so this is built
 * separately from the responsive ladder.
 */
async function buildOgImage() {
  const src = path.join(SRC, 'images/hero-bg.png');
  const out = path.join(ROOT, 'assets/img/og-image.jpg');
  if (!existsSync(src)) return;
  if (!FORCE && existsSync(out)) return;

  await sharp(src)
    .resize(1200, 630, { fit: 'cover', position: 'centre', kernel: 'lanczos3' })
    .sharpen({ sigma: 0.5 })
    .withMetadata({ icc: 'srgb' })
    .jpeg({ quality: 82, progressive: true, mozjpeg: true })
    .toFile(out);

  const s = await stat(out);
  console.log(`og-image.jpg … 1200x630: ${bytes(s.size)}`);
}

async function main() {
  if (!existsSync(SRC)) {
    console.error(`Chybí ${path.relative(ROOT, SRC)} – originály nejsou k dispozici.`);
    process.exit(1);
  }
  await mkdir(OUT, { recursive: true });

  const manifest = {};
  let srcTotal = 0;
  let outJpg = 0;
  let outAvif = 0;

  for (const [rel, role] of Object.entries(IMAGES)) {
    const roles = [role, EXTRA_ROLES[rel]].filter(Boolean);
    process.stdout.write(`${rel} … `);
    const entry = await buildOne(rel, roles);
    if (!entry) continue;

    manifest[entry.slug] = entry;
    srcTotal += (await stat(path.join(SRC, rel))).size;
    const largest = entry.widths.at(-1);
    outJpg += entry.widths.reduce((a, x) => a + x.jpg, 0);
    outAvif += entry.widths.reduce((a, x) => a + x.avif, 0);

    console.log(
      `${entry.widths.length} variant, největší ${largest.w}px: ` +
        `${bytes(largest.jpg)} jpg / ${bytes(largest.avif)} avif (${largest.bpp} bpp)`
    );
  }

  await buildOgImage();
  await writeFile(MANIFEST, JSON.stringify(manifest, null, 2) + '\n');

  const files = (await readdir(OUT)).filter((f) => /\.(jpg|avif)$/.test(f)).length;
  console.log(
    `\nHotovo: ${files} souborů v assets/img/` +
      `\n  originály:  ${bytes(srcTotal)}` +
      `\n  všechny JPEG varianty dohromady:  ${bytes(outJpg)}` +
      `\n  všechny AVIF varianty dohromady:  ${bytes(outAvif)}`
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});

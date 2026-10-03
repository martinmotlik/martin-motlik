# Image pipeline

The site serves no full-resolution images. Every photo on a page comes from
`assets/img/`, as a ladder of fixed-width renditions in AVIF and progressive
JPEG, and the browser picks the one that fits the screen.

This is the approach apple.com uses — several renditions per image, compressed
to roughly 1.0–1.3 bits per pixel — with AVIF added on top, which Apple does
not use and which saves roughly another 45% where it is supported.

## Where the originals live

`Sources/originals/` mirrors the old `assets/` layout and is **gitignored**, so
full-resolution files never enter the repository. Keep that folder: it is the
input to the build. It is not backed up by git — if you work from a fresh clone
you will need to copy it across before rebuilding.

## Adding or replacing an image

1. Put the full-resolution file in `Sources/originals/…`.
2. Register it in the `IMAGES` map in `build-images.mjs` with a role:

   | role | for | widths |
   |------|-----|--------|
   | `hero` | full-bleed background | 640 → 2560 |
   | `card` | reference card, ~238px | 320 → 960 |
   | `portrait` | about photo, ~360px | 360 → 1080 |
   | `gallery` | reference thumbnail + lightbox | 400 → 2560 |

3. `npm run images` — only missing renditions are built, so this is cheap to
   re-run. Use `npm run images:force` to rebuild everything after changing a
   quality setting.
4. Paste the markup: `node tools/picture.mjs <slug> --sizes "…" --alt "…"`.

## Changing a width ladder

Edit `ROLES` in `build-images.mjs`, then:

```
npm run images && npm run images:sync
```

`images:sync` rewrites the `srcset` lists already in the HTML from
`assets/img/manifest.json`. Each list keeps its own upper bound — that bound
encodes how large the image is ever displayed on that page — and gains or loses
only the intermediate steps.

## Things that will bite you

- **`picture { display: contents; }`** is load-bearing. `<picture>` is an inline
  wrapper, so without it any `.parent img { height: 100% }` rule stops
  resolving, the image collapses to zero height, and `loading="lazy"` then
  never fetches it. The image silently never appears.
- **Preload only AVIF.** `type` on `<link rel="preload">` filters out formats
  the browser cannot decode; it is not a preference. A second JPEG preload link
  makes modern browsers fetch both renditions of the LCP image.
- **`sizes` must match the CSS.** If it overstates the box the browser fetches a
  rendition that is too large; understating it makes the image soft. Measure the
  real box in the browser rather than guessing.
- **`clamp()` in `sizes`** is not reliably supported — spell the breakpoints out
  as media conditions instead.
- When checking a change in the browser, remember Chrome prefers an
  already-cached larger rendition over downloading a smaller one. A warm cache
  will show a bigger file than a first-time visitor gets.

## One-off scripts

`rewrite-reference-pages.py` performed the original conversion of the three
reference pages. It is kept for reference and is a no-op once converted.

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

## Crops: when `sizes` is not enough

`sizes` describes the **width** of the image's box. With `object-fit: cover`,
if the image's aspect ratio does not match the box's, the browser scales to
cover the box and the *other* axis becomes the binding constraint — and `sizes`
cannot express that. Feeding a 16:9 photo to a 3:5 portrait card meant the
browser cropped the sides and blew the rest up 2.8x beyond the file's pixels.
Visibly soft, and no amount of `sizes` tuning fixes it.

The answer is `CROPS` in `build-images.mjs`: render the image at the aspect
ratio the box actually has. A centre crop is exactly what `object-fit: cover;
object-position: center` already displayed, so nothing moves visually, and no
pixels are shipped only to be cropped away.

Current crops, each matching its box:

| slug suffix | ratio | box |
|---|---|---|
| `-card` | 3:5 | home-page reference cards |
| `portrait-card` | 3:4 | about photo |
| `-thumb` | 3:2 | reference-page filmstrip |

The lightbox deliberately keeps the **uncropped** images — it shows the whole
frame, not the card's crop.

**Check for this whenever you add an image**: load the page and compare the
file's real pixel size against `box × devicePixelRatio`. Anything above ~1.0
means the browser is inventing pixels and the image needs a crop, not a bigger
`sizes`.

## Things that will bite you

- **Never write the literal picture tag in a CSS comment.** The rewrite
  scripts match `<picture>` in the HTML; prose containing that tag inside a
  comment swallowed the first real element on each page and silently skipped
  it. The regexes now require a `<source>` right after the tag.
- **A `>` combinator targeting the image stops matching.** Wrapping the image
  in `<picture>` makes it a grandchild, so `.parent > img` silently stops
  applying. `display: contents` removes the picture's *box*, not its DOM node,
  and selectors match against the DOM. This is what left the photo showing
  behind the 3D model on the references page. Use a descendant selector.
- **Sibling JS breaks the same way.** `img.nextElementSibling` now resolves
  inside the `<picture>`; reach past it with `img.closest('picture')`.
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

## Language versions (`build-i18n.py`)

Every page exists in English, Czech and German, each at its own URL with the
translated text in the HTML (search engines and AI crawlers do not run
JavaScript, so a switch in the browser would leave the translations invisible).
English is the hand-edited source; Czech and German are generated from it and
`<page>/i18n/cs.json` / `de.json` (the home page's are in `/i18n/`).

| Page | English | Czech | German |
|---|---|---|---|
| Home | `/` | `/cs/` | `/de/` |
| Services | `/services/` | `/cs/sluzby/` | `/de/leistungen/` |
| References | `/references/…` | `/cs/reference/…` | `/de/referenzen/…` |
| Insights | `/insights/…` | `/cs/insights/…` | `/de/insights/…` |

Slugs are translated where they are words (`rfem6-brochure` →
`rfem6-brozura` / `rfem6-broschuere`, the article slugs) and kept where they
are names (`nascc-2026`, `insights`). They are set in one place, `URLS` in the
script. Plain ASCII, ü → ue. **Decide a slug before the page is first
published and never change it afterwards:** GitHub Pages cannot send 301
redirects.

After changing an English page or a translation:

```bash
python3 tools/build-i18n.py
```

Then commit the regenerated `cs/`, `de/` and `sitemap.xml` with the change.
`python3 tools/build-i18n.py --check` exits with an error when they are out of
date.

### What a translation file holds

| Key | Replaces |
|---|---|
| `chrome` | the content of `[data-i18n="…"]`; markup (`<br>`, `<em>`, links) must match the English element |
| `k` | article blocks, `[data-k="…"]` (Insights) |
| `text` | any other text node whose whole text equals the English key (nav links, pills, dates) |
| `attrs` | `alt`, `aria-label` and `title` values equal to the English key |
| `ui` | `<title>`, `data-i18n-attr` bindings and strings page scripts write later (read from `#i18n-ui`) |
| `meta` | description, Open Graph and Twitter texts, `in_language` |
| `ld` | JSON-LD values by path, e.g. `"@graph.0.description"` |
| `keep` | text that stays the same in this language (names, venues, codes) |

The build refuses to write when a translated block's markup differs from
English, a key is missing, a JSON-LD path does not exist, or **any visible
English text or alt / aria-label / title is left on a translated page** that is
not in `keep`. That last check is what keeps new English text from slipping
into the Czech and German pages unnoticed: add the translation, or, for a
name, add it to `keep`.

Each version has its own canonical, `hreflang` links to all three (plus
`x-default` → English), localized title, description, Open Graph and JSON-LD.
Page URLs in JSON-LD point to the version; people, organisations and the
website keep one identity (`#person`, `#website`…). `sitemap.xml` is generated
from the same table. Never point a translation's canonical at the English
page: Google would drop the translation.

Adding a page: add it to `PAGES`, `URLS` (if its slug is translated) and
`SITEMAP` in the script, put the matching `hreflang` block and the
`og:locale:alternate` lines in its `<head>`, make its language switcher links
like the other pages, add `i18n/cs.json` and `de.json`, run the build until it
passes, and list the URLs in `llms.txt`.

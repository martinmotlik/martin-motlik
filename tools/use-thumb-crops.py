#!/usr/bin/env python3
"""
Points the reference-page filmstrip thumbnails at their 3:2 crops.

The strip boxes are 3:2 but the sources are 16:9 or wider, so the uncropped
files were being stretched 1.13-1.27x to cover. The lightbox is left alone:
it shows the whole frame, so it keeps the uncropped images.

Idempotent.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
M = json.loads((ROOT / "assets/img/manifest.json").read_text())

PAGES = [
    "references/nascc-2026/index.html",
    "references/mass-timber-2026/index.html",
    "references/rfem6-brochure/index.html",
]

# .strip-item is width: clamp(260px, 28vw, 420px)
STRIP_SIZES = "(max-width: 928px) 260px, (max-width: 1500px) 28vw, 420px"

# <picture> blocks that live inside a .strip-item
# Require a <source> right after the tag, so prose mentioning the element
# inside a CSS comment cannot be mistaken for real markup.
PICTURE = re.compile(r"<picture>\s*<source\b.*?</picture>", re.S)


def build(slug, alt, indent):
    ws = [v["w"] for v in M[slug]["widths"]]
    mid = ws[len(ws) // 2]
    meta = next(v for v in M[slug]["widths"] if v["w"] == mid)
    pad = " " * indent

    def ss(ext, align):
        return (",\n" + " " * align).join(f"/assets/img/{slug}-{w}.{ext} {w}w" for w in ws)

    return (
        f"<picture>\n"
        f'{pad}  <source type="image/avif" sizes="{STRIP_SIZES}"\n'
        f'{pad}          srcset="{ss("avif", indent + 18)}">\n'
        f'{pad}  <img src="/assets/img/{slug}-{mid}.jpg" sizes="{STRIP_SIZES}"\n'
        f'{pad}       srcset="{ss("jpg", indent + 15)}"\n'
        f'{pad}       alt="{alt}"\n'
        f'{pad}       width="{meta["w"]}" height="{meta["h"]}"'
        f' loading="lazy" decoding="async">\n'
        f"{pad}</picture>"
    )


def main():
    for page in PAGES:
        p = ROOT / page
        s = p.read_text()
        n = 0

        def repl(m):
            nonlocal n
            block = m.group(0)
            # only touch strip items, never the lightbox picture
            start = s.rfind('class="strip-item"', 0, m.start())
            lb = s.rfind("lightbox", 0, m.start())
            if start == -1 or lb > start:
                return block
            slug_m = re.search(r"/assets/img/([a-z0-9-]+?)-\d+\.(?:avif|jpg)", block)
            if not slug_m:
                return block
            slug = slug_m.group(1)
            if slug.endswith("-thumb"):
                return block  # already converted
            thumb = f"{slug}-thumb"
            if thumb not in M:
                print(f"    ! chybí výřez {thumb}, ponechávám")
                return block
            alt = re.search(r'alt="([^"]*)"', block).group(1)
            indent = m.start() - (s.rfind("\n", 0, m.start()) + 1)
            n += 1
            return build(thumb, alt, indent)

        out = PICTURE.sub(repl, s)
        if n:
            p.write_text(out)
        print(f"  {page}: {n} náhledů přepnuto na výřez 3:2")


if __name__ == "__main__":
    sys.exit(main())

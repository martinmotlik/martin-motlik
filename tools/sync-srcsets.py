#!/usr/bin/env python3
"""
Re-syncs the srcset lists already present in the HTML with assets/img/manifest.json.

Run this after changing a width ladder in build-images.mjs. Each existing list
keeps its own upper bound - that bound encodes how large the image is ever
displayed on that page - and simply gains or loses the intermediate steps the
manifest now has.

Also updates the `w: [...]` arrays that drive the reference-page lightboxes.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "assets/img/manifest.json").read_text())

PAGES = [
    "index.html",
    "services/index.html",
    "references/index.html",
    "references/nascc-2026/index.html",
    "references/mass-timber-2026/index.html",
    "references/rfem6-brochure/index.html",
]

CANDIDATE = re.compile(r"/assets/img/(?P<slug>[a-z0-9-]+?)-(?P<w>\d+)\.(?P<ext>avif|jpg) \d+w")
SRCSET = re.compile(r'srcset="(?P<body>[^"]*?/assets/img/[^"]*?)"', re.S)
LIGHTBOX = re.compile(r"\{ slug: '(?P<slug>[a-z0-9-]+)', w: \[(?P<ws>[^\]]*)\] \}")


def widths_for(slug, cap):
    return [v["w"] for v in MANIFEST[slug]["widths"] if v["w"] <= cap]


def rewrite_srcset(m):
    body = m.group("body")
    entries = list(CANDIDATE.finditer(body))
    if not entries:
        return m.group(0)

    slug = entries[0].group("slug")
    ext = entries[0].group("ext")
    if slug not in MANIFEST:
        print(f"    ! neznámý slug {slug}, ponechávám beze změny")
        return m.group(0)

    cap = max(int(e.group("w")) for e in entries)
    ws = widths_for(slug, cap)
    if not ws:
        return m.group(0)

    # Keep whatever indentation the first continuation line used.
    sep = re.search(r",\n(\s+)", body)
    joiner = ",\n" + sep.group(1) if sep else ", "
    new = joiner.join(f"/assets/img/{slug}-{w}.{ext} {w}w" for w in ws)
    return f'srcset="{new}"'


def rewrite_lightbox(m):
    slug = m.group("slug")
    if slug not in MANIFEST:
        return m.group(0)
    cap = max(int(x) for x in re.findall(r"\d+", m.group("ws")))
    ws = widths_for(slug, cap)
    return f"{{ slug: '{slug}', w: {ws} }}"


def main():
    changed = 0
    for page in PAGES:
        p = ROOT / page
        before = p.read_text()
        after = SRCSET.sub(rewrite_srcset, before)
        after = LIGHTBOX.sub(rewrite_lightbox, after)
        if after != before:
            p.write_text(after)
            n = len(SRCSET.findall(after))
            print(f"  {page}: {n} srcset seznamů synchronizováno")
            changed += 1
        else:
            print(f"  {page}: beze změny")
    print(f"Hotovo ({changed} souborů upraveno).")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
One-off rewrite of the three reference pages onto the responsive image set.

Converts every gallery <img> into a <picture> (AVIF + JPEG, width-selected),
points the "next project" thumbnail at a small variant, and reworks the
lightbox so it also picks a width instead of always loading the original.

Safe to re-run: it asserts on every replacement and leaves already-converted
markup alone.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "assets/img/manifest.json").read_text())

# Old asset path -> manifest slug
SLUGS = {
    "/assets/references/nascc/render-1.png": "nascc-render-1",
    "/assets/references/nascc/photo-1.png": "nascc-photo-1",
    "/assets/references/nascc/photo-2.png": "nascc-photo-2",
    "/assets/references/nascc/photo-3.png": "nascc-photo-3",
    "/assets/references/mass-timber/render-1.png": "mass-timber-render-1",
    "/assets/references/mass-timber/render-2.png": "mass-timber-render-2",
    "/assets/references/mass-timber/photo-1.jpg": "mass-timber-photo-1",
    "/assets/references/mass-timber/photo-2.jpg": "mass-timber-photo-2",
    "/assets/references/rfem6-brochure/brochure-1.png": "rfem6-brochure-brochure-1",
    "/assets/references/rfem6-brochure/brochure-2.png": "rfem6-brochure-brochure-2",
    "/assets/references/rfem6-brochure/brochure-3.png": "rfem6-brochure-brochure-3",
    "/assets/references/rfem6-brochure/brochure-4.png": "rfem6-brochure-brochure-4",
}

# .strip-item is width: clamp(260px, 28vw, 420px) — spelled out as media
# conditions because clamp() in a sizes attribute is not reliably supported.
STRIP_SIZES = "(max-width: 928px) 260px, (max-width: 1500px) 28vw, 420px"
# .next-thumb is a fixed 100x67 box.
THUMB_SIZES = "100px"

PAGES = ["references/nascc-2026", "references/mass-timber-2026", "references/rfem6-brochure"]


def widths(slug, cap=None):
    ws = [v["w"] for v in MANIFEST[slug]["widths"]]
    if cap:
        kept = [w for w in ws if w <= cap]
        ws = kept or ws[:1]
    return ws


def picture(slug, sizes, alt, indent, cap=None, extra=""):
    ws = widths(slug, cap)
    pad = " " * indent
    mid = ws[min(len(ws) - 1, len(ws) // 2)]
    meta = next(v for v in MANIFEST[slug]["widths"] if v["w"] == mid)

    def srcset(ext, align):
        join = ",\n" + " " * align
        return join.join(f"/assets/img/{slug}-{w}.{ext} {w}w" for w in ws)

    return (
        f'{pad}<picture>\n'
        f'{pad}  <source type="image/avif" sizes="{sizes}"\n'
        f'{pad}          srcset="{srcset("avif", indent + 18)}">\n'
        f'{pad}  <img src="/assets/img/{slug}-{mid}.jpg" sizes="{sizes}"\n'
        f'{pad}       srcset="{srcset("jpg", indent + 15)}"\n'
        f'{pad}       alt="{alt}"\n'
        f'{pad}       width="{meta["w"]}" height="{meta["h"]}"'
        f' loading="lazy" decoding="async"{extra}>\n'
        f'{pad}</picture>'
    )


IMG_RE = re.compile(r'(?P<pad>[ \t]*)<img\s+src="(?P<src>[^"]+)"\s+alt="(?P<alt>[^"]*)"\s*>')


def convert_simple_imgs(html, path):
    """Strip-item and next-thumb images: <img src alt> on one line."""
    count = 0

    def repl(m):
        nonlocal count
        src = m.group("src")
        if src not in SLUGS:
            return m.group(0)
        slug = SLUGS[src]
        indent = len(m.group("pad"))
        # The only image inside .next-thumb is the one in the project-nav block;
        # detect it by the 100px box it sits in.
        before = html[: m.start()]
        is_thumb = before.rfind('class="next-thumb"') > before.rfind('class="strip-item"')
        count += 1
        if is_thumb:
            return picture(slug, THUMB_SIZES, m.group("alt"), indent, cap=400)
        return picture(slug, STRIP_SIZES, m.group("alt"), indent)

    out = IMG_RE.sub(repl, html)
    print(f"  {path}: {count} obrázků převedeno na <picture>")
    return out


def convert_lightbox(html, path):
    """Wrap the lightbox <img> in a <picture> and drive it from slugs."""
    m = re.search(
        r'[ \t]*<img class="lightbox-img" id="lightbox-img" src="" alt="(?P<alt>[^"]*)">', html
    )
    assert m, f"{path}: lightbox <img> nenalezen"
    html = html.replace(
        m.group(0),
        '    <picture>\n'
        '        <source id="lightbox-avif" type="image/avif" sizes="92vw" srcset="">\n'
        f'        <img class="lightbox-img" id="lightbox-img" src="" alt="{m.group("alt")}"'
        ' sizes="92vw" decoding="async">\n'
        '    </picture>',
        1,
    )

    arr = re.search(r"    const allImages = \[\n(?P<body>.*?)\n    \];", html, re.S)
    assert arr, f"{path}: pole allImages nenalezeno"

    # Drop commented-out entries (the NASCC page carries two placeholders for
    # photos that were never added) before reading the paths.
    live_lines = [l for l in arr.group("body").splitlines() if not l.lstrip().startswith("//")]
    srcs = re.findall(r"'([^']+)'", "\n".join(live_lines))
    entries = []
    for s in srcs:
        assert s in SLUGS, f"{path}: neznámý obrázek v allImages: {s}"
        slug = SLUGS[s]
        entries.append(f"        {{ slug: '{slug}', w: {widths(slug)} }},")

    new_arr = (
        "    // Each entry is a slug plus the widths build-images.mjs produced for it;\n"
        "    // setLightboxImage() turns that into a srcset so the lightbox loads a\n"
        "    // rendition that fits the screen instead of the full-resolution original.\n"
        "    const allImages = [\n" + "\n".join(entries) + "\n    ];\n"
        "\n"
        "    function setLightboxImage(i) {\n"
        "        const im = allImages[i];\n"
        "        const build = (ext) => im.w.map(w => `/assets/img/${im.slug}-${w}.${ext} ${w}w`).join(', ');\n"
        "        document.getElementById('lightbox-avif').srcset = build('avif');\n"
        "        const img = document.getElementById('lightbox-img');\n"
        "        img.srcset = build('jpg');\n"
        "        img.src = `/assets/img/${im.slug}-${im.w[im.w.length - 1]}.jpg`;\n"
        "    }"
    )
    html = html.replace(arr.group(0), new_arr, 1)

    # Route every place that used to poke .src through the new helper.
    before = html
    html = re.sub(
        r"document\.getElementById\('lightbox-img'\)\.src = allImages\[(?P<i>[^\]]+)\];",
        lambda m: f"setLightboxImage({m.group('i')});",
        html,
    )
    assert html != before, f"{path}: nenalezeno žádné přiřazení lightbox src"
    print(f"  {path}: lightbox přepojen na {len(entries)} responzivních obrázků")
    return html


def main():
    for page in PAGES:
        p = ROOT / page / "index.html"
        html = p.read_text()
        if "/assets/img/" in html and "<picture>" in html:
            print(f"  {page}: již převedeno, přeskakuji")
            continue
        html = convert_simple_imgs(html, page)
        html = convert_lightbox(html, page)
        p.write_text(html)
    print("Hotovo.")


if __name__ == "__main__":
    sys.exit(main())

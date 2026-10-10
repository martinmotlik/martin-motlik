# Czech and German versions

The CS and DE pages are generated: never edit `cs/…` or `de/…` by hand.
`python3 tools/build-i18n.py` writes them from the English page plus
`insights/<slug>/i18n/{cs,de}.json`.

## Slugs

- Add the article to `PAGES` and its slugs to `URLS` in `tools/build-i18n.py`.
- Slugs are translated, ASCII, kebab-case, short, with the article's search
  phrase in that language (`/cs/insights/data-aec-pro-vyhledavani-s-ai/`,
  `/de/insights/aec-daten-fuer-ki-suche/`; ü → ue). Agree them in the brief.
  They never change after publishing.
- Add the path to `SITEMAP` with today's date; bump `lastmod` whenever the
  page's content changes.

## The JSON

Copy `insights/ai-visibility-for-aec/i18n/cs.json` as the starting shape.

| key | holds |
|---|---|
| `k` | every `data-k` block: the inner HTML, same markup skeleton as the English block (the build checks it) |
| `chrome` | short labels (`data-i18n`): nav, TOC label, share, read time, podcast labels |
| `ui` | attribute values (`data-i18n-attr="alt:cover_alt"`), `data-ui` text, `<title>`, player strings |
| `meta` | description, image alt, section, locale, `in_language`, the four tags, keywords, about, citations, breadcrumb names |
| `keep` | English strings that stay English on purpose (product names, standards) |

Content marked `lang="en"` (episode titles, chapters, transcript) stays
English and is skipped by the untranslated-text check.

## Translation rules

- Translate meaning for a professional reader in that market, not words.
  Keep the first person and Martin's tone.
- Standards, product names and code stay as they are (NDS, CSA O86,
  robots.txt). Explain a U.S. term once if the CS/DE reader would not know it.
- **Czech**: non-breaking space after one-letter prepositions and
  conjunctions (`s AI`, `v USA`), „quotes", dates "6. října 2026",
  "8 min čtení", vykání.
- **German**: „Anführungszeichen", Sie-form, dates "6. Oktober 2026",
  "8 Min. Lesezeit".
- Episode and article titles of the podcast stay English where the episode
  is English; say on the page that the podcast is in English.

## Checks

```
python3 tools/build-i18n.py
python3 tools/build-i18n.py --check
```

The build fails on: missing keys, a block whose markup differs from the
English one, hreflang that disagrees with `URLS`, and English text left on a
CS/DE page that is not in `keep`. Fix the JSON, never the generated page.

# Review notes · A power outlet for AI

Page: `insights/mcp-power-outlet-for-ai/index.html` (built 2026-10-24 on the
GEO article's template, before the article text arrived). Screenshots:
`review/` (desktop 1440 px, phone 390 px, full page; the GEO article for
comparison; the code block open; the lightbox).

## For approval

### `<title>` (≤ 60 characters)

The working title has 73 characters. The site rule is that `<title>` repeats
the H1 word for word in Title Case, so a shorter `<title>` means a shorter H1.

| | `<title>` | H1 (sentence case) | Chars |
|---|---|---|---|
| A | A Power Outlet for AI: What MCP Means for AEC | A power outlet for AI: what MCP means for AEC | 45 |
| B | What Is MCP? A Power Outlet for AI in AEC Software | What is MCP? A power outlet for AI in AEC software | 50 |

Until you choose, the page uses the full working title in both.

### Meta description (≤ 155 characters)

| | Text | Chars |
|---|---|---|
| A | MCP lets any AI assistant work with any AEC tool through one standard connection. What it is, what I built with it and how to start. | 132 |
| B | What the Model Context Protocol is, why AEC software is adopting it, and what I learned connecting ChatGPT and Gemini to an IFC model review. | 141 |

The page uses A for now.

### Dek (perex under the H1)

- **A:** MCP is an open standard that lets AI assistants work with your software through one connection, like a power outlet. I built an MCP server for IFC model review to see what that means for AEC, and what it asks of the people who use it.
- **B:** An AI assistant can now read a BIM model, check it against an IDS file and point to the failing doors in a 3D viewer, all through one open protocol. Here is what MCP is, what I learned building a server for it, and what to ask your software vendors.

If the article's Markdown has its own dek, that one wins and these are only
suggestions.

### Other choices made on the page (change any)

- **Tags (four):** Model Context Protocol · AI assistants · BIM · IFC
- **Category:** AI in AEC (same as article #1)
- **Breadcrumb short name:** A power outlet for AI
- **OG image alt:** "ChatGPT's answer links to three doors in a web-based 3D viewer of a residential building" (shorter than the hero alt from `assets.md`)
- **Section order and ids:** What MCP is (`what-mcp-is`) · What I built (`what-i-built`) · Three levels of trust (`trust`) · Where the industry stands (`industry`) · How to start on Monday (`monday`). Taken from the brief; checked against the Markdown when it arrives.
- **Dates:** `2026-10-24` in the meta tags and JSON-LD is provisional; the byline shows `[TK: date]`.

## Placeholders still on the page

Every `[TK: …]` is highlighted yellow on the page. Count: 29. They are the
dek, date, read time, every text paragraph, the five vendor questions and their
card title, the key takeaway, the sources and the closing sentence. They are
replaced word for word from `article.md`; the page is not published while one
is left (`check-package.py` checks it).

## Done without the text

- Hero (01) with the 1200 × 630 OG crop (the hero has no text, so no
  `-notext` variant is needed); figures 1–6 (02, 03, 04, 06, 07, 08) and the
  two unnumbered images (05, 11) with alt text and captions from `assets.md`.
  Captions drop the "Figure N." prefix of `assets.md`; the page numbers them.
- Click on a figure: the image opens in a dialog at up to 3840 px, with a
  link to the full-resolution JPEG. Without JavaScript the link opens the file.
- Figure 2 code as text: lines 137–159 of `packages/mcp-server/src/server.ts`,
  exactly as in the image, in the site's code block with Copy.
- JSON-LD: `TechArticle` (no `audio` until the episode exists, no
  `wordCount` until the text exists, `citation` empty until the sources
  exist), `Person`, `BreadcrumbList`. Valid JSON.
- "Keep reading" with a card for article #1 at the end of this article.

## Waiting

- **CS/DE:** the language switcher on this page leads to the CS/DE Insights
  lists until the translations exist; `hreflang` lists only EN.
- **Article #1:** its "Keep reading" card for this article, the card on
  `/insights/`, `llms.txt` and `sitemap.xml` come with the text (title,
  excerpt) and the CS/DE strings the build checks.
- **Podcast:** the page has empty podcast markers; `build-podcast.py` fills
  them once EP 02 is in `podcast/podcast.json`.

## Remarks on the text

(Filled in once `article.md` arrives. The text itself is not changed.)

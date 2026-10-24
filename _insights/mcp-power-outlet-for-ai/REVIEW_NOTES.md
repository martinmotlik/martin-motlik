# Review notes · A power outlet for AI

Page: `insights/mcp-power-outlet-for-ai/index.html`, built on the GEO
article's template from `article.md` (the final text, exported from the Claude
doc on 2026-10-24, rev 40, 18,520 bytes). Screenshots: `review/` (desktop
1440 px and phone 390 px, full page; the GEO article for comparison; the code
block open; the lightbox).

**Text check:** all 86 text blocks and the 11 sources on the page match
`article.md` word for word (compared after removing Markdown syntax and
normalizing quotes). Changes are typographic only: straight quotes and
apostrophes became ’ “ ”, as on the rest of the site, and the H1 is in
sentence case like article #1 (the doc has Title Case).

## For approval

### `<title>` (≤ 60 characters)

The title has 73 characters. The site rule is that `<title>` repeats the H1
word for word in Title Case, so a shorter `<title>` means a shorter H1.

| | `<title>` | H1 (sentence case) | Chars |
|---|---|---|---|
| A | A Power Outlet for AI: What MCP Means for AEC | A power outlet for AI: what MCP means for AEC | 45 |
| B | What Is MCP? A Power Outlet for AI in AEC Software | What is MCP? A power outlet for AI in AEC software | 50 |

Until you choose, the page uses the full title.

### Meta description (≤ 155 characters)

| | Text | Chars |
|---|---|---|
| A | Your AI assistant can’t open your model. MCP, an open standard backed by OpenAI, Google and Microsoft, connects it to the AEC tools you already trust. | 150 |
| B | What Model Context Protocol is, what it’s good for in AEC, and why plugging into ChatGPT, Claude, Gemini and Copilot beats building another chatbot. | 148 |

The page uses A.

### Dek (perex under the H1; the doc has none)

- **A** (on the page): Model Context Protocol is an open standard that connects AI assistants to the software engineers already use. What it is, what it’s good for in AEC, and why plugging into the big AI platforms beats building another chatbot.
- **B:** Your AI assistant can draft the RFI response but can’t open your model. MCP changes that: one standard socket between the AI you already use and the engineering software you already trust.

### Closing box ("Next step"; the doc has none)

On the page: "If you’re connecting AEC software to AI assistants or planning an MCP
pilot, I’d be happy to compare notes." Heading and LinkedIn button as in
article #1.

### Other choices made on the page (change any)

- **Contents labels** are the H2s up to the colon: The AI that can’t open your model · What MCP is · Why AEC needs it · Why plug into the AI giants · Three levels of trust · What I built · Where the industry stands · What MCP won’t fix · How to start on Monday · A bridge, not a replacement.
- **Section ids:** `cant-open`, `what-mcp-is`, `why-aec`, `why-plug-in`, `trust`, `what-i-built`, `industry`, `wont-fix`, `monday`, `bridge` (also the podcast chapter anchors later).
- **Lead:** the first paragraph ("Your AI assistant can draft…") in the lead style, under the first H2.
- **Five reasons** ("Why plug into the AI giants") in the numbered style of article #1's "My rules", the bold sentence as the lead-in.
- **Five vendor questions** in the highlighted card, without a label (the sentence above introduces them).
- **Tags (four):** Model Context Protocol · AI assistants · BIM · IFC. **Category:** AI in AEC. **Breadcrumb:** A power outlet for AI.
- **Date:** Oct 22, 2026 from the doc; set it to the release date when publishing. **Read time:** 12 min (2,645 words / 230).
- **No key takeaway box:** article #1 has one, this text has none. If you want one, a sentence from "A bridge, not a replacement" would do it ("MCP is the outlet between them…").
- **Sources:** numbered [1]–[11] at the end, as in the doc; the text keeps its inline links and has no [n] markers (article #1 has them).

## Open in the text (`[TK]`, highlighted on the page)

1. H2 "What I built: [TK: two evenings] and six tools"
2. The demo's final answer (paragraph after Figure 3)
3. One honest sentence from the build log (end of "What I built")
4. One line pointing to the companion podcast episode (end of the article)

The page is not published while one is left (`check-package.py` checks it).

## Remarks on the text (the text is unchanged; for your decision)

1. **The demo in the text and in the images differ.** The text asks "Which
   load-bearing walls changed in version B…" and Figure 4 is described as
   "the highlighted walls". The screenshots (01, 06, 07, 08) show a different
   demo: "Compare revision R02 with R03. Which of the elements that failed
   the IDS check were fixed…", with the answer "R03 fixes 10 of the 13
   elements that failed in R02. Three still fail" and three doors on
   Residential Level 3 without a fire rating. Either the paragraph and the
   [TK] answer follow the screenshots (my suggestion: the images are real),
   or the images are retaken for the walls question.
2. **Figure 2:** the doc's note says "about ten lines of Python"; the image
   (and the code block under it) is TypeScript, lines 137–159 of
   `server.ts`, 23 lines. Nothing in the text says Python, so no text change
   is needed; just a heads-up.
3. **Figure 3:** the doc's note says "the tool list … with the descriptions
   the AI reads"; image 04 shows ChatGPT's settings with the server switched
   on, not the tool list. The caption from `assets.md` matches the image.
4. **Figure 1:** the doc has its own caption sentence under the diagram ("Each
   AI application needs one client…"). It stays on the page as a paragraph
   under the figure; the figure caption comes from `assets.md`. Consider
   dropping one of the two.
5. **Image 05** has a black band along the right and bottom edges in the
   source file (the window edge of the capture). Worth re-rendering.
6. The lead question names "girder on level 3"; the closing section picks it
   up ("finds the girders that changed"). Nice frame. The demo, though, is
   about doors; another reason to align remark 1.

## Waiting

- **CS/DE:** the language switcher on this page leads to the CS/DE Insights
  lists until the translations exist; `hreflang` lists only EN.
- **Article #1:** its "Keep reading" card for this article, the card on
  `/insights/`, `llms.txt` and `sitemap.xml` come with the CS/DE strings the
  build checks.
- **Podcast:** the page has empty podcast markers; `build-podcast.py` fills
  them once EP 02 is in `podcast/podcast.json`.

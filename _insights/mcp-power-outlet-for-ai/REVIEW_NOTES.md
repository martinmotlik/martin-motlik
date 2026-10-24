# Review notes · A power outlet for AI

Page: `insights/mcp-power-outlet-for-ai/index.html`, built by `build-page.py`
from `article.md` on the GEO article's template. `article.md` is the text
after feedback, exported from the Claude doc on 2026-10-24 (rev 53, 22,321
bytes). Screenshots: `review/` (desktop 1440 px and phone 390 px, full page;
the GEO article for comparison; the code block open; the lightbox).

**Text check:** all 92 text blocks, the 10 links in the text and the 15
sources on the page match `article.md` word for word (compared after removing
Markdown syntax and normalizing quotes). Changes are typographic only:
straight quotes and apostrophes became ’ “ ”, as on the rest of the site.
The H1 is the approved shorter title (below), not the doc's title. No `[TK]`
is left.

## Approved (2026-10-24)

- **Title:** variant A. H1 "A power outlet for AI: what MCP means for AEC"; `<title>` "A Power Outlet for AI: What MCP Means for AEC" (45 characters). The doc's longer title stays in the doc.
- **Meta description:** "Your AI assistant can’t open your model. MCP, an open standard backed by OpenAI, Google and Microsoft, connects it to the AEC tools you already trust." (150 characters)
- **Dek:** "Model Context Protocol is an open standard that connects AI assistants to the software engineers already use. What it is, what it’s good for in AEC, and why connecting to the AI platforms your team already uses usually makes more sense than building another chatbot."

## For approval

### Closing box ("Next step"; the doc has none)

On the page: "If you’re connecting AEC software to AI assistants or planning an
MCP pilot, I’d be happy to compare notes." Heading and LinkedIn button as in
article #1.

### Other choices made on the page (change any)

- **Contents labels** are the H2s up to the colon: The AI that can’t open your model · What MCP is · Why AEC needs it · Why plug into the AI giants · Three kinds of access · What I built · Where the industry stands · What MCP won’t fix · How to start on Monday · A bridge, not a replacement.
- **Section ids:** `cant-open`, `what-mcp-is`, `why-aec`, `why-plug-in`, `access`, `what-i-built`, `industry`, `wont-fix`, `monday`, `bridge` (also the podcast chapter anchors later).
- **Lead:** the first paragraph ("Your AI assistant can draft…") in the lead style, under the first H2.
- **Five reasons** ("Why plug into the AI giants") in the numbered style of article #1's "My rules", the bold sentence as the lead-in.
- **Five vendor questions** in the highlighted card, without a label (the sentence above introduces them).
- **Image 05** (permission prompt) after the "Checking." paragraph; **image 11** (timeline) after the first paragraph of "Where the industry stands".
- **Tags (four):** Model Context Protocol · AI assistants · BIM · IFC. **Category:** AI in AEC. **Breadcrumb:** A power outlet for AI.
- **Date:** Oct 22, 2026 from the doc; set it to the release date when publishing. **Read time:** 14 min (3,121 words / 230).
- **No key takeaway box:** article #1 has one, this text has none.
- **Sources:** numbered [1]–[15] at the end, as in the doc; the text keeps its inline links and has no [n] markers (article #1 has them).

## Remarks (the text is unchanged; for your decision)

Resolved by the revision: the demo in the text now matches the screenshots
(R02 → R03, three doors on Residential Level 3), and the four `[TK]` are gone.

1. **Image 11 (timeline)** ends with the July 2026 specification. The text
   now also names the September Revit servers (Trusted-Write and
   Experimental). The image is not wrong, just a step behind; a "Sep 2026"
   point would match the text.
2. **"Prefer to listen?"** (last paragraph) promises a companion episode.
   EP 02 doesn't exist yet; the page shows the player only once it does.
   Publish the article together with the episode, or leave this line out
   until then.
3. **Figure 2:** the doc's note says "about ten lines of Python"; the image
   (and the code block under it) is TypeScript, 23 lines. Nothing in the text
   says Python.
4. **Figure 3:** the doc's note says "the tool list … with the descriptions
   the AI reads"; image 04 shows ChatGPT's settings with the server switched
   on. The caption from `assets.md` matches the image.
5. **Figure 1:** the doc has its own caption sentence under the diagram ("Each
   AI application needs one client…"). It stays on the page as a paragraph
   under the figure; the figure caption comes from `assets.md`. Consider
   dropping one of the two.
6. **Image 05** has a black band along the right and bottom edges in the
   source file (the window edge of the capture). Worth re-rendering.

## Translations (CS, DE; 2026-10-24)

Source: `article.cs.md`, `article.de.md` (the article block for block) and
`i18n-{cs,de}.extras.json` (hero, contents, captions, alt texts, metadata).
`i18n-from-md.py <lang>` writes `insights/mcp-power-outlet-for-ai/i18n/<lang>.json`;
then `tools/build-i18n.py`. Czech non-breaking spaces are added by the script.

Choices worth a native read:

- **Units localized** in the example question: "cubic yards of concrete" →
  „metrů krychlových“ / „Kubikmeter“ (as article #1 argues: write in the
  language of the reader's market). "L/360" stays as it is.
- **Terms:** girder → průvlak / Unterzug; demand-to-capacity ratio → využití
  únosnosti / Ausnutzung; fire rating → požární odolnost /
  Feuerwiderstandsklasse; fire safety design → požárně bezpečnostní řešení /
  Brandschutzkonzept; BIM Execution Plan → BIM Execution Plan (CS, as used) /
  BIM-Abwicklungsplan; serviceability load combinations → kombinace mezního
  stavu použitelnosti / Grenzzustand der Gebrauchstauglichkeit.
- **Prague** stays „v Praze“ / „in Prag“ (the article names the city).
- **MCP roles** "Tools, Resources, Prompts": CS translates them (Nástroje,
  Zdroje, Prompty), DE keeps the protocol's English names; the diagram
  (image 02) shows them in English.
- **Podcast line:** both say the episode is in English, as the translation
  rules require.
- **Screenshots** stay English (real application interfaces); captions and
  alt texts are translated. Sources stay English (titles of English pages).

## Waiting

- **Listed (2026-10-24):** featured and first card on `/insights/`, entry in
  `llms.txt` (with the CS/DE lines and the language table), "Keep reading"
  card in article #1, `sitemap.xml` in all three languages.
- **Podcast:** the page has empty podcast markers; `build-podcast.py` fills
  them once EP 02 is in `podcast/podcast.json`.

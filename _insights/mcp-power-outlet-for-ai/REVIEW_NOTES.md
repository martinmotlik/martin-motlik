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
2. **"Prefer to listen?"** (last paragraph): EP 02 is integrated
   (2026-10-25), so the line is true. Publish article and episode together.
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

## English copy edit (2026-10-25), items 1–14 applied

A U.S. copy edit of `article.md` and the page-only strings. The author approved
items 1–14 and they are applied in `article.md`, the dek (`build-page.py`, the
cards on `/insights/`) and the Figure 4 caption (`assets.md`); the author adds
them to the Claude doc. The remaining remarks below stay open. Facts check out (14 requirements, 2 failed, 13 elements = 2 + 11,
10 fixed, 3 doors left).

**Errors and misreadings (recommended)**

| # | Where | Now | Fix |
|---|---|---|---|
| 1 | Dek (page) | "connects AI assistants to the software engineers already use" | "The Model Context Protocol (MCP) is an open standard that connects AI assistants to the software that engineers already use." |
| 2 | Intro, ¶2 | "Model Context Protocol, or MCP, … the software and data engineers already use" | "The Model Context Protocol, or MCP, … the software and data that engineers already use" |
| 3 | Why plug in, item 1 | "retest what matters when the model changes" | "… when the AI model changes" |
| 4 | Won't fix, AI-written code | "When a server runs scripts the model writes, the model can write a wrong one." | "When a server runs scripts that the AI writes, some of those scripts will be wrong." |
| 5 | Three kinds of access | "which it describes as use at your own risk" | "which Autodesk describes as \"use at your own risk.\"" |
| 6 | What MCP is, Server | "RFEM, Revit, or an IFC review tool each get their own." | "RFEM, Revit, and an IFC review tool would each get their own." |
| 7 | What MCP is, Prompts | "between version A and B" | "between versions A and B" |
| 8 | Demo | "Two requirements failed, on 13 elements: … eleven doors" / "Ten of the thirteen elements" | "Two requirements failed on 13 elements: … 11 doors" / "Ten of the 13 elements" |
| 9 | Demo | "I asked which requirements fail and which elements are affected." | "… failed … were affected." |
| 10 | Demo | "three residential levels and an attic" | "three residential levels, and an attic" (serial comma, as elsewhere in the body) |
| 11 | Industry, Revu | "[connects to Claude through MCP]" | "an [MCP connection to Claude]" (parallel with the other bullets) |
| 12 | Figure 4 caption | "doors that still miss a fire rating" | "doors that still lack a fire rating" |
| 13 | Why plug in, item 2 | "If that assistant supports the connection you need" ("that" points to the new chatbot) | "If the assistant your firm already has supports the connection you need" |
| 14 | Monday, pilot | "Choose one recurring task and a test model your firm has approved, such as checking a model revision …" | "Choose one recurring task, such as checking a model revision against the project's information requirements, and a test model your firm has approved." |

**Style (optional)**: spell out IDS once ("IDS (Information Delivery
Specification)"); "Read-only access limits changes to the model" appears twice;
"much like a Dynamo or Grasshopper script, except the AI writes it" → "much as a
user would in Dynamo or Grasshopper"; "One outlet finds the elements …" (an
outlet doesn't find anything) → "One server finds …"; "Domain knowledge stays the
competitive advantage, which is exactly where it belongs" → "Domain knowledge
stays where it belongs: with the vendor, as its competitive advantage"; "Anthropic
released the standard in November 2024" repeats the earlier sentence; Figure 2
caption needs the serial comma ("a description the AI reads, and a structured
result"); Figure 6 caption states as a rule what the body hedges ("the answer
does not depend on the chat app" → "the same answer in both").

## Czech and German proofreading (2026-10-25), applied

Independent native-level proofreading of both translations. Applied: CS 62
changes in `article.cs.md` and the strings (meaning: the Experimental server
sentence, „Nic z toho nenahrazuje kontrolní nástroj“, AI vs. BIM model, „trojími
dveřmi“, „mezi verzemi“, „Jaká pravidla pro projekt platí…“; style: calques such as
„úzké nástroje“, „kde žijí nástroje“, „seriózní postupy“; „technical preview“ →
„zkušební verze“, BEP), DE 55 changes (meaning: „Welche Regeln für ein Projekt
gelten…“, KI-Modell vs. Modell, „dessen Nutzung laut Autodesk…“, Brandschutzkonzept
„wird … erst festgelegt“, „Schlechte Daten rein…“, Log instead of Protokoll; style:
„gegen … prüfen“ → „anhand“, „stempelt“ → „unterschreibt“, U-Wert). Not applied:
adding „CCI“ to the classification codes (new content) and removing „(AEC)“ from
`about` (kept on purpose for search).

## Waiting

- **Listed (2026-10-24):** featured and first card on `/insights/`, entry in
  `llms.txt` (with the CS/DE lines and the language table), "Keep reading"
  card in article #1, `sitemap.xml` in all three languages.
- **Release dates:** the article says Oct 22, 2026 and the episode
  2026-10-25 (`podcast/podcast.json` → `published`); set both to the real
  release date when publishing (the feed must not carry a future date).

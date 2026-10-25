# A power outlet for AI: what MCP means for AEC

Insights package `mcp-power-outlet-for-ai` · EP 02 · rules: `.claude/skills/insights-article/SKILL.md`
Check anytime: `python3 tools/insights/check-package.py mcp-power-outlet-for-ai`

| | |
|---|---|
| Article | EN `/insights/mcp-power-outlet-for-ai/` · CS `/cs/insights/mcp-zasuvka-pro-ai-ve-stavebnictvi/` · DE `/de/insights/mcp-steckdose-fuer-ki-im-bauwesen/` |
| Podcast | EP 02 · `podcast/episodes/ep002-power-outlet-for-ai.md` · audio, captions, chapters and cover `assets/podcast/ep002-power-outlet-for-ai.*`, `cover-ep02-v2-*` |
| Social | `social.md` |
| Instagram | `tools/ig-story/teasers/ep002-….json` |
| Drive | (folder link once archived) |
| Branch | `feature/insights-mcp-article` (from `main`) |
| Inputs | text: `article.md` (after feedback, rev 53, from the Claude doc https://claude.ai/artifact/9aafTETYL8eBzdCmNUBJhu, 2026-10-24) · images: `BIM Platform/.claude/worktrees/mcp/article-assets/final/`, figures 02 and 11 redrawn with Claude Design (2026-10-25); metadata in this package's `assets.md` (11 figures, PNG 3840 × 2160, WebP 1920 × 1080)

## Status

- [ ] 1 Brief approved
- [ ] 2 Article text approved · text after feedback received 2026-10-24, no [TK] left, remarks in `REVIEW_NOTES.md`
- [ ] 2 Page built and approved (desktop + phone) · 2026-10-24 built from `article.md` on the GEO template with all figures (`review/`)
- [x] 3 CS + DE translations, `--check` passes (2026-10-24; text in `article.{cs,de}.md` + `i18n-{cs,de}.extras.json` → `i18n-from-md.py`)
- [x] 4 Podcast script approved (production session "AI podcast z scénáře článku")
- [x] 4 Audio delivered (MP3 + transcript .md + .vtt): 14:04.8, 845 s, 20,275,451 B, −16.4 LUFS (final re-export 2026-10-25)
- [x] 5 Episode integrated and previewed (2026-10-25): player, chapter chips, transcript, feed item, JSON-LD audio; publish date in podcast.json set to the release date at release
- [x] 6 Social posts approved (2026-10-25)
- [x] 6 Instagram teaser rendered (`ep002-doors`, 2026-10-25)
- [x] 7 QA done (`check-package.py`, `--check`, JSON-LD, previews EN/CS/DE) · 2026-10-25
- [x] 8 Released 2026-10-25 on the user's instruction (main 83b3d8e), live checks passed
- [x] 9 Archived on Drive 2026-10-25: https://drive.google.com/drive/folders/1_D980LH3I57BgoyWtJQJG7nW2qjH8CWp (3 Docs + 7 files, `package.json` → `drive`)

## Decisions

- 2026-10-24 · Brief from the user covers the EN page; CS/DE, podcast, posts, story and Drive follow as the next phases of this package.
- 2026-10-24 · Article text is the user's and stays word for word; remarks go to `REVIEW_NOTES.md`. Source text, notes, image metadata and review screenshots live here in `_insights/` (any other `.md` in the repo would be published).
- 2026-10-24 · Approved template additions: in-text figure with numbered caption; click to enlarge (link + native `<dialog>`, 3840 px AVIF/WebP, PNG only in Sources/Drive); no wider-than-column figure; code of figure 2 as a `<details>` with the existing code block; the five vendor questions in a `.takeaway`-style card; 16:9 placeholders with the image ID; `[TK …]` highlighted and blocking release; "Keep reading" back on both articles.
- 2026-10-24 · Hero is a composed product image, not Martin in the scene (exception to the hero rule). No `-notext` variant exists; the hero has no text overlay, so the OG crop comes from it directly.
- 2026-10-24 · Not on the page: "Motlar", "Komořanská", "Dlubal CALC" (`package.json` → `forbidden`, checked by `check-package.py`). Images 09, 10 and the interaction video are not in the article.
- 2026-10-24 · The IDS requirement ID "KOM-14" in images 01, 06, 07 and the alt text of 07 stays (user's decision).

- 2026-10-24 · Approved (user): title variant A, "A power outlet for AI: what MCP means for AEC" as H1 and, in Title Case, as `<title>`; meta description A; dek A. The doc keeps its longer working title.

- 2026-10-24 · Approved (user): slugs `/cs/insights/mcp-zasuvka-pro-ai-ve-stavebnictvi/` and `/de/insights/mcp-steckdose-fuer-ki-im-bauwesen/`. Translated titles: „Zásuvka pro AI: co znamená MCP pro AEC“ (CS changed 2026-10-25, below), „Eine Steckdose für KI: Was MCP für AEC bedeutet“.

- 2026-10-25 · Podcast EP 02 (user): the Dlubal line at 10:53 stays as recorded; metadata fixed by the production session (title = article title, show "Insights with Martin Motlík", first chapter "The doors that don't exist" instead of "Cold open"). AI disclosure as in EP 01: text only (feed description, under the transcript, JSON-LD), nothing in the audio or at the player.

- 2026-10-25 · Cover of the article page is the screen-recording video (`assets/video/mcp-article-video-chat.{webm,mp4}`, poster `-poster.webp`; from the session "Obrazové přílohy článku", user's instruction). Muted loop, starts by script; with reduced motion the poster stays with controls. Its label says R03 is a demo revision and the waiting time is sped up. The hero image (`mcp-article-01-hero`) stays for Open Graph, the cards on /insights/ and the podcast page.

- 2026-10-25 · Hero image replaced by the last frame of the cover video (poster PNG 2560 × 1440, user's instruction); still named `mcp-article-01-hero`, so Open Graph, the cards on /insights/, article #1's Keep reading and the podcast page use it. Alt texts updated in EN/CS/DE.

- 2026-10-25 · Closing view added (user, version D) as the last paragraph of "A bridge, not a replacement", before "Prefer to listen?": "My own view: sharing building data with AI models is how they get better at our work, and I trust the large U.S. providers with it. Your contracts still set the rules for each project. In a few years, asking an AI about a model will be as ordinary as searching Google." Added to `article.md` and translated (CS/DE) here; the user adds it to the Claude doc. Not in the podcast.

- 2026-10-25 · Czech version without the abbreviation AEC (user): "stavebnictví", "stavební software"; title „Zásuvka pro AI: co znamená MCP pro stavebnictví“; slug changed before publishing to `/cs/insights/mcp-zasuvka-pro-ai-ve-stavebnictvi/`; the Czech category on the Insights pages is „AI ve stavebnictví“ (menu item and podcast description unchanged).

- 2026-10-25 · Podcast EP 02 re-exported with the closing view in the Close chapter (Sarah 13:20, Martin 13:25, the same words as the article): 14:04.8, 845 s, 20,275,451 B, 103 lines; chapter starts unchanged. Re-exported again the same day from the original approved Close lines plus the two new ones (pronunciation of "MCP" and "AI").

- 2026-10-25 · German version without the abbreviation AEC (user): "Bauwesen", "Bausoftware"; title „Eine Steckdose für KI: Was MCP für das Bauwesen bedeutet“. Slug changed before publishing to `/de/insights/mcp-steckdose-fuer-ki-im-bauwesen/`; the German category on the Insights pages is „KI im Bauwesen“ (menu item unchanged), as in Czech.

- 2026-10-25 · English copy edit items 1–14 approved and applied (user): `article.md`, the dek on the page and the `/insights/` cards, the Figure 4 caption. CS/DE unchanged (the translations already read that way).

- 2026-10-25 · Instagram story (`tools/ig-story/teasers/ep002-doors.json`): the episode's opening hook, 0:00.00–0:14.70 (Martin: the doors that don't exist; Sarah: how do you get an answer you can actually check?), 18.5 s. Design derived from the EP 01 bundle (`Sources/instagram/IG Story - A power outlet for AI.html`: title, date, read time, EP 02, length 14:04, EP 02 cover); photo is the 3D-viewer part of the hero (`Sources/instagram/mcp-ig-story-viewer.png`).
- 2026-10-25 · The IFC review tool is the software I'm developing, not a prototype (user), in all three languages: EN "model-review software", CS „program, který vyvíjím“, DE „Software zur Modellprüfung“ (intro and "What I built"). The podcast transcript keeps "prototype" as recorded. The Claude doc needs the EN change.

- 2026-10-25 · Podcast script and scenes from the production session copied into `podcast/` (from `~/Downloads/insights-podcast-ep2-mcp.md` and `-scenes.json`, 2026-10-24), with the two closing-view lines of the final export added to scene 11.

- 2026-10-25 · Factual wording fixes in EN and CS after publishing (user brief): RFEM 6 MCP server introduced in January 2026 and installed separately (not part of the standard installation); MCP clients per host instead of "one client per app, 25 pieces"; Figure 6 caption limited to this test; the three doors lack a fire-rating value in the model (text, Figure 4 caption, cover video label, Figure 4 and OG alt texts); closing view about access to project data, not model training; standalone chatbot sentence. DE, audio, transcript and podcast.json unchanged. The Figure 1 image itself still says "One client per app, one server per tool."

- 2026-10-25 · New photo for the story teaser (user): the 3D model with a chat card in the site's style (question and answer from the test, dotted link to a red door), `Sources/instagram/mcp-ig-thumb/`; rendered as `IG Story - A power outlet for AI (chat).mp4`. The earlier MP4 stays on Drive.

- 2026-10-25 · Second story teaser, recommended (user chose option 1 of a ranked review of the episode): `ep002-fixed`, 6:17.00–6:41.60, "What got fixed, and what's still missing?" through the three highlighted doors; matches the chat-card photo. 28.4 s. Other candidates: the weekend GitHub server (9:28.5–9:47.4), the big-tech data question (8:05.3–8:29.2), liability (11:50.6–12:07.7).

## Open

- The Claude doc (source of the text) needs the closing paragraph above and the English copy edit items 1–14, so a later export of the doc matches `article.md`.

- Title is 73 characters; the rule is ≤ 60 for the H1 and `<title>`. Two `<title>` variants go to `REVIEW_NOTES.md`.

## Published

- 2026-10-25 · website: https://martinmotlik.com/insights/mcp-power-outlet-for-ai/ · https://martinmotlik.com/cs/insights/mcp-zasuvka-pro-ai-ve-stavebnictvi/ · https://martinmotlik.com/de/insights/mcp-steckdose-fuer-ki-im-bauwesen/ · podcast EP 02 in https://martinmotlik.com/podcast/feed.xml (pubDate 2026-10-25 09:00 +01:00). Release date in the article set to Oct 25, 2026.

(Date · where: LinkedIn, Facebook, X, Threads, Instagram, WhatsApp.)

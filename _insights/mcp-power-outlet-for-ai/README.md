# A power outlet for AI: what MCP means for AEC

Insights package `mcp-power-outlet-for-ai` · EP 02 · rules: `.claude/skills/insights-article/SKILL.md`
Check anytime: `python3 tools/insights/check-package.py mcp-power-outlet-for-ai`

| | |
|---|---|
| Article | EN `/insights/mcp-power-outlet-for-ai/` · CS `/cs/insights/mcp-zasuvka-pro-ai-v-aec/` · DE `/de/insights/mcp-steckdose-fuer-ki-im-aec/` |
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
- [x] 4 Audio delivered (MP3 + transcript .md + .vtt): 13:43, 823 s, 19,761,405 B, −16.4 LUFS (2026-10-25)
- [x] 5 Episode integrated and previewed (2026-10-25): player, chapter chips, transcript, feed item, JSON-LD audio; publish date in podcast.json set to the release date at release
- [ ] 6 Social posts approved
- [ ] 6 Instagram teaser approved and rendered
- [ ] 7 QA done (`check-package.py`, previews EN/CS/DE)
- [ ] 8 Released ("nasaď na produkci"), live checks
- [ ] 9 Archived on Drive, `package.json` → `drive` filled

## Decisions

- 2026-10-24 · Brief from the user covers the EN page; CS/DE, podcast, posts, story and Drive follow as the next phases of this package.
- 2026-10-24 · Article text is the user's and stays word for word; remarks go to `REVIEW_NOTES.md`. Source text, notes, image metadata and review screenshots live here in `_insights/` (any other `.md` in the repo would be published).
- 2026-10-24 · Approved template additions: in-text figure with numbered caption; click to enlarge (link + native `<dialog>`, 3840 px AVIF/WebP, PNG only in Sources/Drive); no wider-than-column figure; code of figure 2 as a `<details>` with the existing code block; the five vendor questions in a `.takeaway`-style card; 16:9 placeholders with the image ID; `[TK …]` highlighted and blocking release; "Keep reading" back on both articles.
- 2026-10-24 · Hero is a composed product image, not Martin in the scene (exception to the hero rule). No `-notext` variant exists; the hero has no text overlay, so the OG crop comes from it directly.
- 2026-10-24 · Not on the page: "Motlar", "Komořanská", "Dlubal CALC" (`package.json` → `forbidden`, checked by `check-package.py`). Images 09, 10 and the interaction video are not in the article.
- 2026-10-24 · The IDS requirement ID "KOM-14" in images 01, 06, 07 and the alt text of 07 stays (user's decision).

- 2026-10-24 · Approved (user): title variant A, "A power outlet for AI: what MCP means for AEC" as H1 and, in Title Case, as `<title>`; meta description A; dek A. The doc keeps its longer working title.

- 2026-10-24 · Approved (user): slugs `/cs/insights/mcp-zasuvka-pro-ai-v-aec/` and `/de/insights/mcp-steckdose-fuer-ki-im-aec/`. Translated titles: „Zásuvka pro AI: co znamená MCP pro AEC“, „Eine Steckdose für KI: Was MCP für AEC bedeutet“.

- 2026-10-25 · Podcast EP 02 (user): the Dlubal line at 10:53 stays as recorded; metadata fixed by the production session (title = article title, show "Insights with Martin Motlík", first chapter "The doors that don't exist" instead of "Cold open"). AI disclosure as in EP 01: text only (feed description, under the transcript, JSON-LD), nothing in the audio or at the player.

- 2026-10-25 · Cover of the article page is the screen-recording video (`assets/video/mcp-article-video-chat.{webm,mp4}`, poster `-poster.webp`; from the session "Obrazové přílohy článku", user's instruction). Muted loop, starts by script; with reduced motion the poster stays with controls. Its label says R03 is a demo revision and the waiting time is sped up. The hero image (`mcp-article-01-hero`) stays for Open Graph, the cards on /insights/ and the podcast page.

- 2026-10-25 · Hero image replaced by the last frame of the cover video (poster PNG 2560 × 1440, user's instruction); still named `mcp-article-01-hero`, so Open Graph, the cards on /insights/, article #1's Keep reading and the podcast page use it. Alt texts updated in EN/CS/DE.

## Open

- Title is 73 characters; the rule is ≤ 60 for the H1 and `<title>`. Two `<title>` variants go to `REVIEW_NOTES.md`.

## Published

(Date · where: LinkedIn, Facebook, X, Threads, Instagram, WhatsApp.)

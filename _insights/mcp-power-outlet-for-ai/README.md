# A power outlet for AI: what MCP is and why AEC professionals will need it

Insights package `mcp-power-outlet-for-ai` · EP 02 · rules: `.claude/skills/insights-article/SKILL.md`
Check anytime: `python3 tools/insights/check-package.py mcp-power-outlet-for-ai`

| | |
|---|---|
| Article | EN `/insights/mcp-power-outlet-for-ai/` · CS `…` · DE `…` |
| Podcast | EP 02 · `podcast/episodes/ep002-….md` |
| Social | `social.md` |
| Instagram | `tools/ig-story/teasers/ep002-….json` |
| Drive | (folder link once archived) |
| Branch | `feature/insights-mcp-article` (from `main`) |
| Inputs | text: `article.md` (final, from the Claude doc https://claude.ai/artifact/9aafTETYL8eBzdCmNUBJhu, 2026-10-24) · images: `BIM Platform/.claude/worktrees/mcp/article-assets/final/` + `assets.md` (11 figures, PNG 3840 × 2160, WebP 1920 × 1080)

## Status

- [ ] 1 Brief approved
- [ ] 2 Article text approved · final text received 2026-10-24, four [TK] left, remarks in `REVIEW_NOTES.md`
- [ ] 2 Page built and approved (desktop + phone) · 2026-10-24 built from `article.md` on the GEO template with all figures (`review/`)
- [ ] 3 CS + DE translations, `--check` passes
- [ ] 4 Podcast script approved
- [ ] 4 Audio delivered (MP3 + transcript .md + .vtt)
- [ ] 5 Episode integrated and previewed
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

## Open

- Title is 73 characters; the rule is ≤ 60 for the H1 and `<title>`. Two `<title>` variants go to `REVIEW_NOTES.md`.

## Published

(Date · where: LinkedIn, Facebook, X, Threads, Instagram, WhatsApp.)

# martinmotlik.com

## Publishing rule: Insights articles and podcast episodes

Every new Insights article ships as one complete package: the article in
EN/CS/DE, the podcast episode (script, audio integration, transcript, feed),
the social post series, an Instagram story teaser and the Google Drive
archive. Follow the `insights-article` skill
(`.claude/skills/insights-article/SKILL.md`); it links the
`insights-social-posts` and `podcast-ig-story` skills for their parts.

- The package lives in `_insights/<article-slug>/` (brief, podcast script and
  scenes, social posts, manifest `package.json`, status README).
  `_insights/ai-visibility-for-aec/` is the reference.
- `python3 tools/insights/check-package.py <slug>` says what is done and
  what is missing. The work is not finished until it passes, including Drive.
- Deploy (push `main`) only after an explicit "nasaď na produkci".

`_insights/` is not published by GitHub Pages (underscore folder). Every
other `.md` file in the repo is served publicly.

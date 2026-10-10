# Insights package tools

Helpers for the `insights-article` skill (`.claude/skills/insights-article/`):
every Insights article ships as a package in `_insights/<slug>/` with its
translations, podcast episode, social posts, Instagram teaser and Drive
archive.

| Command | Does |
|---|---|
| `python3 tools/insights/new-package.py <slug> --title "…"` | Starts `_insights/<slug>/` from the templates (README, brief, podcast script, `package.json`), numbered as the next episode |
| `python3 tools/insights/check-package.py <slug> [--live]` | Lists every deliverable as ✓ / ✗, runs `build-i18n.py --check`; `--live` also checks the published pages and the feed |
| `python3 tools/insights/script-to-scenes.py _insights/<slug>/podcast/script.md [--check]` | Podcast script → `scenes.json` for ElevenLabs Text to Dialogue; character counts, speaking share, estimated length; fails on a scene ≥ 2,000 characters or a production label in a scene title |
| `python3 tools/insights/export-article.py insights/<slug>/index.html [out.md]` | The article as Markdown, for the Google Doc on Drive |
| `python3 tools/insights/drive-stage.py <slug> [--no-upload]` | Uploads the binary deliverables (hero, OG image, MP3, cover, VTT, chapters, story MP4s) into the package's Drive folder with rclone (remote `gdrive`) and records their links in `package.json` |

`_insights/<slug>/package.json` is the manifest these tools read: slug,
episode number, title, URLs, hero name, episode slug, teaser configs,
publish dates and the Drive folder with everything uploaded to it.

---
name: insights-article
description: Plan, write, build, promote and archive a new Insights article on martinmotlik.com together with everything that must ship with it — the CS/DE translations, the podcast episode (two-voice script for ElevenLabs, audio integration, transcript, chapters, cover, feed), the social post series, the Instagram story teaser and the Google Drive archive. Use whenever the user wants a new Insights article or podcast episode ("nový článek", "další díl podcastu", "Insights článek", "publikovat článek"), asks what an article still needs, or asks to check, finish, publish or archive one.
---

# New Insights article — the complete package

Every Insights article ships as one package. **An article is not done until
every item below exists, is committed, is live after an explicit deploy
instruction, and its finished files are on Google Drive.** Article #1
(`ai-visibility-for-aec`, EP 01) is the reference for every item.

| # | Deliverable | Where it lives |
|---|---|---|
| 1 | Brief: topic, audience, core line, title, slugs, sources | `_insights/<slug>/brief.md` |
| 2 | Article, EN, on the site template | `insights/<slug>/index.html` |
| 3 | CS + DE versions with translated slugs | `insights/<slug>/i18n/{cs,de}.json` → generated `cs/…`, `de/…` |
| 4 | Hero photo (+ OG crop), list card, `llms.txt`, sitemap | `Sources/originals/images/`, `assets/img/`, `insights/index.html`, `llms.txt`, `tools/build-i18n.py` |
| 5 | Podcast script + ElevenLabs scenes | `_insights/<slug>/podcast/script.md`, `scenes.json` |
| 6 | Podcast episode on the site and in the feed | `assets/podcast/epNNN-*`, `podcast/episodes/epNNN-*.md`, `podcast/podcast.json` |
| 7 | Social post series, all channels | `_insights/<slug>/social.md` (skill `insights-social-posts`) |
| 8 | Instagram story video with a podcast teaser | `tools/ig-story/teasers/epNNN-*.json` → MP4 (skill `podcast-ig-story`) |
| 9 | Package status, links, Drive folder | `_insights/<slug>/README.md` |
| 10 | Finished files on Google Drive | `Development (Vibe Code)/martinmotlik.com web/Insights/<NN> <slug>/` |

`_insights/` starts with an underscore, so Jekyll (GitHub Pages) never
publishes it, but it is in git and readable on GitHub. Every other `.md` in
the repo is served publicly; never put drafts elsewhere.

## Start or resume

- New article: `python3 tools/insights/new-package.py <slug> --title "<working title>"`
  scaffolds `_insights/<slug>/` from `templates/`.
- Anytime: `python3 tools/insights/check-package.py <slug>` lists what is
  done and what is missing, deliverable by deliverable. Run it at the start
  of every session on an article and before saying anything is finished.
- Read `_insights/<slug>/README.md` first: it holds the decisions and status.

## Phases and gates

Work through the phases in order. A **gate** means: stop, show the user the
result, and continue only after they approve. Record each approval in the
package README.

0. **Generalize the build — once, before article #2.** The build still
   assumes a single article. See `references/article.md` → "Before article #2".
1. **Brief** → `brief.md`. Topic from Martin's own work, audience, one core
   line, title (sentence case, ≤ 60 characters), EN/CS/DE slugs, 3+ primary
   sources. **Gate.**
2. **Article** (`references/article.md`): write the EN text, then build the
   page from the article #1 template. **Gate** on the text before building,
   and on the built page (desktop + phone preview) after.
3. **Translations** (`references/translation.md`): CS and DE JSON, slugs,
   `build-i18n.py --check`.
4. **Podcast script** (`references/podcast.md`): two-voice dialogue built on
   the article, `script.md` + `scenes.json` via `tools/insights/script-to-scenes.py`.
   **Gate.** The user produces the audio in ElevenLabs; you cannot.
5. **Episode** (`references/podcast.md`): check the delivered MP3, transcript
   and VTT, cover, `podcast.json`, build, preview.
6. **Promotion**: social series (`insights-social-posts`), then at least one
   Instagram story teaser (`podcast-ig-story`). **Gate** on the clip choice
   and on the posts.
7. **QA** (`references/release.md`): `check-package.py`, `build-i18n.py --check`,
   preview EN/CS/DE on desktop and phone, links, feed.
8. **Release**: only after the user says **"nasaď na produkci"**. Push
   `main`, verify the live pages and feed (`references/release.md`).
9. **Archive** (`references/drive.md`): upload the finished files to Drive,
   put the folder link and the final status in the package README, commit.

## Rules that apply everywhere

- **Martin's voice**: first person, U.S. English, practical, expert, no hype.
  Experiences, projects and results come only from the user or from what is
  already published. Never invent them. Facts and numbers need a primary
  source.
- **Sarah** is "my co-host Sarah", a fictional AI-voiced character who brings
  a practical case. The AI disclosure is in text only (show description and
  each episode's `disclosure`). No spoken AI note in the audio (the user's
  decision, 2026-10-10).
- **Public labels are not production notes**: no "cold open", "scene",
  "take" or "sting" in chapter titles, transcripts or posts.
- **Never change** a published slug, an episode `guid` or the feed URL.
  GitHub Pages cannot redirect.
- **Git**: one branch per change, imperative commit subjects, bulleted body,
  the Co-Authored-By line. Never commit `services.html`. Run
  `python3 tools/build-i18n.py --check` before every commit that touches the
  site.
- **Deploy** (push to `main`) only on an explicit "nasaď na produkci". "Ulož
  na git" for files outside the site (`_insights/`, `.claude/`, `tools/`) is
  enough to push those.
- **Where data lives**: git holds every text, source and config (article,
  translations, scripts, posts, teaser configs, tools). `Sources/` (gitignored)
  holds full-resolution originals and design bundles. Google Drive holds the
  finished deliverables. Nothing finished exists only in `~/Downloads`.
- Reply to the user in Czech; write the site, scripts and posts in the
  language each item requires.

## References

- `references/article.md`: writing rules, page template, images, list card, `llms.txt`, generalizing the build
- `references/translation.md`: CS/DE JSON, slugs, checks, Czech typography
- `references/podcast.md`: script rules and format, ElevenLabs production notes, episode integration
- `references/release.md`: QA checklist, deploy, post-deploy checks
- `references/drive.md`: Drive layout and upload procedure
- `templates/`: `README.md`, `brief.md`, `script.md` for a new package

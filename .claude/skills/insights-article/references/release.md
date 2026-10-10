# QA, release and checks after release

## Before asking for the deploy

1. `python3 tools/insights/check-package.py <slug>`: everything that can
   exist before release is ✓ (Drive and live checks come after).
2. `python3 tools/build-i18n.py --check` passes.
3. Preview (`.claude/launch.json` → `site-range`, port 4174) EN, CS and DE
   on desktop (1366 px) and phone (375 px): no horizontal scroll, hero
   sharp, TOC links, share buttons, podcast player and chapters, transcript,
   language switcher goes to the translated slug.
4. Every source link opens; every in-text `[N]` jumps to its source.
5. Structured data: valid JSON-LD (no trailing commas), `@id`s as in
   article #1, `citation` matches the source list.
6. The episode's `published` date is not in the future.
7. Report to the user what was checked, with screenshots of the hero and
   the episode card, then ask for the deploy.

## Release

Only after **"nasaď na produkci"**:

```
git checkout main && git merge --ff-only <branch> && git push origin main
```

GitHub Pages publishes `main` in about a minute.

## After release

- Live: the article in EN/CS/DE, `/insights/`, `/insights/podcast/`,
  `sitemap.xml`, `llms.txt` (fetch with `?v=<n>` to skip the cache).
- Feed: `https://martinmotlik.com/podcast/feed.xml` has the new `<item>`;
  the episode appears in Apple Podcasts and Spotify within hours (check the
  show pages linked in `podcast.json` → `show.platforms`).
- Then the promotion goes out (the user posts; the drafts are in
  `social.md`), and the package is archived to Drive (`drive.md`).
- Update the package README: release date, live URLs, what was posted where.

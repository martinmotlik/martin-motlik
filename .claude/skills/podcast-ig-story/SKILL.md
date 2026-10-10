---
name: podcast-ig-story
description: Make an animated Instagram story video (MP4, 1080×1920) that promotes an Insights article with a teaser cut straight from its podcast episode, recorded from a design bundle ("IG Story - ….html"). Use when the user asks for an Instagram/IG story, reel or teaser from the podcast, a "podcast video for Instagram", a "teaser z podcastu", "úryvek z podcastu na Instagram", or wants a different or more attractive clip for an existing story.
---

# Podcast teaser → Instagram story

The tooling is in `tools/ig-story/`; read its `README.md` first. One JSON
config per teaser in `tools/ig-story/teasers/`, one command makes the video.

## Workflow

1. **Design.** The user supplies an exported design bundle (e.g.
   `~/Downloads/IG Story - Be the source.html`). Copy it to
   `Sources/instagram/` (gitignored, 4+ MB) and point `design` at it. Check
   that its animation component still defines `Q_FROM`, `Q_LEN`, `Q_TX`,
   `Q_CHUNKS`, `qAmp`, a `heroImg` resource and the scenes
   Article → Listen → Hold; `prepare.py` asserts each of them.
2. **Photo in full quality.** Use the original from
   `Sources/originals/images/`, never the site's `assets/img/` renditions.
3. **Choose the clip** (or check the one the design names). Judge it as
   marketing for the article, for someone who never heard the episode:
   - hook in the first 1–2 seconds; never start on "That's…", "Because…" or
     another word that needs earlier context
   - one complete thought with a payoff or an open question the article answers
   - 15–30 s; dialogue (question → surprise → answer) beats a monologue
   - read the transcript in `podcast/episodes/<episode>.md`; offer the user
     2–3 ranked options with times when asked which clip is best
4. **Cut in silence.** `python3 tools/ig-story/analyze.py assets/podcast/<ep>.mp3 <from> <to>`.
   Start a few ms before the first word and end inside the pause after the
   last one. VTT cue ends are not safe cut points: they can contain the next
   speaker's first syllable.
5. **Spans and captions.** One span per stretch of speech between measured
   pauses, with its exact text (typographic quotes and apostrophes, as in the
   design). For dialogue set `manual_breaks: true` and break captions by
   meaning with ` | `; short beats like "Wait." or "Right." deserve their own
   caption. Max two lines in the card (~55 characters).
6. **Preview** with `--preview` at the longest captions and the ends of the
   clip; look at the PNGs (crop the card, y 1300–1600) before rendering.
7. **Render** without `--preview`. Then verify from the printed probe:
   1080×1920, 30 fps, avc1 with BT.709, AAC 44.1 kHz stereo, duration =
   Article + clip + Hold; look at the check frames.
8. **Deliver** the MP4 to `~/Downloads/` (don't overwrite an existing file
   without asking) and send it with SendUserFile. Tell the user the clip's
   episode times, the transcript of the clip and where the link sticker goes.
   Add the config to `teasers/` and commit it with any tool changes.
9. **Package**: list the config in `_insights/<slug>/package.json` →
   `teasers`, note the chosen clip in the package README, and archive the MP4
   on Drive (`4 Instagram/`, skill `insights-article` → `references/drive.md`).

## Pitfalls already solved (don't reintroduce)

- No ffmpeg on this Mac: audio is decoded with `afconvert`, video encoded with
  AVFoundation (`encode.swift`).
- The bundle's template lives inside `<script>`: re-encode it with `</`
  escaped as `<\/`, or the page fails with "Unterminated string in JSON".
- The stage must render 1:1 on whole pixels: viewport 1080 × 1965.
- Render every frame from the design's seek event
  (`data-om-seek-to-time-frame`, `sync: true`), never in real time.
- The waveform uses the clip's real loudness envelope and the time in the
  card is the real episode time; keep it that way.

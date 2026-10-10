# The podcast episode: script, production, integration

Show: **Insights with Martin Motlík**. One episode per article, in English,
self-hosted (`assets/podcast/`), in Apple Podcasts and Spotify through the
public feed. Reference: EP 01, script `_insights/ai-visibility-for-aec/podcast/script.md`,
transcript `podcast/episodes/ep001-be-the-source.md`. Technical details of
the site integration: `assets/podcast/README.md`.

## 1. The script

**Format**: two-voice dialogue, U.S. English, 12–15 minutes ≈ 10,000–12,500
characters (EP 01: 11,865 characters → 14:08), 8–10 scenes, each under
2,000 characters (one ElevenLabs request per scene).

**Voices**
- **MARTIN**: the expert, ~70–75 % of the speaking time, his Professional
  Voice Clone.
- **SARAH**: the recurring co-host (same Voice Library voice every episode).
  In each episode she brings one practical case from her side of the market
  (EP 01: marketing lead at a structural engineering firm in Portland). She
  asks how Martin would look at her situation, pushes back once or twice,
  and sums up her plan at the end. She is fictional: never present her case
  as real.

**Structure** (as EP 01)
1. **Opening story** (no intro music before it): Sarah's problem in a few
   lines, ending on a punchline ("One of them has done two. I checked.").
2. "Welcome to Insights. I'm Martin Motlík. I work on websites and content
   for engineering software, for engineers in the U.S., Canada and Europe.
   And today I'm joined by Sarah." Sarah's context, the question of the
   episode, "Let's take it apart."
3. **One scene per article section**, in the article's order, each driven by
   Sarah's case and anchored in one of Martin's real examples from the
   article. Every claim and number comes from the article and its sources.
4. **Close**: "If you had to pick one thing to start with on Monday?", the
   article's key takeaway in Martin's words, Sarah's plan in one breath, the
   CTA ("The full article … is on martinmotlik dot com, under Insights",
   "message me on LinkedIn"), "Thanks for listening." / "See you in the next one."

**Writing rules**
- Spoken language: short sentences, contractions, one idea per line. Read it
  aloud in your head; cut anything that sounds written.
- Real back-and-forth: Sarah's lines are short, Martin's rarely longer than
  four sentences.
- Audio tags in [brackets] are sparse and deliberate: `[laughs]`,
  `[chuckles]`, `[warmly]`, `[gently]`, `[surprised]`. At most one per few
  lines.
- Spell out what TTS mispronounces and list it in the pronunciation table:
  "CSA O-eighty-six", "H-ref-lang", "Merj", "martinmotlik dot com". Never
  spell a word out in the published transcript.
- Plan 2–3 strong 20–30 s moments that work alone (a surprising fact plus a
  reaction). They become the Instagram teasers.
- Scene titles become chapter titles: write them as public chapter names
  ("The gallery problem"), never production labels ("Cold open").

**Files**
- `_insights/<slug>/podcast/script.md` from `templates/script.md`: header
  (format, speakers, Sarah's arc), production notes, pronunciation table,
  then `### Scene N · Title` + `**SPEAKER:** text` lines.
- `python3 tools/insights/script-to-scenes.py _insights/<slug>/podcast/script.md`
  writes `scenes.json` (`[{scene, inputs: [{speaker, text}]}]`, the shape
  ElevenLabs Text to Dialogue takes), updates every scene's character count
  and prints the total, the speaking share per speaker and the estimated
  length. It fails on a scene over 2,000 characters.
- **Gate**: the user approves the script before production.

## 2. Production (done by the user in ElevenLabs)

Hand over `script.md` + `scenes.json` with these notes (also in the template):
Text to Dialogue, Eleven v4 (or the current best model), stability around
the middle, similarity high for MARTIN, 2–3 takes per scene, scenes joined
with 0.4–0.8 s gaps, loudness −16 LUFS, peak ≤ −1 dBFS, MP3 44.1 kHz
128–192 kbps. Ask for the final MP3 plus the transcript as `.md` and `.vtt`
(speaker cues `<v Martin>` / `<v Sarah>`).

## 3. Integration

Follow "Adding an episode" in `assets/podcast/README.md`. In short:

1. **Audio**: `assets/podcast/epNNN-<slug>.mp3`. Check it, don't re-encode:
   duration, loudness (−16 ± 1 LUFS), peak, and that it starts with Sarah's
   story and ends after "See you in the next one".
2. **Captions**: `assets/podcast/epNNN-<slug>.vtt`; the last cue must end
   within 3 s of the audio length.
3. **Transcript**: `podcast/episodes/epNNN-<slug>.md` with `### Title [m:ss]`
   chapters and `**Name** [m:ss]: text` lines. Compare it with the script:
   no audio tags, no phonetic spellings ("CSA O86", not "O-eighty-six").
4. **Cover**: `tools/podcast-cover.html` with tag "EP NN" → 3000 px PNG in
   `Sources/originals/podcast/cover-epNN-v2-3000.png` → `node tools/podcast-covers.mjs`.
5. **`podcast/podcast.json`**: the episode object (`number`, `slug`, `title`
   = article title, `article`, `category`, `published` ISO with offset and
   not in the future at release, `audio`, `duration` in whole seconds,
   `captions`, `transcript`, `cover`, `teaser`, `summary`, `h2` = article H2
   id → chapter start in seconds, `note`, `disclosure`). Copy `note` and
   `disclosure` from EP 01.
6. **Article**: the podcast markers and labels as in article #1; the
   "Podcast · N min" tag on `/insights/`; the teaser and date in
   `insights/podcast/i18n/{cs,de}.json`.
7. `python3 tools/build-i18n.py` (runs `build-podcast.py`: feed, chapters
   JSON, episode card, chips, JSON-LD, podcast page) and `--check`.
8. Preview on the `site-range` dev server (byte ranges, so seeking works):
   play, chapter chips, transcript sync, mini player, on desktop and phone.

The `guid` is built from the slug: never rename the episode slug after
release. Apple Podcasts and Spotify pick new episodes up from the feed on
their own, usually within hours.

# Instagram story teasers from the podcast

An animated 1080×1920 story that announces an Insights article and plays a
short teaser straight from its podcast episode: the article (photo, badge,
headline), then the podcast card with live captions, the voice waveform and
the episode time of the clip, then a hold for the link sticker.

The look comes from a design bundle (exported "Bundled Page", e.g.
`IG Story - Be the source.html`); these scripts only feed it the clip and
record it. Everything runs locally on macOS: Google Chrome draws the frames,
AVFoundation encodes them. No ffmpeg, no npm packages.

## Make a video

```
python3 tools/ig-story/ig-story.py tools/ig-story/teasers/ep001-invisible.json --preview 5.5,14.5,25
python3 tools/ig-story/ig-story.py tools/ig-story/teasers/ep001-invisible.json
```

`--preview` renders only those story times as PNG into
`Sources/exports/ig-story/<teaser>/preview/`. Without it the whole story is
rendered (~3 frames per second) and written to the config's `output`, and the
tracks and three check frames are printed and saved.

## A new teaser

1. **Pick the moment.** It has to work for someone who has not heard the
   episode: a hook in the first two seconds, one complete thought, a payoff
   or an open question that the article answers. 15–30 s. A dialogue
   (question, surprise, answer) holds attention better than a monologue.
2. **Find the cuts.**
   `python3 tools/ig-story/analyze.py assets/podcast/<episode>.mp3 <from> <to>`
   lists the pauses and the caption cues. Start and end inside a pause, never
   on a cue boundary: a cue end can already hold the next speaker's first
   syllable.
3. **Write the config** in `teasers/` (copy one):

   | key | |
   |---|---|
   | `design` | the design bundle (kept in `Sources/instagram/`, gitignored) |
   | `photo` | full-quality photo for the design's `heroImg` |
   | `episode` | the episode MP3 |
   | `output` | where the MP4 goes |
   | `from`, `len` | the clip, in episode seconds |
   | `spans` | `[start, end, text]` per stretch of speech between two pauses; words are spread over it by length |
   | `manual_breaks` | true: a caption ends at every span end and at each ` \| ` in the text. false: the automatic rule (sentence end, comma after 4 words, 7 words) |
   | `variant` | the design's variant, e.g. `A · Photo` |

   Captions hold at most two lines in the card (about 55 characters).
4. **Preview, then render.** Check the frames where the longest captions
   show, and that the time in the card runs from the clip's start to its end.

## Files

| | |
|---|---|
| `ig-story.py` | runs everything below for one config |
| `analyze.py` | pauses and caption cues in a stretch of an episode |
| `prepare.py` | cuts the audio, measures the voice envelope and word timings, patches the design |
| `render.mjs` | headless Chrome, one PNG per frame via the design's seek event |
| `encode.swift` | PNG frames + WAV → MP4 (H.264 High ~15–20 Mbit/s, BT.709, AAC 44.1 kHz) |
| `probe.swift` | prints the MP4's tracks, saves check frames |
| `teasers/*.json` | one config per published teaser |

Work files (decoded episode, patched page, frames, check frames, compiled
Swift tools) live in `Sources/exports/ig-story/`, which git ignores.

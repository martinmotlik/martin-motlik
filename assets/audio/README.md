# Voice-over audio

Each Insights article can carry a narrated version. The player on the article
page is **hidden until the file below loads and reports a duration**, so a
visitor is never shown a control with nothing behind it.

| Article | File |
|---|---|
| `/insights/ai-visibility-for-aec/` | `ai-visibility-for-aec.m4a` |

The duration shown in the player comes from the file itself, so nothing needs
to be edited in the HTML when a file is replaced. To point an article at a
different file, change `data-src` on `#vo` in that article's `index.html`.

## Format

AAC in an `.m4a` container, mono, 44.1 kHz, 96 kbps. Every current browser
plays it. macOS has no MP3 encoder built in (CoreAudio only decodes MP3), and
AAC is the better codec for speech at these bitrates anyway.

The player only fetches metadata until the visitor presses play
(`preload="metadata"`), so file size does not affect page load.

## Mastering spec

What `ai-visibility-for-aec.m4a` was mastered to, and what any future voice-over
should match so all articles play at the same level:

| | Target | `ai-visibility-for-aec.m4a` (measured after AAC decode) |
|---|---|---|
| Integrated loudness | −16 LUFS (podcast / Apple standard) | −15.98 LUFS |
| True peak | ≤ −1 dBTP | −1.90 dBTP |
| Loudness range | 3–5 LU | 2.9 LU — narrower than the parts' 4.4 LU mainly because the 1.9 LU level differences between parts were removed |
| Level step at a join | below the voice's own variation (median 0.57 LU) | 0.05–0.14 LU |
| Gap between joined parts | between the voice's p90 pause and its longest | 0.75 s of room tone |
| Tonal balance vs source | no dulling | 3 kHz +0.1 dB, 5–9 kHz +0.7 to +1.9 dB |

Source: four parts generated in ElevenLabs (mono MP3, 44.1 kHz, 128 kbps),
8:53 when joined. They arrived clean and consistent — noise floor −86 dBFS, no
sibilance peak, the same timbre in every part, steady level within each part —
so there is no noise reduction, de-essing or EQ. What they did need:

1. **Loudness.** −21 to −23 LUFS, 5–7 dB short of −16, with peaks already at
   −1.2 dBFS — plain gain could add only 0.2 dB, so the rest needs peak control.
2. **Gaps.** Plain concatenation left 0.10–0.17 s between topics, shorter than
   the voice's ordinary sentence pause (0.30 s).
3. **One join.** Part 1 → 2 stepped up 1.9 LU, above the voice's own p90 of 1.4 LU.

Chain used: edge trim → 75 Hz high-pass → per-part loudness match → look-ahead
transient limiter on the top 2 % of samples (short consonant onsets) → 2.5:1
compressor, 5 ms attack (barely engaged: 0.3 dB mean) → assembly with room-tone
gaps and 8 ms fades → closed loop of −16 LUFS normalisation, slow gain ramps
that close each join, and a look-ahead safety limiter at −2.0 dBFS (room for the
~0.75 dB AAC overshoot; it never engaged on this file) → TPDF dither.

Parts start in the joined file at 0:00.0, 1:44.7, 4:58.6 and 6:43.3.

The 16-bit WAV master (`ai-visibility-for-aec-master.wav`, 47 MB) is kept
outside the repository; re-encode from it rather than from the `.m4a`.

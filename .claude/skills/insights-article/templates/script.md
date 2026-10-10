# Insights Podcast – Episode {{nn}}
## "{{title}}"

**Format:** Two-voice dialogue · U.S. English · ~14 minutes · ~11,000–12,500 characters in 8–10 scenes
**Speakers:**
- **MARTIN:** the expert. Martin's Professional Voice Clone, about 70–75 % of the speaking time.
- **SARAH:** the recurring co-host (the same Voice Library voice as EP 01). This episode she is … (her role and firm). Her case runs through the whole episode, and she keeps asking how Martin sees it.

**Source article:** https://martinmotlik.com/insights/{{slug}}/

**Sarah's story arc**
1. (her problem, ends on a punchline)
2. …

---

## Production notes

**Voices**: MARTIN = Professional Voice Clone; SARAH = the same Voice Library voice as in EP 01.

**Model & settings**
- Text to Dialogue, Eleven v4 (or the current best model).
- Stability around the middle. Similarity high for MARTIN.
- One scene = one request (every scene is under 2,000 characters). Generate 2–3 takes per scene and pick the best.
- Audio tags in [brackets] are deliberate and sparse. Don't add more.
- `scenes.json` next to this file is the same script in the Text to Dialogue shape (made by `tools/insights/script-to-scenes.py`).

**Pronunciation (already spelled out in the script)**
| In the article | In the script |
|---|---|
| martinmotlik.com | martinmotlik dot com |
| Motlík | Check the first take. If wrong, try "MOT-leek". |

**Post-production**
- Join scenes with 0.4–0.8 s gaps. No music before the opening story.
- Normalize to −16 LUFS (stereo), peak ≤ −1 dBFS, export MP3 44.1 kHz 128–192 kbps.
- Deliver: the MP3, and the transcript as `.md` (chapters `### Title [m:ss]`, lines `**Name** [m:ss]: text`) and `.vtt` (`<v Martin>` / `<v Sarah>`), without audio tags and phonetic spellings.

**Disclosure**: in text only (show description and the episode's `disclosure` in `podcast/podcast.json`). Nothing spoken.

---

## Script

### Scene 1 · (public chapter title)

**SARAH:** …

**MARTIN:** …

**MARTIN:** [warmly] Welcome to Insights. I'm Martin Motlík. I work on websites and content for engineering software, for engineers in the U.S., Canada and Europe. And today I'm joined by Sarah.

---

### Scene N · Close

**SARAH:** If you had to pick one thing for me to start with on Monday?

**MARTIN:** …

**SARAH:** The full article … is on martinmotlik dot com, under Insights.

**MARTIN:** And if you're working on something similar, … message me on LinkedIn. I'm always happy to compare notes.

**SARAH:** Thanks for listening.

**MARTIN:** [warmly] See you in the next one.

"""Finds the pauses in a stretch of a podcast episode, to cut a teaser in silence.

    python3 tools/ig-story/analyze.py <episode.mp3|.wav> <from s> <to s> [--db -45] [--min-ms 60]

Prints every pause (loudness below --db for at least --min-ms) between the two
times, in episode seconds and as m:ss.ss, and the caption cues of the episode's
.vtt for the same stretch when it lies next to the audio. Speech spans for a
teaser config are the stretches between consecutive pauses. VTT cue times are
approximate: a cue end can already contain the next speaker's first syllable,
so always cut in a measured pause.
"""
import argparse, array, math, os, re, subprocess, sys, tempfile, wave

p = argparse.ArgumentParser()
p.add_argument('audio'); p.add_argument('start', type=float); p.add_argument('end', type=float)
p.add_argument('--db', type=float, default=-45); p.add_argument('--min-ms', type=int, default=60)
a = p.parse_args()

src = a.audio
if not src.lower().endswith('.wav'):
    tmp = os.path.join(tempfile.gettempdir(), 'ig-story-' + os.path.basename(src) + '.wav')
    if not os.path.exists(tmp):
        subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@44100', src, tmp], check=True)
    src = tmp

w = wave.open(src)
sr, ch = w.getframerate(), w.getnchannels()
w.setpos(int(a.start * sr))
x = array.array('h', w.readframes(int((a.end - a.start) * sr)))
hop = sr // 100                                   # 10 ms
mono = (lambda j: (x[2 * j] + x[2 * j + 1]) / 2) if ch == 2 else (lambda j: x[j])
levels = []
for i in range(0, len(x) // ch - hop, hop):
    s = sum(mono(j) ** 2 for j in range(i, i + hop))
    levels.append(20 * math.log10(max(math.sqrt(s / hop), 1) / 32768))

clock = lambda t: f'{int(t // 60)}:{t % 60:05.2f}'
print(f'pauses below {a.db:.0f} dB, at least {a.min_ms} ms:')
start = None
for k, db in enumerate(levels + [0]):
    if db < a.db and start is None:
        start = k
    elif db >= a.db and start is not None:
        if (k - start) * 10 >= a.min_ms:
            t0, t1 = a.start + start / 100, a.start + k / 100
            print(f'  {t0:8.2f} – {t1:8.2f}   {clock(t0)} – {clock(t1)}   {(t1 - t0) * 1000:4.0f} ms')
        start = None

vtt = os.path.splitext(a.audio)[0] + '.vtt'
if os.path.exists(vtt):
    sec = lambda h, m, s: int(h) * 3600 + int(m) * 60 + float(s)
    print('\ncaption cues:')
    for m in re.finditer(r'(\d+):(\d+):([\d.]+) --> (\d+):(\d+):([\d.]+)\n(.+)', open(vtt, encoding='utf-8').read()):
        t0, t1 = sec(*m.group(1, 2, 3)), sec(*m.group(4, 5, 6))
        if t1 > a.start and t0 < a.end:
            print(f'  {t0:8.2f} – {t1:8.2f}  {m.group(7)}')

"""Makes an Instagram story MP4 from a teaser config, end to end.

    python3 tools/ig-story/ig-story.py tools/ig-story/teasers/<name>.json            # final video
    python3 tools/ig-story/ig-story.py tools/ig-story/teasers/<name>.json --preview 5.5,14.5   # a few frames only

1. decodes the episode MP3 to WAV (afconvert, cached)
2. prepare.py: audio track + patched design page (see there)
3. render.mjs: headless Chrome draws every frame at 1080×1920
4. encode.swift: H.264 + AAC MP4 via AVFoundation (no ffmpeg needed)
5. probe.swift: prints the tracks of the result and saves three check frames

Work files go to Sources/exports/ig-story/<name>/ (gitignored); the frames
are deleted after a successful encode unless --keep is given. The MP4 goes to
the config's "output" path.
"""
import argparse, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
p = argparse.ArgumentParser()
p.add_argument('config')
p.add_argument('--preview', help='comma-separated story times in seconds: render only these frames as PNG')
p.add_argument('--keep', action='store_true', help='keep the rendered frames')
a = p.parse_args()

cfg = json.load(open(a.config, encoding='utf-8'))
name = os.path.splitext(os.path.basename(a.config))[0]
work = os.path.join(ROOT, 'Sources', 'exports', 'ig-story', name)
bins = os.path.join(ROOT, 'Sources', 'exports', 'ig-story', 'bin')
os.makedirs(work, exist_ok=True); os.makedirs(bins, exist_ok=True)
run = lambda *cmd: subprocess.run(list(cmd), check=True)
fps = str(cfg.get('fps', 30))

episode = os.path.join(ROOT, cfg['episode'])
wav = os.path.join(os.path.dirname(work), os.path.basename(episode) + '.wav')
if not os.path.exists(wav) or os.path.getmtime(wav) < os.path.getmtime(episode):
    run('afconvert', '-f', 'WAVE', '-d', 'LEI16@44100', episode, wav)

run(sys.executable, os.path.join(HERE, 'prepare.py'), a.config, wav, work)
total = str(json.load(open(os.path.join(work, 'timing.json')))['total'])
page = os.path.join(work, 'story.html')

if a.preview:
    out = os.path.join(work, 'preview')
    shutil.rmtree(out, ignore_errors=True)
    run('node', os.path.join(HERE, 'render.mjs'), page, out, fps, total, a.preview)
    print('preview frames in', out)
    sys.exit(0)

for tool in ('encode', 'probe'):
    src, exe = os.path.join(HERE, tool + '.swift'), os.path.join(bins, tool)
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        run('swiftc', '-O', '-swift-version', '5', src, '-o', exe)

frames = os.path.join(work, 'frames')
shutil.rmtree(frames, ignore_errors=True)
run('node', os.path.join(HERE, 'render.mjs'), page, frames, fps, total)
output = os.path.expanduser(cfg['output'])
run(os.path.join(bins, 'encode'), frames, os.path.join(work, 'audio.wav'), output, fps)
t = float(total)
run(os.path.join(bins, 'probe'), output, work, f'{min(3.0, t / 4):.1f},{t / 2:.1f},{t - 0.4:.1f}')
if not a.keep:
    shutil.rmtree(frames)
print('\nvideo:', output, '\ncheck frames:', work)

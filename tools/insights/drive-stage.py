"""Collects the finished binary files of an Insights package for Google Drive.

    python3 tools/insights/drive-stage.py <slug>

Text deliverables (article, transcript, social posts) are uploaded by Claude
through the Google Drive connector as Google Docs. Binary ones are too large
for the connector, so this script gathers them in the Drive folder layout:

    <NN slug · short name>/
      1 Article/    hero original (full resolution), OG image
      2 Podcast/    episode MP3, cover 3000 px, captions .vtt, chapters .json
      4 Instagram/  every rendered story MP4 of the package's teasers

If Google Drive for desktop is installed, the files are copied straight into
the synced folder (My Drive/Development (Vibe Code)/martinmotlik.com web/
Insights/…), which uploads them; otherwise they are staged in
Sources/exports/drive/ for drag and drop into the Drive folder from
package.json. Either way the script prints what went where; record uploads in
package.json → drive.uploaded (Claude verifies them with the connector).
"""
import glob, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRIVE_PATH = ('My Drive', 'Development (Vibe Code)', 'martinmotlik.com web', 'Insights')
slug = sys.argv[1]
pkg = json.load(open(os.path.join(ROOT, '_insights', slug, 'package.json'), encoding='utf-8'))
rel = lambda p: os.path.join(ROOT, p.lstrip('/'))
folder = pkg['drive']['folder']

files = []                      # (subfolder, source path)
hero = pkg.get('hero')
if hero:
    files += [('1 Article', rel(f'Sources/originals/images/{hero}.jpg')), ('1 Article', rel(f'assets/img/{hero}-og-1200.jpg'))]
pod = json.load(open(rel('podcast/podcast.json'), encoding='utf-8'))
ep = next((e for e in pod['episodes'] if e['slug'] == pkg.get('episode')), None)
if ep:
    files += [('2 Podcast', rel(ep['audio'])), ('2 Podcast', rel(ep['cover'] + '-3000.jpg')),
              ('2 Podcast', rel(ep['captions'])), ('2 Podcast', rel(f'assets/podcast/{ep["slug"]}.chapters.json'))]
for t in pkg.get('teasers', []):
    out = os.path.expanduser(json.load(open(rel(t), encoding='utf-8'))['output'])
    files.append(('4 Instagram', out))

synced = glob.glob(os.path.expanduser('~/Library/CloudStorage/GoogleDrive-*'))
if synced:
    base = os.path.join(synced[0], *DRIVE_PATH, folder)
    how = 'copied into Google Drive for desktop (uploads on its own)'
else:
    base = os.path.join(ROOT, 'Sources', 'exports', 'drive', folder)
    how = 'staged locally: drag each subfolder\'s files into the same subfolder on Drive'

print(f'{folder}: {how}\n  {base}\n  Drive: {pkg["drive"].get("url", "(no folder yet)")}\n')
missing = 0
for sub, src in files:
    if not os.path.exists(src):
        print(f'  ✗ {sub}/{os.path.basename(src)}  missing: {src}')
        missing += 1
        continue
    dst = os.path.join(base, sub, os.path.basename(src))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
        shutil.copy2(src, dst)
    print(f'  ✓ {sub}/{os.path.basename(src)}  {os.path.getsize(src) / 1e6:.1f} MB')
sys.exit(1 if missing else 0)

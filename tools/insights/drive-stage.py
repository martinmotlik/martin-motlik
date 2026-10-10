"""Uploads the finished binary files of an Insights package to Google Drive.

    python3 tools/insights/drive-stage.py <slug> [--no-upload]

Text deliverables (article, transcript, social posts) are uploaded by Claude
through the Google Drive connector as Google Docs. Binary ones are too large
for the connector, so this script gathers them in the Drive folder layout:

    <NN slug · short name>/
      1 Article/    hero original (full resolution), OG image
      2 Podcast/    episode MP3, cover 3000 px, captions .vtt, chapters .json
      4 Instagram/  every rendered story MP4 of the package's teasers

They are staged in Sources/exports/drive/<folder>/ and uploaded with rclone
(remote "gdrive", rooted at the Drive folder Insights; setup in
.claude/skills/insights-article/references/drive.md): `rclone copy` skips
files that are already there with the same size and checksum. Every file
found in the package's Drive folder afterwards is recorded in package.json →
drive.uploaded with its link. Without rclone, Google Drive for desktop is
used when installed; otherwise the files stay staged for drag and drop.
"""
import glob, json, os, shutil, subprocess, sys

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

RCLONE = shutil.which('rclone') or os.path.expanduser('~/.local/bin/rclone')
has_rclone = os.path.exists(RCLONE) and 'gdrive:' in subprocess.run([RCLONE, 'listremotes'], capture_output=True, text=True).stdout
upload = has_rclone and '--no-upload' not in sys.argv
synced = glob.glob(os.path.expanduser('~/Library/CloudStorage/GoogleDrive-*'))
if synced and not has_rclone:
    base = os.path.join(synced[0], *DRIVE_PATH, folder)
    how = 'copied into Google Drive for desktop (uploads on its own)'
else:
    base = os.path.join(ROOT, 'Sources', 'exports', 'drive', folder)
    how = 'staged, uploading with rclone' if upload else 'staged locally: drag each subfolder\'s files into the same subfolder on Drive'

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

if upload:
    remote = f'gdrive:{folder}'
    r = subprocess.run([RCLONE, 'copy', base, remote, '--checksum', '--log-level', 'ERROR', '--stats-one-line', '-P'])
    if r.returncode:
        sys.exit('rclone copy failed')
    listing = json.loads(subprocess.run([RCLONE, 'lsjson', '-R', '--files-only', remote, '--log-level', 'ERROR'],
                                        capture_output=True, text=True, check=True).stdout)
    up = pkg['drive'].setdefault('uploaded', {})
    for f in listing:
        name = f['Path']
        if f.get('MimeType', '').startswith('application/vnd.google-apps.') or name.endswith('.docx'):
            continue                                  # Google Docs are recorded when created
        up[name] = f'https://drive.google.com/file/d/{f["ID"]}/view'
    pkg_path = os.path.join(ROOT, '_insights', slug, 'package.json')
    json.dump(pkg, open(pkg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(pkg_path, 'a').write('\n')
    print(f'\nuploaded; {len(up)} files recorded in _insights/{slug}/package.json → drive.uploaded')
sys.exit(1 if missing else 0)

"""Checks that an Insights package is complete: every deliverable, item by item.

    python3 tools/insights/check-package.py <slug> [--live]

Reads _insights/<slug>/package.json and checks the files in the repo (article
and translations, build registration, images, listing, llms.txt, podcast
episode, feed, social posts, Instagram teasers, package documents, Drive).
--live also fetches the published pages and the feed. Exit code 1 if
anything required is missing. The rules behind each check are in
.claude/skills/insights-article/.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = 'https://martinmotlik.com'
slug = sys.argv[1]
live = '--live' in sys.argv
pkg_dir = os.path.join(ROOT, '_insights', slug)
rel = lambda p: os.path.join(ROOT, p.lstrip('/'))
read = lambda p: open(rel(p), encoding='utf-8').read() if os.path.exists(rel(p)) else ''
results = []


def check(group, label, ok, hint=''):
    results.append((group, label, bool(ok), hint))


if not os.path.exists(os.path.join(pkg_dir, 'package.json')):
    sys.exit(f'_insights/{slug}/package.json is missing: run tools/insights/new-package.py {slug}')
pkg = json.load(open(os.path.join(pkg_dir, 'package.json'), encoding='utf-8'))
urls = pkg.get('urls', {})
en = urls.get('en', f'/insights/{slug}/')

# 1 · package documents
for f, why in (('README.md', 'status and decisions'), ('brief.md', 'brief (phase 1)'), ('social.md', 'social posts (skill insights-social-posts)'),
               ('podcast/script.md', 'podcast script (phase 4)'), ('podcast/scenes.json', 'scenes for ElevenLabs (script-to-scenes.py)')):
    check('Package', f'_insights/{slug}/{f}', os.path.exists(os.path.join(pkg_dir, f)), why)

# 2 · article + translations
page = read(en + 'index.html')
check('Article', f'page {en}index.html', page)
if page:
    title = re.search(r'<title>(.*?)</title>', page, re.S)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', page, re.S)
    strip = lambda s: re.sub(r'<[^>]+>|\s+', ' ', s).strip()
    check('Article', '<title> = H1 word for word (Title Case), ≤ 60 characters', title and h1 and strip(title.group(1)).lower() == strip(h1.group(1)).lower() and len(strip(title.group(1))) <= 60,
          f'{strip(title.group(1)) if title else "?"}')
    check('Article', 'exactly four article:tag', len(re.findall(r'property="article:tag"', page)) == 4)
    check('Article', 'TechArticle JSON-LD with citations', '"TechArticle"' in page and '"citation"' in page)
    check('Article', 'sources list', 'class="src-list"' in page or 'class="sources"' in page)
    check('Article', 'podcast markers', '<!-- podcast:start' in page and '<!-- toc-pod:start' in page)
for lang in ('cs', 'de'):
    check('Translations', f'insights/{slug}/i18n/{lang}.json', os.path.exists(rel(f'insights/{slug}/i18n/{lang}.json')))
    if urls.get(lang):
        check('Translations', f'generated {urls[lang]}', os.path.exists(rel(urls[lang] + 'index.html')))
build = read('tools/build-i18n.py')
art = re.search(r"^ARTICLE = '([^']+)'", build, re.M)
known = lambda block: (f"'{en}'" in block) or (art and art.group(1) == en and 'ARTICLE' in block)
urls_block = re.search(r'^URLS = \{.*?^\}', build, re.S | re.M)
sitemap_block = re.search(r'^SITEMAP = \{.*?^\}', build, re.S | re.M)
check('Site', 'slugs in build-i18n.py URLS', urls_block and known(urls_block.group(0)))
check('Site', 'SITEMAP entry in build-i18n.py', sitemap_block and known(sitemap_block.group(0)))
check('Site', 'sitemap.xml lists it', SITE + en in read('sitemap.xml'))
check('Site', 'card on /insights/', f'href="{en}"' in read('insights/index.html'))
check('Site', 'llms.txt entry', SITE + en in read('llms.txt'))
hero = pkg.get('hero', '')
check('Site', f'hero renditions assets/img/{hero}-*', hero and os.path.exists(rel(f'assets/img/{hero}-og-1200.jpg')) and any(
    f.startswith(hero + '-') and f.endswith('.avif') for f in os.listdir(rel('assets/img'))))
check('Site', f'hero original Sources/originals/images/{hero}.jpg', hero and os.path.exists(rel(f'Sources/originals/images/{hero}.jpg')), 'gitignored, local only')

# 3 · podcast
pod = json.loads(read('podcast/podcast.json') or '{}')
ep = next((e for e in pod.get('episodes', []) if e.get('slug') == pkg.get('episode') or e.get('article') == en), None)
check('Podcast', 'episode in podcast/podcast.json', ep)
if ep:
    for key in ('audio', 'captions'):
        check('Podcast', f'{key}: {ep[key]}', os.path.exists(rel(ep[key])))
    check('Podcast', f'transcript: {ep["transcript"]}', os.path.exists(rel(ep['transcript'])))
    check('Podcast', 'chapters JSON', os.path.exists(rel(f'assets/podcast/{ep["slug"]}.chapters.json')))
    check('Podcast', f'cover {ep["cover"]}-3000.jpg', os.path.exists(rel(ep['cover'] + '-3000.jpg')))
    check('Podcast', 'h2 map points at article sections', ep.get('h2') and all(f'id="{h}"' in page for h in ep['h2']))
    check('Podcast', 'disclosure text', ep.get('disclosure'))
    tr = read(ep['transcript'])
    check('Podcast', 'no production labels in chapter titles', not re.search(r'(?im)^### .*\b(cold open|scene|take|sting)\b', tr))
    feed = read('podcast/feed.xml')
    check('Podcast', 'item in podcast/feed.xml', f'podcast/{ep["slug"]}<' in feed or ep['slug'] in feed)

# 4 · promotion
social = read(f'_insights/{slug}/social.md')
for h in ('LinkedIn: long', 'LinkedIn: short', 'LinkedIn: first comment', 'Facebook', '## X', 'Threads', 'Instagram story', 'WhatsApp'):
    check('Social', f'social.md: {h.strip("# ")}', h in social)
teasers = pkg.get('teasers', [])
check('Instagram', 'at least one teaser config', teasers)
for t in teasers:
    ok = os.path.exists(rel(t))
    out = os.path.expanduser(json.load(open(rel(t), encoding='utf-8'))['output']) if ok else ''
    check('Instagram', f'{t}', ok)
    check('Instagram', f'video {os.path.basename(out)}', out and os.path.exists(out), 'render with tools/ig-story/ig-story.py')

# 5 · archive
drive = pkg.get('drive', {})
check('Drive', 'Drive folder recorded', drive.get('url'))
up = [k.lower() for k in drive.get('uploaded', {})]
for sub, need, pattern in (('1 Article', 'article text', 'article'), ('1 Article', 'hero photo', '.jpg'),
                           ('2 Podcast', 'episode MP3', '.mp3'), ('2 Podcast', 'transcript', 'transcript'), ('2 Podcast', 'cover', 'cover'),
                           ('3 Social', 'social posts', 'social'), ('4 Instagram', 'story video', '.mp4')):
    check('Drive', f'{sub}: {need}', any(k.startswith(sub.lower() + '/') and pattern in k for k in up), 'see references/drive.md')

# 6 · build + live
r = subprocess.run([sys.executable, rel('tools/build-i18n.py'), '--check'], capture_output=True, text=True, cwd=ROOT)
check('Build', 'build-i18n.py --check', r.returncode == 0, (r.stdout + r.stderr).strip()[-200:])
if live:
    curl = lambda u, *a: subprocess.run(['curl', '-s', '-m', '20', *a, f'{SITE}{u}?v={os.getpid()}'], capture_output=True, text=True).stdout
    for lang, u in urls.items():
        code = curl(u, '-o', '/dev/null', '-w', '%{http_code}')
        check('Live', f'{SITE}{u}', code == '200', code)
    if ep:
        check('Live', 'episode in the live feed', ep['slug'] in curl('/podcast/feed.xml'))

group = None
missing = 0
for g, label, ok, hint in results:
    if g != group:
        print(f'\n{g}'); group = g
    print(f'  {"✓" if ok else "✗"} {label}' + (f'  ({hint})' if hint and not ok else ''))
    missing += not ok
print(f'\n{len(results) - missing}/{len(results)} done' + (f', {missing} missing' if missing else ', package complete'))
sys.exit(1 if missing else 0)

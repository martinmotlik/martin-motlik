"""Starts the package of a new Insights article.

    python3 tools/insights/new-package.py <slug> --title "<working title>"

Creates _insights/<slug>/ with README.md, brief.md, podcast/script.md (from
.claude/skills/insights-article/templates/) and package.json, numbered as the
next podcast episode. Refuses to touch an existing package.
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TPL = os.path.join(ROOT, '.claude', 'skills', 'insights-article', 'templates')
p = argparse.ArgumentParser()
p.add_argument('slug'); p.add_argument('--title', required=True)
a = p.parse_args()
if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', a.slug):
    sys.exit('slug: lowercase ASCII words joined by hyphens')
pkg = os.path.join(ROOT, '_insights', a.slug)
if os.path.exists(pkg):
    sys.exit(f'{pkg} exists already')

pod = json.load(open(os.path.join(ROOT, 'podcast', 'podcast.json'), encoding='utf-8'))
n = max((e['number'] for e in pod['episodes']), default=0) + 1
vals = {'slug': a.slug, 'title': a.title, 'nn': f'{n:02d}', 'nnn': f'{n:03d}'}
fill = lambda s: re.sub(r'\{\{(\w+)\}\}', lambda m: vals[m.group(1)], s)

os.makedirs(os.path.join(pkg, 'podcast'))
for src, dst in (('README.md', 'README.md'), ('brief.md', 'brief.md'), ('script.md', 'podcast/script.md')):
    open(os.path.join(pkg, dst), 'w', encoding='utf-8').write(fill(open(os.path.join(TPL, src), encoding='utf-8').read()))
json.dump({
    '_about': 'Manifest of one Insights package. Read by tools/insights/check-package.py and drive-stage.py; rules in .claude/skills/insights-article/SKILL.md.',
    'slug': a.slug, 'number': n, 'title': a.title, 'short_name': '', 'category': '', 'core_line': '',
    'urls': {'en': f'/insights/{a.slug}/', 'cs': '', 'de': ''},
    'hero': '', 'episode': '', 'teasers': [], 'published': {'article': '', 'episode': ''},
    'drive': {'folder': f'{n:02d} {a.slug} · ', 'url': '', 'id': '', 'subfolders': {}, 'uploaded': {}},
}, open(os.path.join(pkg, 'package.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'created _insights/{a.slug}/ (EP {n:02d}): README.md, brief.md, podcast/script.md, package.json')
print(f'next: fill brief.md, then git checkout -b {a.slug}')

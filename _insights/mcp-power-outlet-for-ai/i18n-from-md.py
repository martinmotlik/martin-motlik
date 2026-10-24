"""Builds insights/mcp-power-outlet-for-ai/i18n/<lang>.json from the
translated text, so the CS and DE pages follow the article block for block.

    python3 _insights/mcp-power-outlet-for-ai/i18n-from-md.py cs
    python3 _insights/mcp-power-outlet-for-ai/i18n-from-md.py de

Reads article.<lang>.md (the translation of article.md: the same headings,
paragraphs, lists, links, bold and code, in the same order; figure notes
copied as they are) and i18n-<lang>.extras.json (hero, contents, figure
captions, tags, closing, chrome, ui, meta, keep). Labels the GEO article
already translates (navigation, share, player) come from its JSON. The keys
are generated exactly as build-page.py generates them for the English page,
and the script stops if they differ. Then run tools/build-i18n.py.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PKG = os.path.join(ROOT, '_insights', 'mcp-power-outlet-for-ai')
PAGE = os.path.join(ROOT, 'insights', 'mcp-power-outlet-for-ai')
lang = sys.argv[1]
assert lang in ('cs', 'de')

SECTION_IDS = ['cant-open', 'what-mcp-is', 'why-aec', 'why-plug-in', 'access',
               'what-i-built', 'industry', 'wont-fix', 'monday', 'bridge']
FIGS = {'embedded content: Figure 1': '02-architecture', 'Figure 2:': '03-code', 'Figure 3:': '04-tools',
        'Figure 4:': '06-main', 'Figure 5:': '07-under-the-hood', 'Figure 6:': '08-two-ais'}
FROM_GEO_K = ('hero.span1', 'hero.div2', 'sources-h.h21', 'closing.div1', 'closing.p2', 'closing.a4', 'author.div1')


def fmt(s):
    s = html.escape(s, quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)


def inline(t):
    """Same Markdown subset as build-page.py; quotes are typed in the translation („…“)."""
    t = t.replace('&#91;', '[').replace('\\[', '[').replace('\\]', ']')
    out = []
    for part in re.split(r'(`[^`]+`)', t):
        if part.startswith('`'):
            out.append('<code>' + html.escape(part[1:-1], quote=False) + '</code>')
            continue
        for seg in re.split(r'(\[[^\]]+\]\([^)]+\))', part):
            m = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', seg)
            out.append(f'<a href="{html.escape(m[2], quote=True)}" target="_blank" rel="noopener">{fmt(m[1])}</a>' if m else fmt(seg))
    return ''.join(out)


def blocks_to_k(md, figs):
    """Article blocks → {data-k key: inner HTML}, keyed like build-page.py."""
    body = re.split(r'\n## (?:Sources|Zdroje|Quellen)\n', md)[0]
    blocks = [b.strip() for b in body.split('\n\n') if b.strip()][2:]
    k, sid, n, paras, sections = {}, None, 0, 0, iter(SECTION_IDS)

    def key(tag):
        nonlocal n
        n += 1
        return f'{sid}.{tag}{n}'

    for b in blocks:
        if b.startswith('## '):
            sid, n, paras = next(sections), 0, 0
            k[key('h2')] = inline(b[3:])
            continue
        fig = next((v for kk, v in FIGS.items() if kk in b), None)
        if fig:
            k[key('figcaption')] = figs[fig]
            continue
        lines = b.split('\n')
        if all(l.startswith('- ') for l in lines):
            for l in lines:
                k[key('li')] = inline(l[2:])
            continue
        if all(re.match(r'\d+\. ', l) for l in lines):
            for l in lines:
                item = inline(re.sub(r'^\d+\. ', '', l))
                if sid != 'monday':
                    item = re.sub(r'^<strong>(.+?)</strong>', r'<span class="lead-in">\1</span>', item)
                k[key('li')] = item
            continue
        assert len(lines) == 1, b[:80]
        paras += 1
        k[key('p')] = inline(b)
        if sid == 'access' and paras == 3:          # image 05 after the paragraph on checking
            k[key('figcaption')] = figs['05-permission']
        if sid == 'industry' and paras == 1:        # image 11 after the first paragraph
            k[key('figcaption')] = figs['11-timeline']
    return k


NBSP_CS = re.compile(r'(?<![\w])([KkSsVvZzOoUuAaIi]) (?=\S)')


def czech_spaces(s):
    """Non-breaking space after one-letter prepositions and conjunctions, in text only."""
    return ''.join(p if p.startswith('<') else NBSP_CS.sub('\\1\u00a0', p) for p in re.split(r'(<[^>]+>)', s))


extras = json.load(open(os.path.join(PKG, f'i18n-{lang}.extras.json'), encoding='utf-8'))
geo = json.load(open(os.path.join(ROOT, 'insights', 'ai-visibility-for-aec', 'i18n', f'{lang}.json'), encoding='utf-8'))
md = open(os.path.join(PKG, f'article.{lang}.md'), encoding='utf-8').read()

k = {key: geo['k'][key] for key in FROM_GEO_K}
k.update(extras['k'])
k.update(blocks_to_k(md, extras['figs']))

# Every data-k of the English page, and nothing else.
en = open(os.path.join(PAGE, 'index.html'), encoding='utf-8').read()
en_keys = re.findall(r'data-k="([^"]+)"', en[en.index('<body'):])
missing, extra = [x for x in en_keys if x not in k], [x for x in k if x not in en_keys]
assert not missing and not extra, f'keys differ from the English page:\n  missing {missing}\n  extra {extra}'
k = {key: k[key] for key in dict.fromkeys(en_keys)}

chrome = dict(geo['chrome']); chrome.update(extras['chrome'])
ui = dict(geo['ui']); ui.update(extras['ui'])
meta = extras['meta']
if lang == 'cs':
    k = {key: czech_spaces(v) for key, v in k.items()}
    for d in (chrome, ui):
        for key, v in d.items():
            if isinstance(v, str) and not re.search(r'\{\w+\}', v):
                d[key] = czech_spaces(v)
    for key in ('description', 'image_alt'):
        meta[key] = czech_spaces(meta[key])

out = {'lang': lang, 'ui': ui, 'chrome': chrome, 'k': k, 'meta': meta, 'keep': extras['keep']}
os.makedirs(os.path.join(PAGE, 'i18n'), exist_ok=True)
with open(os.path.join(PAGE, 'i18n', f'{lang}.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)   # as the other i18n files
    f.write('\n')
print(f'wrote insights/mcp-power-outlet-for-ai/i18n/{lang}.json: {len(k)} blocks')

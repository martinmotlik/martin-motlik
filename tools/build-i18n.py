#!/usr/bin/env python3
"""Build the Czech and German versions of the Insights pages.

Every language has its own URL with the translated text in the HTML, so search
engines and AI crawlers (which do not run JavaScript) can read, index and cite
each version:

    /insights/…        English: the hand-edited source pages
    /cs/insights/…     generated from the English page + <page>/i18n/cs.json
    /de/insights/…     generated from the English page + <page>/i18n/de.json

Edit the English page or the JSON, then run:

    python3 tools/build-i18n.py            # writes cs/ and de/
    python3 tools/build-i18n.py --check    # fails if the output is out of date

What the translation JSON holds:
    k       article blocks; replaces the inner HTML of [data-k="…"]; the markup
            of each block must match the English one (checked here)
    chrome  short labels; replaces the text of [data-i18n="…"]
    ui      attribute values (data-i18n-attr="attr:key[:arg];…"), the text of
            [data-ui="…"], the <title> and the strings page scripts write later
    meta    description, Open Graph, structured data
"""
import html, json, os, re, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://martinmotlik.com'
LANGS = ('cs', 'de')
LOCALES = {'en': 'en_US', 'cs': 'cs_CZ', 'de': 'de_DE'}

ARTICLE = '/insights/ai-visibility-for-aec/'
PAGES = [
    {'path': '/insights/', 'kind': 'list'},
    {'path': ARTICLE, 'kind': 'article'},
]

# Translated slugs: an article's URL is in the language of the reader. The
# /insights/ segment stays (it is the section's name in every language).
# Plain ASCII, ü → ue. Once a URL is published, do not change it: GitHub Pages
# has no 301 redirects.
URLS = {
    ARTICLE: {'cs': '/cs/insights/data-aec-pro-vyhledavani-s-ai/',
              'de': '/de/insights/aec-daten-fuer-ki-suche/'},
}


def url(path, lang):
    if lang == 'en':
        return path
    return URLS.get(path, {}).get(lang, '/' + lang + path)


def src_file(path):
    return os.path.join(ROOT, path.strip('/'), 'index.html')


def load_json(path, lang):
    with open(os.path.join(ROOT, path.strip('/'), 'i18n', lang + '.json'), encoding='utf-8') as f:
        return json.load(f)


def esc(text):
    return html.escape(text, quote=True)


# ── HTML helpers (the pages are hand-written and regular, so a careful regex
#    walk is enough; every replacement asserts what it expects to find) ──────

def element_spans(s, attr, key):
    """(inner_start, inner_end) of every element whose `attr` equals `key`."""
    spans = []
    for m in re.finditer(r'<(\w+)\b[^>]*\b%s="%s"[^>]*>' % (re.escape(attr), re.escape(key)), s):
        tag, i, depth = m.group(1), m.end(), 1
        for t in re.finditer(r'<(/?)%s\b[^>]*>' % tag, s[i:]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                spans.append((i, i + t.start()))
                break
    return spans


def set_inner(s, attr, key, inner):
    spans = element_spans(s, attr, key)
    assert spans, f'no element with {attr}="{key}"'
    for a, b in reversed(spans):
        s = s[:a] + inner + s[b:]
    return s


def sub_once(s, pattern, repl, count=1, flags=0):
    new, n = re.subn(pattern, repl, s, flags=flags)
    assert n == count, f'{pattern!r}: expected {count}, found {n}'
    return new


def set_meta(s, attr, name, value):
    return sub_once(s, r'(<meta %s="%s" content=")[^"]*(">)' % (attr, re.escape(name)),
                    lambda m: m.group(1) + esc(value) + m.group(2))


TAG = re.compile(r'<(/?)([a-z0-9]+)([^>]*)>')
ATTR = re.compile(r'([a-z-]+)="([^"]*)"')


def skeleton(fragment):
    """Tag structure of a fragment; aria-label values may differ (translated)."""
    return [(m.group(1), m.group(2), tuple((k, '*' if k == 'aria-label' else v) for k, v in ATTR.findall(m.group(3))))
            for m in TAG.finditer(fragment)]


# ── Translation of one page ──────────────────────────────────────────────────

def translate_body(s, data, lang, path):
    ui, chrome = data.get('ui', {}), data.get('chrome', {})

    # 1 · Article blocks (markup must match the English block)
    for key, inner in data.get('k', {}).items():
        en = element_spans(s, 'data-k', key)
        assert en, f'{path}: data-k="{key}" not in the English page'
        a, b = en[0]
        assert skeleton(s[a:b]) == skeleton(inner), f'{path} {lang}: markup of "{key}" differs from English'
        s = set_inner(s, 'data-k', key, inner)

    # 2 · Short labels
    for key in sorted(set(re.findall(r'data-i18n="([^"]+)"', s))):
        assert key in chrome, f'{path} {lang}: chrome "{key}" missing'
        for a, b in element_spans(s, 'data-i18n', key):
            assert '<' not in s[a:b], f'{path}: data-i18n="{key}" is not a text-only element'
        s = set_inner(s, 'data-i18n', key, esc(chrome[key]))

    # 3 · Text written from ui strings
    for key in sorted(set(re.findall(r'data-ui="([^"]+)"', s))):
        assert key in ui, f'{path} {lang}: ui "{key}" missing'
        s = set_inner(s, 'data-ui', key, esc(ui[key]))

    # 4 · Attributes
    def attrs(m):
        tag = m.group(0)
        for binding in m.group(1).split(';'):
            parts = binding.split(':')
            name, key = parts[0], parts[1]
            assert key in ui, f'{path} {lang}: ui "{key}" missing'
            value = ui[key].replace('{net}', parts[2]) if len(parts) > 2 else ui[key]
            tag, n = re.subn(r'(\s%s=")[^"]*(")' % re.escape(name), lambda x: x.group(1) + esc(value) + x.group(2), tag, count=1)
            assert n == 1, f'{path}: attribute {name} missing on {tag[:60]}'
        return tag
    s = re.sub(r'<[^>]*\bdata-i18n-attr="([^"]+)"[^>]*>', attrs, s)

    # 5 · Links inside Insights stay in the language; the rest of the site has one URL
    for p in sorted(URLS, key=len, reverse=True):
        s = s.replace(f'href="{p}"', f'href="{url(p, lang)}"')
    s = s.replace('href="/insights/"', f'href="{url("/insights/", lang)}"')

    # 6 · Language switcher: same links, this version marked current
    def switch(m):
        tag = m.group(0)
        l = re.search(r'data-lang="(\w+)"', tag).group(1)
        tag = tag.replace(' aria-current="page"', '').replace('class="lang-btn active"', 'class="lang-btn"')
        tag = re.sub(r'href="[^"]*"', f'href="{url(path, l)}"', tag, count=1)
        if l == lang:
            tag = tag.replace('class="lang-btn"', 'class="lang-btn active"').replace('>', ' aria-current="page">', 1)
        return tag
    s = re.sub(r'<a class="lang-btn[^"]*"[^>]*>', switch, s)
    return s


def translate_head(s, data, lang, path, extra):
    ui, meta = data['ui'], data['meta']
    page = SITE + url(path, lang)
    s = sub_once(s, r'<html lang="en">', f'<html lang="{lang}">')
    s = sub_once(s, r'<title>[^<]*</title>', f'<title>{esc(ui["title"])}</title>')
    s = set_meta(s, 'name', 'description', meta['description'])
    s = sub_once(s, r'(<link rel="canonical" href=")[^"]*(">)', lambda m: m.group(1) + page + m.group(2))
    s = set_meta(s, 'property', 'og:url', page)
    s = set_meta(s, 'property', 'og:locale', LOCALES[lang])
    others = [LOCALES[l] for l in ('en',) + LANGS if l != lang]
    s = sub_once(s, r'(<meta property="og:locale:alternate" content=")[^"]*(">)\n(\s*<meta property="og:locale:alternate" content=")[^"]*(">)',
                 lambda m: m.group(1) + others[0] + m.group(2) + '\n' + m.group(3) + others[1] + m.group(4))
    s = set_meta(s, 'property', 'og:image:alt', meta['image_alt'])
    s = set_meta(s, 'name', 'twitter:image:alt', meta['image_alt'])
    for name, value in extra.items():
        attr = 'name' if name.startswith('twitter:') else 'property'
        s = set_meta(s, attr, name, value)
    return s


def rewrite_ld(s, fn):
    m = re.search(r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)', s, re.S)
    ld = json.loads(m.group(2))
    fn(ld)
    dump = json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n    ')
    return s[:m.start(2)] + dump + s[m.end(2):]


def word_count(data):
    text = ' '.join(v for k, v in data['k'].items()
                    if k.split('.')[0] in ('intro', 'ai-search', 'localization', 'load-path', 'rules', 'try', 'kit', 'start'))
    text = re.sub(r'<code[^>]*>.*?</code>', ' ', text, flags=re.S)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
    return len(re.findall(r'\w[\w\-’\']*', text))


def build_article(lang):
    path = ARTICLE
    s = open(src_file(path), encoding='utf-8').read()
    data = load_json(path, lang)
    ui, meta = data['ui'], data['meta']
    page = SITE + url(path, lang)
    title = ui['article_title']

    s = translate_head(s, data, lang, path, {
        'og:title': title, 'og:description': meta['description'], 'article:section': meta['section'],
        'twitter:title': title, 'twitter:description': meta['description'],
    })
    tags = meta['tags']
    s = sub_once(s, r'(\s*<meta property="article:tag" content="[^"]*">){4}',
                 ''.join(f'\n    <meta property="article:tag" content="{esc(t)}">' for t in tags))

    def ld(g):
        art, person, crumbs = g['@graph']
        assert art['@type'] == 'TechArticle' and crumbs['@type'] == 'BreadcrumbList'
        art.pop('workTranslation', None)
        art.update({
            '@id': page + '#article', 'headline': title, 'description': meta['description'],
            'inLanguage': meta['in_language'], 'mainEntityOfPage': page,
            'isPartOf': {'@id': SITE + url('/insights/', lang) + '#blog'},
            'articleSection': meta['section'], 'keywords': meta['keywords'],
            'about': [{'@type': 'Thing', 'name': n} for n in meta['about']],
            'wordCount': word_count(data),
            'translationOfWork': {'@id': SITE + path + '#article'},
        })
        art['audio']['name'] = meta['audio_name']          # the narration itself stays English
        art['citation'][0]['name'], art['citation'][0]['description'] = meta['citation1']
        items = crumbs['itemListElement']
        items[0]['name'] = meta['crumb_home']
        items[1]['item'] = SITE + url('/insights/', lang)
        items[2]['name'] = meta['crumb_article']
    s = rewrite_ld(s, ld)

    # Share links carry this version's URL and title.
    en_url, en_title = quote(SITE + path, safe=''), quote('Be the source: getting AEC data ready for AI search', safe='')
    assert s.count(en_url) >= 12 and s.count(en_title) >= 6
    s = s.replace(en_url, quote(page, safe='')).replace(en_title, quote(title, safe=''))
    s = s.replace(quote('I thought this was worth your time:', safe=''), quote(meta['share_intro'], safe=''))

    s = translate_body(s, data, lang, path)

    # Strings for scripts (player state, copy feedback); </ cannot end the block.
    blob = json.dumps(ui, ensure_ascii=False).replace('</', '<\\/')
    s = sub_once(s, r'\n<script>\n// — Language ', f'\n<script type="application/json" id="i18n-ui">{blob}</script>\n<script>\n// — Language ')
    return s


def build_list(lang):
    path = '/insights/'
    s = open(src_file(path), encoding='utf-8').read()
    data = load_json(path, lang)
    art = load_json(ARTICLE, lang)
    chrome, meta = data['chrome'], data['meta']
    page = SITE + url(path, lang)

    s = translate_head(s, data, lang, path, {
        'og:description': chrome['hero_dek'], 'twitter:description': meta['twitter_description'],
    })

    def ld(g):
        blog, person, crumbs = g['@graph']
        assert blog['@type'] == 'Blog' and crumbs['@type'] == 'BreadcrumbList'
        blog.update({
            '@id': page + '#blog', 'description': meta['twitter_description'], 'url': page,
            'inLanguage': meta['in_language'], 'translationOfWork': {'@id': SITE + path + '#blog'},
        })
        post = blog['blogPost'][0]
        post.update({
            '@id': SITE + url(ARTICLE, lang) + '#article', 'headline': art['ui']['article_title'],
            'description': art['meta']['description'], 'url': SITE + url(ARTICLE, lang),
            'articleSection': art['meta']['section'], 'inLanguage': art['meta']['in_language'],
        })
        crumbs['itemListElement'][0]['name'] = meta['crumb_home']
    s = rewrite_ld(s, ld)

    return translate_body(s, data, lang, path)


# Phrases that only exist in the English pages; none may survive in visible text.
ENGLISH_MARKERS = ('Be the source', 'Field notes from', 'All articles', 'On this page', 'Keep reading',
                   'More options', 'Copy link', 'In this article', 'Working on a similar challenge',
                   'Where I would start', 'Get new insights first', '8 min read', 'Oct 6, 2026')


def visible_text(s):
    s = re.sub(r'<(script|style)\b.*?</\1>|<!--.*?-->', ' ', s, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))


def generated_notice(path, lang):
    src = path.strip('/') + '/index.html'
    return (f'<!DOCTYPE html>\n<!-- Generated by tools/build-i18n.py from {src} and '
            f'{path.strip("/")}/i18n/{lang}.json. Do not edit: change those and rerun. -->')


def check_hreflang(path):
    s = open(src_file(path), encoding='utf-8').read()
    found = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', s))
    want = {l: SITE + url(path, l) for l in ('en',) + LANGS}
    want['x-default'] = SITE + path
    assert found == want, f'{path}: hreflang links in the English page do not match URLS:\n  found {found}\n  want  {want}'


def build():
    out = {}
    for p in PAGES:
        check_hreflang(p['path'])
        for lang in LANGS:
            s = build_article(lang) if p['kind'] == 'article' else build_list(lang)
            s = sub_once(s, r'<!DOCTYPE html>', generated_notice(p['path'], lang))
            leftovers = [t for t in ENGLISH_MARKERS if t in visible_text(s)]
            assert not leftovers, f'{p["path"]} {lang}: English left in the page: {leftovers}'
            out[os.path.join(ROOT, url(p['path'], lang).strip('/'), 'index.html')] = s
    return out


def main():
    files = build()
    if '--check' in sys.argv:
        stale = [f for f, s in files.items() if not os.path.exists(f) or open(f, encoding='utf-8').read() != s]
        for f in stale:
            print('out of date:', os.path.relpath(f, ROOT))
        sys.exit(1 if stale else 0)
    for f, s in files.items():
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(s)
        print('wrote', os.path.relpath(f, ROOT))


if __name__ == '__main__':
    main()

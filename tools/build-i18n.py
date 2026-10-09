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
    {'path': '/', 'kind': 'page'},
    {'path': '/services/', 'kind': 'page'},
    {'path': '/references/', 'kind': 'page'},
    {'path': '/references/nascc-2026/', 'kind': 'page'},
    {'path': '/references/mass-timber-2026/', 'kind': 'page'},
    {'path': '/references/rfem6-brochure/', 'kind': 'page'},
    {'path': '/insights/', 'kind': 'list'},
    {'path': '/insights/podcast/', 'kind': 'page'},
    {'path': ARTICLE, 'kind': 'article'},
]

# Translated slugs: a URL is in the language of the reader. /insights/ stays
# (the section's name in every language), as do event names (nascc-2026).
# Plain ASCII, ü → ue. Once a URL is published, do not change it: GitHub Pages
# has no 301 redirects. Pages not listed get /cs/ or /de/ + the English path.
URLS = {
    '/': {'cs': '/cs/', 'de': '/de/'},
    '/services/': {'cs': '/cs/sluzby/', 'de': '/de/leistungen/'},
    '/references/': {'cs': '/cs/reference/', 'de': '/de/referenzen/'},
    '/references/nascc-2026/': {'cs': '/cs/reference/nascc-2026/', 'de': '/de/referenzen/nascc-2026/'},
    '/references/mass-timber-2026/': {'cs': '/cs/reference/mass-timber-2026/', 'de': '/de/referenzen/mass-timber-2026/'},
    '/references/rfem6-brochure/': {'cs': '/cs/reference/rfem6-brozura/', 'de': '/de/referenzen/rfem6-broschuere/'},
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

    # 2 · Labels and short texts. Plain values are escaped; a value with markup
    #     must have the same tags as the English element (e.g. <br>, <em>).
    for key in sorted(set(re.findall(r'data-i18n="([^"]+)"', s))):
        assert key in chrome, f'{path} {lang}: chrome "{key}" missing'
        value = chrome[key]
        for a, b in element_spans(s, 'data-i18n', key):
            if '<' in s[a:b] or '<' in value:
                assert skeleton(s[a:b]) == skeleton(value), f'{path} {lang}: markup of chrome "{key}" differs from English'
        s = set_inner(s, 'data-i18n', key, value if '<' in value else esc(value))

    # 2b · Untagged text and attributes, matched by their exact English text
    s = translate_by_text(s, data.get('text', {}), data.get('attrs', {}))

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

    # 5 · Links to other pages of the site stay in the language
    s = localize_links(s, lang)

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
    for attr, name in (('property', 'og:image:alt'), ('name', 'twitter:image:alt')):
        key = 'twitter_image_alt' if name.startswith('twitter') and 'twitter_image_alt' in meta else 'image_alt'
        if f'<meta {attr}="{name}"' in s:
            assert key in meta, f'{path} {lang}: meta "{key}" missing'
            s = set_meta(s, attr, name, meta[key])
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


# ── Site-wide helpers ────────────────────────────────────────────────────────

PAGE_PATHS = {p['path'] for p in PAGES}
SKIP = re.compile(r'<(script|style|svg)\b.*?</\1>', re.S)


def body_parts(s):
    """Split the body into (is_markup_to_skip, chunk) so script/style/svg stay untouched."""
    i = s.index('<body')
    parts, last = [(True, s[:i])], i
    for m in SKIP.finditer(s, i):
        parts.append((False, s[last:m.start()]))
        parts.append((True, m.group(0)))
        last = m.end()
    parts.append((False, s[last:]))
    return parts


def localize_links(s, lang):
    """Every <a href> to a page of this site points to its version in `lang`."""
    def fix(m):
        absolute, path, rest = m.group(2) or '', m.group(3), m.group(4) or ''
        if path not in PAGE_PATHS:
            return m.group(0)
        return m.group(1) + absolute + url(path, lang) + rest + '"'
    pat = re.compile(r'(<a\b[^>]*?\shref=")(%s)?(/[^"#?]*)([#?][^"]*)?"' % re.escape(SITE))
    out = []
    for skip, chunk in body_parts(s):
        out.append(chunk if skip else pat.sub(fix, chunk))
    return ''.join(out)


TRANSLATABLE_ATTRS = ('alt', 'aria-label', 'title')


def translate_by_text(s, text, attrs):
    """Replace text nodes and alt / aria-label / title values that equal an
    English string in the map (whole value, surrounding whitespace kept)."""
    if not text and not attrs:
        return s
    def node(m):
        raw = m.group(1)
        key = ' '.join(html.unescape(raw).split())
        if key in text:
            lead, trail = raw[:len(raw) - len(raw.lstrip())], raw[len(raw.rstrip()):]
            return '>' + lead + esc(text[key]) + trail + '<'
        return m.group(0)
    def attr(m):
        key = html.unescape(m.group(3))
        return m.group(1) + m.group(2) + '="' + esc(attrs[key]) + '"' if key in attrs else m.group(0)
    apat = re.compile(r'(\s)(%s)="([^"]*)"' % '|'.join(TRANSLATABLE_ATTRS))
    out = []
    for skip, chunk in body_parts(s):
        if not skip:
            chunk = re.sub(r'>([^<>]+)<', node, chunk)
            chunk = re.sub(r'<[a-zA-Z][^>]*>', lambda t: apat.sub(attr, t.group(0)), chunk)
        out.append(chunk)
    return ''.join(out)


def english_runs(s):
    """Visible text runs and translatable attribute values of a page body."""
    runs = set()
    for skip, chunk in body_parts(strip_english(s)):
        if skip:
            continue
        for t in re.findall(r'>([^<>]+)<', chunk):
            t = ' '.join(html.unescape(t).split())
            if re.search(r'[A-Za-z]{2}', t):
                runs.add(t)
        for t in re.findall(r'\s(?:%s)="([^"]+)"' % '|'.join(TRANSLATABLE_ATTRS), chunk):
            runs.add(' '.join(html.unescape(t).split()))
    return runs


# Names and codes that are the same in every language.
KEEP_EVERYWHERE = {
    'EN', 'CS', 'DE', 'English', 'Čeština', 'Deutsch', 'Martin Motlík', 'Insights', 'Dlubal', 'Dlubal Software',
    'LinkedIn', 'X', 'Facebook', 'AI', 'BIM', 'SEO', 'SaaS', 'Design', 'Adobe', 'Dev',
}


def check_untranslated(src, out, data, path, lang):
    left = english_runs(src) & english_runs(out)
    left -= KEEP_EVERYWHERE | set(data.get('keep', []))
    assert not left, f'{path} {lang}: English left on the page (translate it or add it to "keep"):\n  ' + '\n  '.join(sorted(left))


def localize_ld(node, lang, data):
    """Page URLs in JSON-LD point to this version; people and organisations
    keep their single identity (#martin-motlik, #website…)."""
    if isinstance(node, list):
        for n in node:
            localize_ld(n, lang, data)
        return
    if not isinstance(node, dict):
        return
    entity = node.get('@type') in ('Person', 'Organization', 'WebSite', 'PodcastSeries', 'PodcastEpisode')
    touched = False
    for k, v in list(node.items()):
        if isinstance(v, str) and k in ('url', 'item', 'mainEntityOfPage', '@id') and not entity and '#' not in v:
            p = v[len(SITE):] if v.startswith(SITE) else None
            if p is not None and (p in PAGE_PATHS or p + '/' in PAGE_PATHS):
                node[k] = SITE + url(p if p in PAGE_PATHS else p + '/', lang)
                touched = True
        else:
            localize_ld(v, lang, data)
    if touched and ('inLanguage' in node or node.get('@type') in ('WebPage', 'CollectionPage', 'CreativeWork', 'Service')):
        node['inLanguage'] = data['meta']['in_language']


def apply_ld_overrides(ld, overrides, path, lang):
    """"@graph.0.description": "…" sets one value; the path must exist."""
    for dotted, value in overrides.items():
        node, keys = ld, dotted.split('.')
        for k in keys[:-1]:
            node = node[int(k)] if isinstance(node, list) else node[k]
        last = int(keys[-1]) if isinstance(node, list) else keys[-1]
        assert isinstance(node, list) or last in node, f'{path} {lang}: JSON-LD path "{dotted}" not found'
        node[last] = value


def build_page(path, lang):
    src = open(src_file(path), encoding='utf-8').read()
    data = load_json(path, lang)
    meta = data['meta']
    extra = {k: meta[f] for k, f in (('og:title', 'og_title'), ('og:description', 'og_description'),
                                     ('twitter:title', 'twitter_title'), ('twitter:description', 'twitter_description'))
             if f in meta}
    s = translate_head(src, data, lang, path, extra)
    def ld(g):
        localize_ld(g, lang, data)
        # The page node (WebPage / CollectionPage) is named like the page itself.
        for n in g.get('@graph', []):
            if n.get('@type') in ('WebPage', 'CollectionPage') and 'title' in data.get('ui', {}):
                n['name'], n['description'] = data['ui']['title'], meta['description']
        apply_ld_overrides(g, data.get('ld', {}), path, lang)
    s = rewrite_ld(s, ld)
    s = translate_body(s, data, lang, path)
    blob = json.dumps(data.get('ui', {}), ensure_ascii=False).replace('</', '<\\/')
    s = sub_once(s, r'(<body[^>]*>)', lambda m: m.group(1) + f'\n<script type="application/json" id="i18n-ui">{blob}</script>')
    check_untranslated(src, s, data, path, lang)
    return s


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
        art = next(n for n in g['@graph'] if n.get('@type') == 'TechArticle')
        crumbs = next(n for n in g['@graph'] if n.get('@type') == 'BreadcrumbList')
        # The PodcastEpisode node (tools/build-podcast.py) stays as it is: the episode is English.
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

    # Strings for scripts (player state, copy feedback), first in <body> so that
    # assets/podcast/podcast.js finds them too; </ cannot end the block.
    blob = json.dumps(ui, ensure_ascii=False).replace('</', '<\\/')
    s = sub_once(s, r'(<body[^>]*>)', lambda m: m.group(1) + f'\n<script type="application/json" id="i18n-ui">{blob}</script>')
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


def strip_english(s):
    """Content marked lang="en" (podcast titles, chapters, transcript) is English
    on purpose: the episodes are in English. The checks skip it."""
    return re.sub(r'<(?!html\b)(\w+)\b[^>]*\slang="en"[^>]*>.*?</\1>', ' ', s, flags=re.S)


def visible_text(s):
    s = strip_english(re.sub(r'<(script|style)\b.*?</\1>|<!--.*?-->', ' ', s, flags=re.S))
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
            s = {'article': build_article, 'list': build_list}[p['kind']](lang) if p['kind'] != 'page' else build_page(p['path'], lang)
            s = sub_once(s, r'<!DOCTYPE html>', generated_notice(p['path'], lang))
            leftovers = [t for t in ENGLISH_MARKERS if t in visible_text(s)]
            assert not leftovers, f'{p["path"]} {lang}: English left in the page: {leftovers}'
            out[os.path.join(ROOT, url(p['path'], lang).strip('/'), 'index.html')] = s
    return out


# sitemap.xml: every page in every language, each with all its alternates.
SITEMAP = {  # path: (lastmod, changefreq, priority)
    '/': ('2026-10-07', 'monthly', '1.0'),
    '/services/': ('2026-10-07', 'monthly', '0.9'),
    '/references/': ('2026-10-07', 'monthly', '0.9'),
    '/references/nascc-2026/': ('2026-10-07', 'monthly', '0.8'),
    '/references/mass-timber-2026/': ('2026-10-07', 'monthly', '0.8'),
    '/references/rfem6-brochure/': ('2026-10-07', 'monthly', '0.8'),
    '/insights/': ('2026-10-08', 'weekly', '0.9'),
    '/insights/podcast/': ('2026-10-09', 'weekly', '0.8'),
    ARTICLE: ('2026-10-09', 'monthly', '0.8'),
}


def sitemap():
    assert set(SITEMAP) == PAGE_PATHS, 'SITEMAP and PAGES list different pages'
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- Generated by tools/build-i18n.py. Do not edit: change SITEMAP there and rerun. -->',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">', '']
    for p in PAGES:
        lastmod, freq, prio = SITEMAP[p['path']]
        alts = [(l, SITE + url(p['path'], l)) for l in ('en',) + LANGS] + [('x-default', SITE + p['path'])]
        for lang in ('en',) + LANGS:
            out += ['  <url>', f'    <loc>{SITE + url(p["path"], lang)}</loc>', f'    <lastmod>{lastmod}</lastmod>',
                    f'    <changefreq>{freq}</changefreq>', f'    <priority>{prio}</priority>']
            out += [f'    <xhtml:link rel="alternate" hreflang="{l}" href="{u}"/>' for l, u in alts]
            out += ['  </url>', '']
    out.append('</urlset>')
    return '\n'.join(out) + '\n'


def main():
    # The podcast first: it writes the episode list and article sections that
    # the language versions are built from.
    import importlib.util
    spec = importlib.util.spec_from_file_location('build_podcast', os.path.join(ROOT, 'tools', 'build-podcast.py'))
    podcast = importlib.util.module_from_spec(spec); spec.loader.exec_module(podcast)
    pod = podcast.build()
    pod_stale = podcast.stale_files(pod)
    if '--check' not in sys.argv:
        podcast.write(pod, pod_stale)
    files = build()
    files[os.path.join(ROOT, 'sitemap.xml')] = sitemap()
    if '--check' in sys.argv:
        stale = pod_stale + [f for f, s in files.items() if not os.path.exists(f) or open(f, encoding='utf-8').read() != s]
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

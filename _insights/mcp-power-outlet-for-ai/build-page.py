"""Builds insights/mcp-power-outlet-for-ai/index.html from article.md (the
final text, word for word) on the GEO article's template, with the figures
from the image set and the approved components. Rerun it after article.md
changes (the [TK] places), until the page is approved; after that the page is
edited by hand like article #1.

    python3 _insights/mcp-power-outlet-for-ai/build-page.py . "<article-assets>/assets.md"
"""
import html, json, re, subprocess, sys
from urllib.parse import quote

ROOT, ASSETS_MD = sys.argv[1], sys.argv[2]
GEO = open(f'{ROOT}/insights/ai-visibility-for-aec/index.html', encoding='utf-8').read()
SITE = 'https://martinmotlik.com'
PATH = '/insights/mcp-power-outlet-for-ai/'
URL = SITE + PATH
H1 = 'A power outlet for AI: what MCP is and why AEC professionals will need it'
TITLE = 'A Power Outlet for AI: What MCP Is and Why AEC Professionals Will Need It'
DESC = ('Your AI assistant can’t open your model. MCP, an open standard backed by OpenAI, Google and '
        'Microsoft, connects it to the AEC tools you already trust.')
DEK = ('Model Context Protocol is an open standard that connects AI assistants to the software engineers '
       'already use. What it is, what it’s good for in AEC, and why plugging into the big AI platforms '
       'beats building another chatbot.')
CLOSING = 'If you’re connecting AEC software to AI assistants or planning an MCP pilot, I’d be happy to compare notes.'
SHORT = 'A power outlet for AI'
CATEGORY = 'AI in AEC'
TAGS = ['Model Context Protocol', 'AI assistants', 'BIM', 'IFC']
DATE = '2026-10-22'          # the date of the article text; set to the release date when published
esc = lambda s: html.escape(s, quote=True)


def tk(note):
    return f'<mark class="tk">[TK: {esc(note)}]</mark>'


# ── image metadata from assets.md ────────────────────────────────────────────
meta = {}
for block in open(ASSETS_MD, encoding='utf-8').read().split('\n## ')[1:]:
    name = block.split('\n', 1)[0].strip()
    fields = dict(re.findall(r'^- \*\*([^*]+):\*\* (.*)$', block, re.M))
    meta[name] = fields


def picture(slug, sizes, alt, mx, eager=False, indent=0):
    args = ['node', 'tools/picture.mjs', slug, '--sizes', sizes, '--alt', alt, '--max', str(mx), '--indent', str(indent)]
    if eager:
        args.append('--eager')
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=True).stdout.rstrip('\n')


COL = '(min-width: 1004px) 700px, (min-width: 861px) calc(100vw - 304px), min(700px, calc(100vw - 48px))'
ZOOM_IC = ('<span class="fig-ic" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"></path><path d="M9 21H3v-6"></path>'
           '<path d="M21 3l-7 7"></path><path d="M3 21l7-7"></path></svg></span>')
fig_no = 0


def figure(img, key, numbered=True):
    """An article figure: the image links to its 3840 px file (lightbox with JS)."""
    global fig_no
    m = meta[f'mcp-article-{img}']
    alt = m['Alt text']
    cap = re.sub(r'^Figure \d+\.\s*', '', m['Description'])
    if numbered:
        fig_no += 1
        label = f'<span class="fig-n">Figure {fig_no}</span> '
        fid = f' id="fig-{fig_no}"'
        aria = f'Enlarge figure {fig_no}'
    else:
        label, fid, aria = '', f' id="img-{img.split("-")[0]}"', 'Enlarge image'
    pic = picture(f'mcp-article-{img}', COL, esc(alt), 1920, indent=10)
    return (f'      <figure class="fig"{fid}>\n'
            f'        <a class="fig-zoom" href="/assets/img/mcp-article-{img}-3840.jpg" aria-label="{aria}">\n'
            f'{pic}\n          {ZOOM_IC}\n        </a>\n'
            f'        <figcaption data-k="{key}">{label}{esc(cap)}</figcaption>\n'
            f'      </figure>')


# ── code of figure 2 as text (packages/mcp-server/src/server.ts, lines 137–159) ─
CODE = '''server.registerTool(
  "get_properties",
  {
    title: "Element properties",
    description:
      "Returns all property sets, quantities with units and the material " +
      "of one element. Use it to inspect an element found with list_elements.",
    inputSchema: z.object({
      version,
      guid: z.string().describe("IFC GlobalId of the element, 22 characters."),
    }),
    outputSchema: z.looseObject({
      summary: z.string(),
      guid: z.string(),
      property_sets: z.array(z.unknown()),
    }),
    annotations: { readOnlyHint: true, idempotentHint: true },
  },
  async ({ version, guid }) =>
    run("get_properties", { version, guid }, () =>
      elementProperties(catalog, version, guid),
    ),
);'''


def code_line(line):
    s = esc(line)
    s = re.sub(r'(&quot;.*?&quot;)', r'<span class="u">\1</span>', s)
    s = re.sub(r'^(\s*)([a-zA-Z_]+)(:)', r'\1<span class="k">\2</span>\3', s)
    return f'<span class="l">{s}\n</span>'


code_html = ''.join(code_line(l) for l in CODE.split('\n'))
code_html = code_html[:-len('\n</span>')] + '</span>'
CHEV = ('<svg class="chev" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"></path></svg>')
code_details = f'''      <details class="code-src">
        <summary><span data-i18n="code_as_text">Show the code as text</span>{CHEV}</summary>
<figure class="codeblock">
        <figcaption class="cb-bar"><span class="cb-meta"><span class="cb-name">server.ts</span><span class="cb-sub">packages/mcp-server/src · lines 137–159</span></span><button class="cb-copy" type="button" data-copy-code=".cb-body code" aria-label="Copy the code" data-i18n-attr="aria-label:copy_code" data-ui="copy">Copy</button></figcaption>
<pre class="cb-body scroll-x" tabindex="0" style="counter-reset:ln 136"><code>{code_html}</code></pre>
      </figure>
      </details>'''


# ── the article text: _insights/<slug>/article.md, word for word ─────────────
# Markdown subset of the export: ## headings, paragraphs, "- " and "1. " lists,
# **bold**, `code`, [links](url), \[ \] escapes; figure notes become figures.
MD = open(f'{ROOT}/_insights/mcp-power-outlet-for-ai/article.md', encoding='utf-8').read()
IDS = {
    "The AI that can't open your model": ('cant-open', "The AI that can’t open your model"),
    'What MCP is: an outlet, not a brain': ('what-mcp-is', 'What MCP is'),
    'Why AEC needs it: guessing vs. computing': ('why-aec', 'Why AEC needs it'),
    'Why plug into the AI giants instead of building our own chatbot': ('why-plug-in', 'Why plug into the AI giants'),
    'Three levels of trust': ('trust', 'Three levels of trust'),
    'What I built: \\[TK: two evenings\\] and six tools': ('what-i-built', 'What I built'),
    'Where the industry stands': ('industry', 'Where the industry stands'),
    "What MCP won't fix": ('wont-fix', 'What MCP won’t fix'),
    'How to start on Monday': ('monday', 'How to start on Monday'),
    'A bridge, not a replacement': ('bridge', 'A bridge, not a replacement'),
}
FIGS = {'embedded content: Figure 1': '02-architecture', 'Figure 2:': '03-code', 'Figure 3:': '04-tools',
        'Figure 4:': '06-main', 'Figure 5:': '07-under-the-hood', 'Figure 6:': '08-two-ais'}


def smart(s):
    """Typographic quotes as on the rest of the site (’ “ ”); the words stay."""
    s = s.replace("'", '’')
    s = re.sub(r'"(?=[\w\[(])', '“', s)
    return s.replace('"', '”')


def fmt(s):
    s = html.escape(smart(s), quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return re.sub(r'\[TK: (.+?)\]', lambda m: f'<mark class="tk">[TK: {m[1]}]</mark>', s)


def inline(t):
    t = t.replace('&#91;', '[').replace('\\[', '[').replace('\\]', ']')
    out = []
    for part in re.split(r'(`[^`]+`)', t):
        if part.startswith('`'):
            out.append('<code>' + html.escape(part[1:-1], quote=False) + '</code>')
            continue
        for seg in re.split(r'(\[[^\]]+\]\([^)]+\))', part):
            m = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', seg)
            out.append(f'<a href="{esc(m[2])}" target="_blank" rel="noopener">{fmt(m[1])}</a>' if m else fmt(seg))
    return ''.join(out)


text, sources_md = MD.split('\n## Sources\n')
blocks = [b.strip() for b in text.split('\n\n') if b.strip()]
assert blocks[0].startswith('# ') and blocks[1].startswith('Oct 22, 2026')
blocks = blocks[2:]

SECTIONS, body = [], []
sid, n, after_first = None, 0, False


def key(tag):
    global n
    n += 1
    return f'{sid}.{tag}{n}'


for b in blocks:
    if b.startswith('## '):
        title = b[3:]
        sid, short = IDS[title]
        SECTIONS.append((sid, short))
        n, after_first = 0, False
        body.append(f'      <div class="h2-row"><h2 data-k="{key("h2")}" id="{sid}">{inline(title)}</h2></div>')
        continue
    fig = next((v for k, v in FIGS.items() if k in b), None)
    if fig:
        body.append(figure(fig, key('figcaption')))
        if fig == '03-code':
            body.append(code_details)
        continue
    lines = b.split('\n')
    if all(l.startswith('- ') for l in lines):
        items = '\n'.join(f'        <li data-k="{key("li")}">{inline(l[2:])}</li>' for l in lines)
        body.append(f'      <ul>\n{items}\n      </ul>')
        continue
    if all(re.match(r'\d+\. ', l) for l in lines):
        items = [inline(re.sub(r'^\d+\. ', '', l)) for l in lines]
        if sid == 'monday':      # the five vendor questions: highlighted card (approved component E)
            lis = '\n'.join(f'          <li data-k="{key("li")}">{i}</li>' for i in items)
            body.append(f'      <div class="takeaway ask">\n        <ol class="steps">\n{lis}\n        </ol>\n      </div>')
        else:                    # numbered reasons with a bold lead-in, as "My rules" in article #1
            lis = '\n'.join(f'        <li data-k="{key("li")}">' + re.sub(r'^<strong>(.+?)</strong>', r'<span class="lead-in">\1</span>', i) + '</li>' for i in items)
            body.append(f'      <ol class="steps">\n{lis}\n      </ol>')
        continue
    assert len(lines) == 1, b[:80]
    lead = ' class="lead"' if sid == 'cant-open' and n == 1 else ''
    body.append(f'      <p data-k="{key("p")}"{lead}>{inline(b)}</p>')
    # Unnumbered images: after the paragraph on level two, after the first paragraph of the industry section.
    if sid == 'trust' and b.startswith('**Level two'):
        body.append(figure('05-permission', key('figcaption'), numbered=False))
    if sid == 'industry' and not after_first:
        after_first = True
        body.append(figure('11-timeline', key('figcaption'), numbered=False))

assert fig_no == 6, fig_no
SOURCES = []
for l in sources_md.strip().split('\n'):
    m = re.fullmatch(r'- \[(.+?)\]\((.+?)\)', l)
    pub, title = m[1].split(': ', 1) if ': ' in m[1] else ('', m[1])
    SOURCES.append((pub, title, m[2]))

plain = re.sub(r'<[^>]+>', ' ', '\n'.join(b for b in body if '<figure' not in b and 'code-src' not in b))
WORDS = len(re.findall(r'\w[\w\-’\']*', html.unescape(plain)))
READ = round(WORDS / 230)

toc = '\n'.join(f'        <a data-k="toc.a{i + 1}" href="#{s}">{esc(t)}</a>' for i, (s, t) in enumerate(SECTIONS))
toc_m = toc.replace('        <a', '          <a')

# ── head ─────────────────────────────────────────────────────────────────────
head_top = GEO[:GEO.index('    <title>')]
head_assets = GEO[GEO.index('    <link rel="icon"'):GEO.index('    <!-- Preload only AVIF')]
geo_ld = json.loads(re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', GEO, re.S).group(1))
person = next(n for n in geo_ld['@graph'] if n['@type'] == 'Person')
ld = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'TechArticle', '@id': URL + '#article', 'headline': H1, 'description': DESC, 'inLanguage': 'en-US',
     'datePublished': DATE, 'dateModified': DATE,
     'author': {'@id': SITE + '/#martin-motlik'}, 'publisher': {'@id': SITE + '/#martin-motlik'},
     'mainEntityOfPage': URL,
     'image': [SITE + '/assets/img/mcp-article-01-hero-1920.jpg', SITE + '/assets/img/mcp-article-01-hero-og-1200.jpg'],
     'isPartOf': {'@id': SITE + '/insights/#blog'}, 'articleSection': CATEGORY,
     'keywords': ['Model Context Protocol', 'MCP', 'AI assistants', 'AI agents', 'BIM', 'IFC', 'IDS', 'AEC software'],
     'about': [{'@type': 'Thing', 'name': 'Model Context Protocol'},
               {'@type': 'Thing', 'name': 'Architecture, engineering and construction industry'}],
     'wordCount': WORDS,
     'citation': [dict({'@type': 'CreativeWork', 'name': t, 'url': u}, **({'publisher': {'@type': 'Organization', 'name': p}} if p else {}))
                  for p, t, u in SOURCES]},
    person,
    {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Insights', 'item': SITE + '/insights/'},
        {'@type': 'ListItem', 'position': 3, 'name': SHORT}]},
]}
ld_txt = json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n    ')
hero_alt = meta['mcp-article-01-hero']['Alt text']
og_alt = "ChatGPT's answer links to three doors in a web-based 3D viewer of a residential building"

head = head_top + f'''    <title>{esc(TITLE)}</title>
    <meta name="description" content="{esc(DESC)}">
    <meta name="author" content="Martin Motlík">
    <link rel="canonical" href="{URL}">

    <!-- Language versions (tools/build-i18n.py). CS and DE are added with the translations. -->
    <link rel="alternate" hreflang="en" href="{URL}">
    <link rel="alternate" hreflang="x-default" href="{URL}">
    <link rel="alternate" type="application/rss+xml" title="Insights with Martin Motlík (podcast)" href="https://martinmotlik.com/podcast/feed.xml">

    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Martin Motlík">
    <meta property="og:locale" content="en_US">
    <meta property="og:title" content="{esc(H1)}">
    <meta property="og:description" content="{esc(DESC)}">
    <meta property="og:url" content="{URL}">
    <meta property="og:image" content="https://martinmotlik.com/assets/img/mcp-article-01-hero-og-1200.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:alt" content="{esc(og_alt)}">
    <meta property="article:published_time" content="{DATE}">
    <meta property="article:modified_time" content="{DATE}">
    <meta property="article:author" content="https://martinmotlik.com/#martin-motlik">
    <meta property="article:section" content="{CATEGORY}">
''' + ''.join(f'    <meta property="article:tag" content="{esc(t)}">\n' for t in TAGS) + f'''
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@martinmotlik">
    <meta name="twitter:creator" content="@martinmotlik">
    <meta name="twitter:title" content="{esc(H1)}">
    <meta name="twitter:description" content="{esc(DESC)}">
    <meta name="twitter:image" content="https://martinmotlik.com/assets/img/mcp-article-01-hero-og-1200.jpg">
    <meta name="twitter:image:alt" content="{esc(og_alt)}">

''' + head_assets + f'''    <!-- Preload only AVIF: `type` filters out formats the browser cannot decode, so a
         second JPEG link would make modern browsers fetch both copies of the LCP image. -->
    <link rel="preload" as="image" type="image/avif"
          href="/assets/img/mcp-article-01-hero-1280.avif"
          imagesrcset="/assets/img/mcp-article-01-hero-900.avif 900w, /assets/img/mcp-article-01-hero-1280.avif 1280w, /assets/img/mcp-article-01-hero-1920.avif 1920w, /assets/img/mcp-article-01-hero-2560.avif 2560w"
          imagesizes="(min-width: 1128px) 1032px, calc(100vw - 48px)">

    <script type="application/ld+json">
    {ld_txt}
  </script>

'''

# ── CSS: the template's, plus the components this article needs ─────────────
css = GEO[GEO.index('    <style>\n        :root {'):GEO.index('</head>')]
NEW_CSS = '''/* ── 12 · FIGURES ────────────────────────────────────────────────────────────
   An image in the text column with its caption below. The image links to its
   3840 px file; with JS it opens in a native <dialog> (Esc, click outside or
   × closes it), with a link to the full-resolution file. */
article figure.fig{margin:var(--sp-6) 0}
.ins article a.fig-zoom{position:relative;display:block;aspect-ratio:16/9;border-radius:var(--r-panel);overflow:hidden;background:var(--s3);cursor:zoom-in;text-decoration:none}
.fig-zoom img{display:block;width:100%;height:100%;object-fit:cover}
.fig-zoom::after{content:"";position:absolute;inset:0;border-radius:inherit;box-shadow:inset 0 0 0 1px rgba(28,43,51,.08);pointer-events:none}
.fig-ic{position:absolute;right:12px;bottom:12px;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.94);color:var(--ink);display:grid;place-items:center;box-shadow:0 1px 2px rgba(28,43,51,.12),0 8px 20px -10px rgba(28,43,51,.35);transition:transform .2s}
.fig-zoom:hover .fig-ic{transform:scale(1.08)}
article figure.fig figcaption{margin-top:var(--sp-3);font-size:14px;line-height:1.55;color:var(--m1);text-wrap:pretty}
.fig-n{font-weight:600;color:var(--ink);margin-right:2px}
html:has(.zoom[open]){overflow:hidden}
.zoom{width:100vw;height:100dvh;max-width:none;max-height:none;margin:0;padding:0;border:0;background:transparent;color:#fff}
.zoom::backdrop{background:rgba(9,9,11,.92)}
.zoom[open]{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:64px var(--gutter) 20px}
.zoom img{display:block;max-width:100%;max-height:calc(100dvh - 150px);width:auto;height:auto;border-radius:12px;background:#fff}
.zoom-foot{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:center;gap:6px 16px;max-width:900px;font-size:13px;line-height:1.5;text-align:center;color:rgba(255,255,255,.78)}
.zoom-foot a{color:#fff;font-weight:600;white-space:nowrap;text-decoration:none}
.zoom-foot a:hover{text-decoration:underline}
.zoom-x{position:fixed;top:12px;right:12px;width:44px;height:44px;border:0;border-radius:50%;background:rgba(255,255,255,.12);color:#fff;font:400 24px/1 Inter,system-ui,sans-serif;cursor:pointer}
.zoom-x:hover{background:rgba(255,255,255,.22)}
.zoom :focus-visible{outline:2px solid var(--on-dark-label);outline-offset:2px}

/* 13 · Code shown in a figure, also as text: a closed <details> below it */
.code-src{margin:calc(var(--sp-6) * -1 + var(--sp-3)) 0 var(--sp-6)}
.code-src summary{list-style:none;display:inline-flex;align-items:center;gap:10px;min-height:44px;padding:0 16px;border:1px solid var(--line);border-radius:999px;background:#fff;font-size:13px;font-weight:600;line-height:1.2;color:var(--ink);cursor:pointer;transition:background .2s}
.code-src summary::-webkit-details-marker{display:none}
.code-src summary:hover{background:var(--s1)}
.code-src summary .chev{color:var(--m2)}
.code-src .codeblock{margin:var(--sp-3) 0 0}

/* 14 · A list inside the highlighted card (questions to ask), and the TK marks
   for text that is still missing: a page with one must not be published. */
.takeaway ol.steps{margin:var(--sp-4) 0 0}
.takeaway.ask ol.steps{margin:0}
/* Bulleted lists (article #1 had none): the paragraph rhythm below them too. */
article ul{margin:0 0 1.375rem}
.takeaway ol.steps>li::before{background:#fff}
mark.tk{padding:1px 6px;border-radius:6px;background:#FEF3C7;color:#92400E;font-weight:500;-webkit-box-decoration-break:clone;box-decoration-break:clone}

/* 15 · Keep reading: the other articles as compact cards */
.more{margin:var(--sp-7) 0 0;padding-top:20px;border-top:1px solid var(--rule)}
.ins article a.more-card{margin-top:12px;display:grid;grid-template-columns:minmax(0,200px) minmax(0,1fr);gap:20px;align-items:center;padding:12px;border-radius:var(--r-panel);background:#fff;box-shadow:var(--card);color:var(--ink);text-decoration:none;transition:transform .5s var(--ease),box-shadow .5s var(--ease)}
.ins article a.more-card:hover{transform:translateY(-2px);box-shadow:var(--card-hi);color:var(--ink)}
.mc-shot{display:block;aspect-ratio:16/10;border-radius:14px;overflow:hidden;background:var(--s3)}
.mc-shot img{width:100%;height:100%;object-fit:cover}
.mc-txt,.mc-t,.mc-m{display:block}
.mc-cat{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--blue)}
.mc-t{margin-top:6px;font-size:18px;line-height:1.3;letter-spacing:-.015em;font-weight:700;text-wrap:balance}
.mc-m{margin-top:8px;font-size:13px;color:var(--m2)}
.more p.all-link{margin-top:var(--sp-4)}
@media (max-width:620px){.ins article a.more-card{grid-template-columns:112px minmax(0,1fr);gap:14px}.mc-t{font-size:16px}}
@media (prefers-reduced-motion:reduce){.fig-ic,.code-src summary,.more-card{transition:none}}

'''
anchor = '/* ── 11 · PODCAST'
css = css.replace(anchor, NEW_CSS + anchor, 1)

# ── body ─────────────────────────────────────────────────────────────────────
nav = GEO[GEO.index('<body>'):GEO.index('<main class="ins">')]
nav = nav.replace('href="/insights/ai-visibility-for-aec/"', f'href="{PATH}"')
# CS/DE do not exist yet: the switcher leads to the translated Insights lists.
nav = nav.replace('href="/cs/insights/data-aec-pro-vyhledavani-s-ai/"', 'href="/cs/insights/"')
nav = nav.replace('href="/de/insights/aec-daten-fuer-ki-suche/"', 'href="/de/insights/"')

byline = GEO[GEO.index('        <div class="byline" id="byline">'):GEO.index('          <span data-k="hero.span5" id="vo-meta">')]
cover = picture('mcp-article-01-hero', '(min-width: 1128px) 1032px, calc(100vw - 48px)', esc(hero_alt), 2560, eager=True, indent=8)
cover = cover.replace('alt="', 'data-i18n-attr="alt:cover_alt" alt="', 1)


def share(block):
    old_url = quote(SITE + '/insights/ai-visibility-for-aec/', safe='')
    old_title = quote('Be the source: getting AEC data ready for AI search', safe='')
    assert block.count(old_url) >= 6 and block.count(old_title) >= 3
    return block.replace(old_url, quote(URL, safe='')).replace(old_title, quote(H1, safe=''))


share_side = share(GEO[GEO.index('      <div class="share" role="group" aria-labelledby="share-h-side">'):GEO.index('    </aside>')])
share_row = share(GEO[GEO.index('      <div class="share-row">'):GEO.index('      <div class="tags">')])
closing = GEO[GEO.index('      <section class="closing"'):GEO.index('      <div class="share-row">')]
closing = re.sub(r'(<p data-k="closing.p3" class="cl-d">).*?(</p>)', lambda m: m.group(1) + esc(CLOSING) + m.group(2), closing)
author = GEO[GEO.index('      <div class="author">'):GEO.index('      <!-- "Keep reading"')]

geo_card = picture('ai-search-hero', '(min-width: 621px) 200px, 112px', 'Martin Motl&iacute;k working on a laptop, surrounded by the icons of AI assistants', 900, indent=10)
geo_card = geo_card.replace('alt="', 'data-i18n-attr="alt:more_a1_alt" alt="', 1)
more = f'''      <section class="more" aria-labelledby="more-h">
        <h2 class="src-h" id="more-h" data-i18n="more_h">Keep reading</h2>
        <a class="more-card" href="/insights/ai-visibility-for-aec/">
          <span class="mc-shot">
{geo_card}
          </span>
          <span class="mc-txt">
            <span class="mc-cat" data-i18n="cat_ai">AI in AEC</span>
            <span class="mc-t" data-i18n="more_a1_title">Be the source: getting AEC data ready for AI search</span>
            <span class="mc-m"><time datetime="2026-10-06" data-i18n="more_a1_date">Oct 6, 2026</time> &middot; <span data-i18n="read_8">8 min read</span> &middot; <span data-i18n="podcast_tag">Podcast</span> 14 min</span>
          </span>
        </a>
        <p class="all-link"><a href="/insights/" data-i18n="more_all">All insights →</a></p>
      </section>
'''

tags = '\n'.join(f'        <span data-k="tags.span{i + 1}">{esc(t)}</span>' for i, t in enumerate(TAGS))
src_items = '\n'.join(
    f'          <li id="src-{i}"><a href="{esc(u)}" target="_blank" rel="noopener"><span class="src-n">[{i}]</span>'
    f'<span data-k="sources-h.span{i + 1}" class="src-t">{esc(p) + ": " if p else ""}<strong>{fmt(t)}</strong></span><span class="src-arr" aria-hidden="true">↗</span></a></li>'
    for i, (p, t, u) in enumerate(SOURCES, 1))
sources = f'''      <section class="sources" aria-labelledby="sources-h">
        <h2 data-k="sources-h.h21" class="src-h" id="sources-h">Sources</h2>
        <ol class="src-list">
{src_items}
        </ol>
      </section>
'''

main = f'''<main class="ins">
  <section class="hero">
    <div class="glow" aria-hidden="true"></div>
    <div class="wrap hero-in">
      <nav class="crumbs" aria-label="Breadcrumb" data-i18n-attr="aria-label:crumbs_aria"><a href="/insights/" data-i18n="nav_insights">Insights</a><span>/</span><span data-k="hero.span1">{CATEGORY}</span></nav>
      <div class="head">
        <div data-k="hero.div2" class="cat">{CATEGORY}</div>
        <h1 data-k="hero.h13">{esc(H1)}</h1>
        <p data-k="hero.p4" class="dek">{esc(DEK)}</p>

{byline}          <span data-k="hero.span5" id="vo-meta"><time datetime="{DATE}">Oct 22, 2026</time> &middot; <span data-i18n="read_{READ}">{READ} min read</span></span>
        </div>
      </div>

      <div class="cover">
{cover}
      </div>
    </div>
  </section>

  <div class="body">
    <aside class="toc">
      <div class="lbl" data-i18n="toc_label">On this page</div>
      <nav id="toc" class="toc-links" aria-label="On this page" data-i18n-attr="aria-label:toc_aria">
{toc}
      </nav>
<!-- toc-pod:start · generated by tools/build-podcast.py -->
<!-- toc-pod:end -->
{share_side}    </aside>

    <article>

      <!-- One-column layouts: the sidebar is hidden and the contents fold up here. -->
      <details class="toc-m" id="toc-m">
        <summary><span id="toc-m-h" data-i18n="toc_mobile">In this article</span>{CHEV}</summary>
        <nav class="toc-links" aria-labelledby="toc-m-h">
{toc_m}
        </nav>
      </details>

''' + '\n\n'.join(body) + f'''

<!-- podcast:start · generated by tools/build-podcast.py from podcast/podcast.json -->
<!-- podcast:end -->

{sources}
{closing}{share_row}      <div class="tags">
{tags}
      </div>

{author}{more}    </article>
  </div>

</main>

<p class="sr" id="sr-live" role="status" aria-live="polite"></p>

<!-- Figures open here, full size (script below); without JS their links open the file. -->
<dialog class="zoom" id="zoom" aria-label="Enlarged image" data-i18n-attr="aria-label:zoom_aria">
  <button class="zoom-x" type="button" data-zoom-close aria-label="Close" data-i18n-attr="aria-label:close">×</button>
  <picture><source id="zoom-avif" type="image/avif" sizes="100vw"><img id="zoom-img" alt="" sizes="100vw" decoding="async"></picture>
  <div class="zoom-foot"><span id="zoom-cap"></span><a id="zoom-full" href="#" target="_blank" rel="noopener" data-i18n="zoom_full">Open full resolution ↗</a></div>
</dialog>

<!-- pod-mini:start · generated by tools/build-podcast.py -->
<!-- pod-mini:end -->
'''

tail = GEO[GEO.index('<!-- pod-mini:end -->') + len('<!-- pod-mini:end -->\n</div>\n'):]
tail = re.sub(r'<!-- pod-data:start.*?<!-- pod-data:end -->', '<!-- pod-data:start · generated by tools/build-podcast.py -->\n<!-- pod-data:end -->', tail, flags=re.S)
ZOOM_JS = '''
// — Figures: the image link opens the full-size file in the <dialog>. Plain
//   clicks only; modified clicks (new tab) and no-JS keep the link.
(function(){
  var dlg = document.getElementById('zoom');
  if (!dlg || !dlg.showModal) return;
  var avif = document.getElementById('zoom-avif'), img = document.getElementById('zoom-img');
  var cap = document.getElementById('zoom-cap'), full = document.getElementById('zoom-full');
  var widths = [1400, 1920, 2560, 3840];
  document.querySelectorAll('a.fig-zoom').forEach(function(a){
    a.addEventListener('click', function(e){
      if (e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      var href = a.getAttribute('href'), base = href.replace(/-\\d+\\.jpg$/, '');
      var set = function(ext){ return widths.map(function(w){ return base + '-' + w + '.' + ext + ' ' + w + 'w'; }).join(', '); };
      avif.srcset = set('avif');
      img.srcset = set('jpg');
      img.src = href;
      img.alt = a.querySelector('img').alt;
      var fc = a.closest('figure').querySelector('figcaption');
      cap.textContent = fc ? fc.textContent.replace(/\\s+/g, ' ').trim() : '';
      full.href = href;
      dlg.showModal();
    });
  });
  dlg.addEventListener('click', function(e){
    if (e.target === dlg || e.target.closest('[data-zoom-close]')) dlg.close();
  });
  dlg.addEventListener('close', function(){ avif.removeAttribute('srcset'); img.removeAttribute('srcset'); img.removeAttribute('src'); });
})();
'''
i = tail.rindex('</script>')
tail = tail[:i] + ZOOM_JS + tail[i:]

page = head + css + '</head>\n' + nav + main + tail
open(f'{ROOT}/insights/mcp-power-outlet-for-ai/index.html', 'w', encoding='utf-8').write(page)
print('figures:', fig_no, ' words:', WORDS, ' read:', READ, ' sources:', len(SOURCES), ' bytes:', len(page.encode()))

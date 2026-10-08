#!/usr/bin/env python3
"""Build the podcast "Insights by Martin Motlík" from podcast/podcast.json.

    python3 tools/build-podcast.py            # write everything below
    python3 tools/build-podcast.py --check    # fail if anything is out of date

Writes:
    podcast/feed.xml                         RSS for Apple Podcasts, Spotify & co.
    assets/podcast/<slug>.chapters.json      Podcasting 2.0 chapters
    insights/podcast/index.html              episode list + JSON-LD (between markers)
    <article>/index.html                     podcast section, player source, JSON-LD

tools/build-i18n.py runs this first, so one command builds the whole site.
Audio is self-hosted on GitHub Pages (byte-range requests work, which Apple
requires). Each episode needs: the MP3, a WebVTT file and the transcript in
Markdown (chapters as "### Title [m:ss]", lines as "**Name** [m:ss]: text").
"""
import email.utils, html, json, os, re, sys, uuid
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, 'podcast', 'podcast.json'), encoding='utf-8'))
SHOW, EPISODES = DATA['show'], DATA['episodes']
SITE = SHOW['site']
# false: the podcast lives only on the website (no feed.xml, no RSS links), so
# no directory can pick it up. true: the feed is published for Apple & co.
PUBLIC = bool(SHOW.get('feed_public'))
RSS_LINK = f'    <link rel="alternate" type="application/rss+xml" title="{SHOW["title"]} (podcast)" href="{SITE}{SHOW["feed"]}">\n'


def esc(s):
    return html.escape(s, quote=True)


def clock(sec):
    sec = int(sec)                     # whole seconds, as the player shows them
    h, m, s = sec // 3600, sec // 60 % 60, sec % 60
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'


def iso_duration(sec):
    sec = int(round(sec))
    return f'PT{sec // 60}M{sec % 60}S'


def seconds(ts):
    parts = [int(p) for p in ts.split(':')]
    return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))


def parse_transcript(path):
    """→ [(chapter_title, start_seconds, [(speaker, seconds, text), ...]), ...]"""
    chapters = []
    for line in open(os.path.join(ROOT, path), encoding='utf-8'):
        line = line.rstrip('\n')
        m = re.match(r'### (.+) \[(\d+:\d\d)\]$', line)
        if m:
            chapters.append((m.group(1), seconds(m.group(2)), []))
            continue
        m = re.match(r'\*\*(.+?)\*\* \[(\d+:\d\d)\]: (.+)$', line)
        if m:
            assert chapters, f'{path}: a line before the first chapter'
            chapters[-1][2].append((m.group(1), seconds(m.group(2)), m.group(3)))
    assert chapters and all(c[2] for c in chapters), f'{path}: no chapters or an empty chapter'
    return chapters


def episode_files(ep):
    """Checks the files an episode needs and returns (bytes, chapters)."""
    audio = os.path.join(ROOT, ep['audio'].lstrip('/'))
    assert os.path.exists(audio), f'missing {ep["audio"]}'
    vtt = open(os.path.join(ROOT, ep['captions'].lstrip('/')), encoding='utf-8').read()
    assert vtt.startswith('WEBVTT'), f'{ep["captions"]} is not WebVTT'
    last = re.findall(r'--> (\d\d):(\d\d):(\d\d)\.(\d+)', vtt)[-1]
    end = int(last[0]) * 3600 + int(last[1]) * 60 + int(last[2])
    assert abs(end - ep['duration']) <= 3, f'{ep["slug"]}: duration {ep["duration"]} s, captions end at {end} s'
    return os.path.getsize(audio), parse_transcript(ep['transcript'])


# ── RSS ──────────────────────────────────────────────────────────────────────

def feed(eps):
    page, feed_url, cover = SITE + SHOW['page'], SITE + SHOW['feed'], SITE + SHOW['cover']
    # Podcasting 2.0 GUID: UUIDv5 of the feed URL without the scheme.
    guid = uuid.uuid5(uuid.UUID('ead4c236-bf58-58c6-a2c6-a6b28d128cb6'), feed_url.split('://', 1)[1])
    cats = ''.join(
        f'\n    <itunes:category text="{esc(c[0])}">' + (f'<itunes:category text="{esc(c[1])}"/>' if len(c) > 1 else '') + '</itunes:category>'
        for c in SHOW['categories'])
    items = []
    for ep, size, chapters in sorted(eps, key=lambda e: e[0]['number'], reverse=True):
        link = SITE + ep['article']
        notes = (f'<p>{esc(ep["summary"])}</p>'
                 '<p>Chapters:</p><ul>' + ''.join(f'<li>{clock(t)} {esc(title)}</li>' for title, t, _ in chapters) + '</ul>'
                 f'<p>Read the article: <a href="{link}">{esc(ep["title"])}</a></p>'
                 f'<p>{esc(ep["disclosure"])}</p>')
        pub = email.utils.format_datetime(datetime.fromisoformat(ep['published']))
        items.append(f'''  <item>
    <title>{esc(ep["title"])}</title>
    <link>{link}</link>
    <guid isPermaLink="false">martinmotlik.com/podcast/{ep["slug"]}</guid>
    <pubDate>{pub}</pubDate>
    <description><![CDATA[{notes}]]></description>
    <enclosure url="{SITE + ep["audio"]}" length="{size}" type="audio/mpeg"/>
    <itunes:duration>{ep["duration"]}</itunes:duration>
    <itunes:episode>{ep["number"]}</itunes:episode>
    <itunes:episodeType>full</itunes:episodeType>
    <itunes:explicit>false</itunes:explicit>
    <podcast:transcript url="{SITE + ep["captions"]}" type="text/vtt" language="en" rel="captions"/>
    <podcast:chapters url="{SITE}/assets/podcast/{ep["slug"]}.chapters.json" type="application/json+chapters"/>
  </item>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated by tools/build-podcast.py from podcast/podcast.json. Do not edit. -->
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:podcast="https://podcastindex.org/namespace/1.0"
     xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{esc(SHOW["title"])}</title>
  <link>{page}</link>
  <atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>
  <language>{SHOW["language"]}</language>
  <copyright>{esc(SHOW["copyright"])}</copyright>
  <description>{esc(SHOW["description"])}</description>
  <itunes:author>{esc(SHOW["author"])}</itunes:author>
  <itunes:owner>
    <itunes:name>{esc(SHOW["owner"]["name"])}</itunes:name>
    <itunes:email>{esc(SHOW["owner"]["email"])}</itunes:email>
  </itunes:owner>
  <itunes:image href="{cover}"/>
  <image><url>{cover}</url><title>{esc(SHOW["title"])}</title><link>{page}</link></image>{cats}
  <itunes:explicit>{str(SHOW["explicit"]).lower()}</itunes:explicit>
  <itunes:type>{SHOW["type"]}</itunes:type>
  <podcast:guid>{guid}</podcast:guid>
  <podcast:locked owner="{esc(SHOW["owner"]["email"])}">yes</podcast:locked>
  <podcast:person role="host" href="{SITE}/">{esc(SHOW["author"])}</podcast:person>
{chr(10).join(items)}
</channel>
</rss>
'''


def chapters_json(chapters):
    return json.dumps({'version': '1.2.0', 'chapters': [{'startTime': t, 'title': title} for title, t, _ in chapters]},
                      ensure_ascii=False, indent=1) + '\n'


# ── Article: podcast section, player source, JSON-LD ─────────────────────────

CHEV = '<svg class="chev" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"></path></svg>'


def article_section(ep, chapters):
    w = SHOW['cover_web']
    rss = f'              <a class="pod-link" href="{SITE + SHOW["feed"]}" data-i18n="pod_rss">RSS feed</a>\n' if PUBLIC else ''
    chap = ''.join(f'\n          <li><button type="button" data-pod-seek="{t}"><span class="ts">{clock(t)}</span><span class="ct">{esc(title)}</span></button></li>'
                   for title, t, _ in chapters)
    body = ''
    for title, _, lines in chapters:
        body += f'\n            <h3>{esc(title)}</h3>'
        for who, t, text in lines:
            body += f'\n            <p><b>{esc(who)}</b> <button class="ts" type="button" data-pod-seek="{t}" aria-label="{clock(t)}">{clock(t)}</button> {esc(text)}</p>'
    return f'''<!-- podcast:start · generated by tools/build-podcast.py from podcast/podcast.json -->
      <section class="pod" id="podcast" aria-labelledby="podcast-h">
        <div class="pod-top">
          <picture><source type="image/avif" srcset="{w}.avif"><img class="pod-cover" src="{w}.jpg" width="600" height="600" alt="" loading="lazy" decoding="async"></picture>
          <div class="pod-intro">
            <div class="pod-k"><span data-i18n="pod_kicker">Insights podcast</span> · <span data-i18n="pod_episode">Episode</span> {ep["number"]} · {clock(ep["duration"])}</div>
            <h2 class="pod-t" id="podcast-h" data-i18n="pod_title">Listen to the conversation</h2>
            <p class="pod-d" data-i18n="pod_desc">Martin and his co-host Sarah work through this article with a practical case, in English.</p>
            <div class="pod-acts">
              <button class="pod-play" type="button" data-pod-seek="0"><span class="ic-play" aria-hidden="true"></span><span data-i18n="pod_play">Play episode</span></button>
              <a class="pod-link" href="{SHOW["page"]}" data-i18n="pod_all">All episodes</a>
{rss}            </div>
          </div>
        </div>
        <h3 class="pod-h" data-i18n="pod_chapters">Chapters</h3>
        <ol class="pod-ch" lang="en">{chap}
        </ol>
        <details class="pod-tr">
          <summary><span data-i18n="pod_transcript">Transcript</span>{CHEV}</summary>
          <div class="pod-tr-body" lang="en">{body}
            <p class="pod-note">{esc(ep["disclosure"])}</p>
          </div>
        </details>
      </section>
<!-- podcast:end -->'''


def replace_between(s, start, end, new, path):
    a = s.find(start)
    assert a >= 0, f'{path}: marker {start!r} missing'
    b = s.index(end, a) + len(end)
    return s[:a] + new + s[b:]


def rewrite_ld(s, fn):
    m = re.search(r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)', s, re.S)
    ld = json.loads(m.group(2))
    fn(ld)
    return s[:m.start(2)] + json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n    ') + s[m.end(2):]


def audio_object(ep):
    return {'@type': 'AudioObject', 'name': f'{SHOW["title"]} — Episode {ep["number"]}: {ep["title"]}',
            'contentUrl': SITE + ep['audio'], 'encodingFormat': 'audio/mpeg',
            'duration': iso_duration(ep['duration']), 'inLanguage': 'en-US'}


def series_ref():
    ref = {'@type': 'PodcastSeries', '@id': SITE + SHOW['page'] + '#series', 'name': SHOW['title'], 'url': SITE + SHOW['page']}
    if PUBLIC:
        ref['webFeed'] = SITE + SHOW['feed']
    return ref


def rss_autodiscovery(s):
    """<link rel="alternate" type="application/rss+xml"> after the hreflang block
    when the feed is public; none otherwise."""
    s = s.replace(RSS_LINK, '')
    if PUBLIC:
        m = re.search(r'<link rel="alternate" hreflang="x-default" href="[^"]+">\n', s)
        s = s[:m.end()] + RSS_LINK + s[m.end():]
    return s


def episode_node(ep):
    url = SITE + ep['article']
    return {'@type': 'PodcastEpisode', '@id': url + '#podcast', 'url': url + '#podcast', 'name': ep['title'],
            'episodeNumber': ep['number'], 'datePublished': ep['published'][:10],
            'description': ep['summary'] + ' ' + ep['disclosure'], 'inLanguage': 'en-US',
            'associatedMedia': audio_object(ep), 'partOfSeries': series_ref(),
            'author': {'@id': SITE + '/#martin-motlik'}, 'about': {'@id': url + '#article'}}


def build_article(ep, chapters, current):
    path = os.path.join(ROOT, ep['article'].strip('/'), 'index.html')
    s = current.get(path) or open(path, encoding='utf-8').read()
    s = replace_between(s, '<!-- podcast:start', '<!-- podcast:end -->', article_section(ep, chapters), path)
    s = rss_autodiscovery(s)
    s, n = re.subn(r'(<div class="vo-root" id="vo" data-src=")[^"]*(")', lambda m: m.group(1) + ep['audio'] + m.group(2), s)
    assert n == 1, f'{path}: player (#vo data-src) not found'

    def ld(g):
        graph = g['@graph']
        art = next(n for n in graph if n.get('@type') == 'TechArticle')
        art['audio'] = audio_object(ep)
        graph[:] = [n for n in graph if n.get('@type') != 'PodcastEpisode'] + [episode_node(ep)]
    return path, rewrite_ld(s, ld)


# ── Show page: episode list and JSON-LD ──────────────────────────────────────

def episode_list(eps):
    out = ['<!-- episodes:start · generated by tools/build-podcast.py from podcast/podcast.json -->', '      <ol class="eps">']
    for ep, size, chapters in sorted(eps, key=lambda e: e[0]['number'], reverse=True):
        d = datetime.fromisoformat(ep['published'])
        out.append(f'''        <li>
          <a class="ep" href="{ep["article"]}#podcast">
            <div class="ep-meta"><span data-i18n="ep_label">Episode</span> {ep["number"]} · <time datetime="{d.date()}">{d.strftime("%b")} {d.day}, {d.year}</time> · {round(ep["duration"] / 60)} <span data-i18n="ep_min">min</span></div>
            <h3 lang="en">{esc(ep["title"])}</h3>
            <p>{esc(ep["summary"])}</p>
            <span class="ep-go" data-i18n="ep_go">Listen and read the article →</span>
          </a>
        </li>''')
    out += ['      </ol>', '<!-- episodes:end -->']
    return '\n'.join(out)


def subscribe_block():
    if PUBLIC:
        body = (f'        <div class="subs">\n          <a class="btn btn-blue" href="{SITE + SHOW["feed"]}" data-i18n="rss">Subscribe via RSS</a>\n        </div>\n'
                f'        <p class="feed-url"><span data-i18n="feed_label">Feed URL for your podcast app:</span> <code>{SITE + SHOW["feed"]}</code></p>')
    else:
        body = '        <p class="web-only" data-i18n="web_only">New episodes are published here, together with each new article.</p>'
    return '<!-- subscribe:start · generated by tools/build-podcast.py -->\n' + body + '\n<!-- subscribe:end -->'


def build_show_page(eps, current):
    path = os.path.join(ROOT, SHOW['page'].strip('/'), 'index.html')
    s = current.get(path) or open(path, encoding='utf-8').read()
    s = replace_between(s, '<!-- episodes:start', '<!-- episodes:end -->', episode_list(eps), path)
    s = replace_between(s, '<!-- subscribe:start', '<!-- subscribe:end -->', subscribe_block(), path)
    s = rss_autodiscovery(s)

    def ld(g):
        graph = g['@graph']
        series = next(n for n in graph if n.get('@type') == 'PodcastSeries')
        series.update({'@id': SITE + SHOW['page'] + '#series', 'name': SHOW['title'], 'description': SHOW['description'],
                       'url': SITE + SHOW['page'], 'image': SITE + SHOW['cover'],
                       'inLanguage': 'en-US', 'author': {'@id': SITE + '/#martin-motlik'}})
        series.pop('webFeed', None)
        if PUBLIC:
            series['webFeed'] = SITE + SHOW['feed']
        graph[:] = [n for n in graph if n.get('@type') != 'PodcastEpisode'] + [episode_node(ep) for ep, _, _ in eps]
    return path, rewrite_ld(s, ld)


def build():
    eps = [(ep, *episode_files(ep)) for ep in EPISODES]
    assert len({e['number'] for e in EPISODES}) == len(EPISODES), 'episode numbers repeat'
    # None = the file must not exist (the feed while the podcast is web-only)
    files = {os.path.join(ROOT, SHOW['feed'].strip('/')): feed(eps) if PUBLIC else None}
    for ep, size, chapters in eps:
        files[os.path.join(ROOT, 'assets', 'podcast', ep['slug'] + '.chapters.json')] = chapters_json(chapters)
        p, s = build_article(ep, chapters, files)
        files[p] = s
    p, s = build_show_page(eps, files)
    files[p] = s
    # The Insights list links the feed for autodiscovery too
    lp = os.path.join(ROOT, 'insights', 'index.html')
    files[lp] = rss_autodiscovery(files.get(lp) or open(lp, encoding='utf-8').read())
    return files


def stale_files(files):
    return [f for f, s in files.items()
            if (s is None and os.path.exists(f)) or (s is not None and (not os.path.exists(f) or open(f, encoding='utf-8').read() != s))]


def write(files, stale):
    for f in stale:
        if files[f] is None:
            os.remove(f)
            print('removed', os.path.relpath(f, ROOT))
            continue
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'w', encoding='utf-8').write(files[f])
        print('wrote', os.path.relpath(f, ROOT))


def main():
    files = build()
    stale = stale_files(files)
    if '--check' in sys.argv:
        for f in stale:
            print('out of date:', os.path.relpath(f, ROOT))
        sys.exit(1 if stale else 0)
    write(files, stale)


if __name__ == '__main__':
    main()

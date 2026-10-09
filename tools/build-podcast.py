#!/usr/bin/env python3
"""Build the podcast "Insights with Martin Motlík" from podcast/podcast.json.

    python3 tools/build-podcast.py            # write everything below
    python3 tools/build-podcast.py --check    # fail if anything is out of date

tools/build-i18n.py runs this first, so one command builds the whole site.

Writes (generated blocks sit between <!-- name:start --> / <!-- name:end --> markers):
    podcast/feed.xml                       RSS for Apple & co. — only while show.feed_public is true
    assets/podcast/<slug>.chapters.json    Podcasting 2.0 chapters
    <article>/index.html                   episode card (podcast), chapter chips on H2s,
                                           "Also a podcast" (toc-pod), mini player (pod-mini),
                                           player data (pod-data), JSON-LD
    insights/podcast/index.html            latest episode + list (episodes), e-mail opt-in
                                           (notify-btn, notify-form), pod-mini, pod-data, JSON-LD

The player itself is assets/podcast/podcast.js. Each episode needs an MP3, a
WebVTT file and the transcript in Markdown (chapters "### Title [m:ss]", lines
"**Name** [m:ss]: text"); covers come from tools/podcast-cover.html.
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
ENDPOINT = SHOW.get('subscribe_endpoint') or ''
PLATFORMS = SHOW.get('platforms') or []      # Apple Podcasts, Spotify: hero buttons and sameAs
RSS_LINK = f'    <link rel="alternate" type="application/rss+xml" title="{SHOW["title"]} (podcast)" href="{SITE}{SHOW["feed"]}">\n'
SPEAKER_CLASS = {'Martin': 'who-host'}            # everyone else gets the co-host colour


def esc(s):
    return html.escape(s, quote=True)


def clock(sec):
    sec = int(sec)                                 # whole seconds, as the player shows them
    h, m, s = sec // 3600, sec // 60 % 60, sec % 60
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'


def iso_duration(sec):
    sec = int(sec)
    return f'PT{sec // 60}M{sec % 60}S'


def seconds(ts):
    return sum(int(p) * 60 ** i for i, p in enumerate(reversed(ts.split(':'))))


def ep_tag(ep):
    return 'EP ' + str(ep['number']).zfill(2)


def picture(base, size, px, cls='', lazy=True):
    """<picture> for the covers rendered by tools/podcast-cover.html (base-<px>.avif/.jpg)."""
    c = f' class="{cls}"' if cls else ''
    load = ' loading="lazy"' if lazy else ''
    return (f'<picture><source type="image/avif" srcset="{base}-{px}.avif">'
            f'<img{c} src="{base}-{px}.jpg" width="{size}" height="{size}" alt=""{load} decoding="async"></picture>')


def parse_transcript(path):
    """→ [(chapter_title, start, [(speaker, start, text), ...]), ...]"""
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
    """Checks the files an episode needs; returns (bytes, chapters)."""
    audio = os.path.join(ROOT, ep['audio'].lstrip('/'))
    assert os.path.exists(audio), f'missing {ep["audio"]}'
    for px in (96, 144, 264):
        for ext in ('avif', 'jpg'):
            assert os.path.exists(os.path.join(ROOT, f'{ep["cover"]}-{px}.{ext}'.lstrip('/'))), f'missing cover {ep["cover"]}-{px}.{ext}'
    vtt = open(os.path.join(ROOT, ep['captions'].lstrip('/')), encoding='utf-8').read()
    assert vtt.startswith('WEBVTT'), f'{ep["captions"]} is not WebVTT'
    last = re.findall(r'--> (\d\d):(\d\d):(\d\d)\.(\d+)', vtt)[-1]
    end = int(last[0]) * 3600 + int(last[1]) * 60 + int(last[2])
    assert abs(end - ep['duration']) <= 3, f'{ep["slug"]}: duration {ep["duration"]} s, captions end at {end} s'
    chapters = parse_transcript(ep['transcript'])
    starts = {t for _, t, _ in chapters}
    for h2, t in ep.get('h2', {}).items():
        assert t in starts, f'{ep["slug"]}: H2 "{h2}" points to {t} s, which is no chapter start'
    return os.path.getsize(audio), chapters


# ── RSS ──────────────────────────────────────────────────────────────────────

def feed(eps):
    page, feed_url, cover = SITE + SHOW['page'], SITE + SHOW['feed'], SITE + SHOW['cover']
    # Podcasting 2.0 GUID: UUIDv5 of the feed URL without the scheme.
    guid = uuid.uuid5(uuid.UUID('ead4c236-bf58-58c6-a2c6-a6b28d128cb6'), feed_url.split('://', 1)[1])
    cats = ''.join(
        f'\n  <itunes:category text="{esc(c[0])}">' + (f'<itunes:category text="{esc(c[1])}"/>' if len(c) > 1 else '') + '</itunes:category>'
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
    <itunes:image href="{SITE + ep["cover"]}-3000.jpg"/>
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


# ── Shared blocks ────────────────────────────────────────────────────────────

ICON = '<span class="i-play" aria-hidden="true"></span><span class="i-pause" aria-hidden="true"><i></i><i></i></span>'
CHEV = '<svg class="chev" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"></path></svg>'


def lines_of(chapters):
    return [line for _, _, lines in chapters for line in lines]


def pod_data(ep, chapters):
    data = {'id': ep['slug'], 'number': ep['number'], 'audio': ep['audio'], 'duration': ep['duration'],
            'chapters': [[t, title] for title, t, _ in chapters], 'lines': [t for _, t, _ in lines_of(chapters)]}
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return f'<!-- pod-data:start · generated by tools/build-podcast.py -->\n<script type="application/json" id="pod-data">{blob}</script>\n<!-- pod-data:end -->'


def mini(ep):
    return f'''<!-- pod-mini:start · generated by tools/build-podcast.py -->
<div class="pod-mini" id="pod-mini" role="region" aria-label="Podcast player" data-i18n-attr="aria-label:mini_aria" aria-hidden="true">
  {picture(ep["cover"], 40, 96, "pm-cover")}
  <div class="pm-txt"><div class="pm-st" data-pod-status></div><div class="pm-ti" data-pod-chapter-title lang="en"></div></div>
  <span class="pod-time" data-pod-time>0:00</span>
  <button class="pod-rate" type="button" data-pod-rate aria-label="Playback speed" data-i18n-attr="aria-label:speed">1×</button>
  <button class="pod-round" type="button" data-pod-toggle aria-label="Play episode" data-i18n-attr="aria-label:play_episode">{ICON}</button>
  <button class="pm-x" type="button" data-pod-close aria-label="Close the player" data-i18n-attr="aria-label:close">×</button>
  <div class="pm-bar" aria-hidden="true"><div data-pod-progress></div></div>
</div>
<!-- pod-mini:end -->'''


# ── Article ──────────────────────────────────────────────────────────────────

def episode_card(ep, chapters):
    chap = ''.join(
        f'\n            <li><button type="button" data-pod-seek="{t}" data-pod-chapter="{i}"><span class="ts">{clock(t)}</span><span class="ct">{esc(title)}</span><span class="dot" aria-hidden="true"></span></button></li>'
        for i, (title, t, _) in enumerate(chapters))
    rows = ''.join(
        f'\n              <button type="button" class="ep-line" data-pod-seek="{t}" data-pod-line="{i}"><span class="who {SPEAKER_CLASS.get(who, "who-guest")}">{esc(who)}</span><span class="tx">{esc(text)}</span><span class="ts">{clock(t)}</span></button>'
        for i, (who, t, text) in enumerate(lines_of(chapters)))
    return f'''<!-- podcast:start · generated by tools/build-podcast.py from podcast/podcast.json -->
      <section class="ep-card" id="episode" aria-labelledby="episode-h">
        <div class="ep-top">
          {picture(ep["cover"], 132, 264, "ep-cover")}
          <div class="ep-intro">
            <div class="ep-k"><span data-i18n="pod_kicker">Insights Podcast</span> · {ep_tag(ep)} · {clock(ep["duration"])}</div>
            <h2 class="ep-t" id="episode-h" data-i18n="pod_title">Listen to the conversation</h2>
            <p class="ep-d" data-i18n="pod_desc">Martin and his co-host Sarah work through this article with a practical case, in English.</p>
            <div class="ep-acts">
              <button class="pod-btn" type="button" data-pod-toggle="card"><span class="pod-btn-ic">{ICON}</span><span data-pod-label data-i18n="pod_play">Play episode</span></button>
              <a class="pod-btn2" href="{SHOW["page"]}" data-i18n="pod_all">All episodes →</a>
            </div>
          </div>
        </div>
        <div class="ep-bar" aria-hidden="true"><div data-pod-progress></div></div>
        <div class="ep-chs" id="chapters">
          <h3 class="ep-h" data-i18n="pod_chapters">Chapters</h3>
          <ol class="ep-ch" lang="en">{chap}
          </ol>
        </div>
        <div class="ep-tr" id="transcript">
          <button class="ep-tr-h" type="button" aria-expanded="false" aria-controls="ep-tr-body" data-pod-transcript><span data-i18n="pod_transcript">Transcript</span><span class="ep-tr-s"><span data-i18n="pod_synced">Synced with audio</span>{CHEV}</span></button>
          <div class="ep-tr-body" id="ep-tr-body"><div class="ep-tr-in" lang="en">{rows}
          </div></div>
        </div>
        <p class="ep-note" data-i18n="pod_note">{esc(ep["note"])}</p>
      </section>
<!-- podcast:end -->'''


def toc_card(ep):
    return f'''<!-- toc-pod:start · generated by tools/build-podcast.py -->
      <a class="toc-pod" href="#episode">
        {picture(ep["cover"], 40, 96, "tp-cover")}
        <span class="tp-txt"><span class="tp-t" data-i18n="also_podcast">Also a podcast</span><span class="tp-s">{round(ep["duration"] / 60)} <span data-i18n="ep_min">min</span> · <span data-i18n="also_listen">Listen</span></span></span>
      </a>
<!-- toc-pod:end -->'''


def chips(s, ep, path):
    """Put "Listen from m:ss" under each mapped H2, in .h2-row (idempotent)."""
    s = re.sub(r'<div class="h2-row">(<h2\b[^>]*>.*?</h2>)<button class="ch-chip".*?</button></div>', r'\1', s, flags=re.S)
    for h2, t in ep.get('h2', {}).items():
        m = re.search(r'<h2\b[^>]*\bid="%s"[^>]*>.*?</h2>' % re.escape(h2), s, re.S)
        assert m, f'{path}: no <h2 id="{h2}">'
        chip = (f'<button class="ch-chip" type="button" data-pod-seek="{t}" data-pod-chip>'
                f'<span class="i-play" aria-hidden="true"></span><span><span data-i18n="chip_at">Listen from</span> <span class="cc-t">{clock(t)}</span></span></button>')
        s = s[:m.start()] + '<div class="h2-row">' + m.group(0) + chip + '</div>' + s[m.end():]
    return s


def replace_between(s, name, new, path):
    start, end = f'<!-- {name}:start', f'<!-- {name}:end -->'
    a = s.find(start)
    assert a >= 0, f'{path}: marker <!-- {name}:start --> missing'
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
            'duration': iso_duration(ep['duration']), 'uploadDate': ep['published'], 'inLanguage': 'en-US',
            'caption': {'@type': 'MediaObject', 'contentUrl': SITE + ep['captions'], 'encodingFormat': 'text/vtt', 'inLanguage': 'en-US'}}


def series_ref():
    ref = {'@type': 'PodcastSeries', '@id': SITE + SHOW['page'] + '#series', 'name': SHOW['title'], 'url': SITE + SHOW['page']}
    if PUBLIC:
        ref['webFeed'] = SITE + SHOW['feed']
    return ref


def episode_node(ep):
    url = SITE + ep['article']
    return {'@type': 'PodcastEpisode', '@id': url + '#episode', 'url': url + '#episode', 'name': ep['title'],
            'episodeNumber': ep['number'], 'datePublished': ep['published'][:10],
            'description': ep['summary'] + ' ' + ep['disclosure'], 'inLanguage': 'en-US',
            'image': f'{SITE}{ep["cover"]}-3000.jpg', 'isAccessibleForFree': True,
            'associatedMedia': audio_object(ep), 'partOfSeries': series_ref(),
            'author': {'@id': SITE + '/#martin-motlik'}, 'about': {'@id': url + '#article'}}


def rss_autodiscovery(s):
    s = s.replace(RSS_LINK, '')
    if PUBLIC:
        m = re.search(r'<link rel="alternate" hreflang="x-default" href="[^"]+">\n', s)
        s = s[:m.end()] + RSS_LINK + s[m.end():]
    return s


def build_article(ep, chapters, current):
    path = os.path.join(ROOT, ep['article'].strip('/'), 'index.html')
    s = current.get(path) or open(path, encoding='utf-8').read()
    s = replace_between(s, 'podcast', episode_card(ep, chapters), path)
    s = replace_between(s, 'toc-pod', toc_card(ep), path)
    s = replace_between(s, 'pod-mini', mini(ep), path)
    s = replace_between(s, 'pod-data', pod_data(ep, chapters), path)
    s = chips(s, ep, path)
    s = rss_autodiscovery(s)

    def ld(g):
        graph = g['@graph']
        art = next(n for n in graph if n.get('@type') == 'TechArticle')
        art['audio'] = audio_object(ep)
        graph[:] = [n for n in graph if n.get('@type') != 'PodcastEpisode'] + [episode_node(ep)]
    return path, rewrite_ld(s, ld)


# ── Show page ────────────────────────────────────────────────────────────────

HERO = '/assets/img/ai-search-hero'                # article hero renditions, per episode later if needed


def latest_card(ep, chapters):
    d = datetime.fromisoformat(ep['published'])
    return f'''      <article class="latest" data-pod-started aria-labelledby="latest-h">
        <div class="latest-img">
          <picture>
            <source type="image/avif" sizes="(min-width: 900px) 480px, 100vw" srcset="{HERO}-600.avif 600w, {HERO}-900.avif 900w, {HERO}-1280.avif 1280w">
            <img src="{HERO}-900.jpg" sizes="(min-width: 900px) 480px, 100vw" srcset="{HERO}-600.jpg 600w, {HERO}-900.jpg 900w, {HERO}-1280.jpg 1280w" width="1672" height="941" alt="" loading="lazy" decoding="async">
          </picture>
          <span class="latest-flag"><span data-i18n="latest">Latest</span> · {ep_tag(ep)}</span>
        </div>
        <div class="latest-txt">
          <div class="latest-meta"><span class="cat">{esc(ep["category"])}</span><time datetime="{d.date()}">{d.strftime("%b")} {d.day}, {d.year}</time><span>·</span><span>{round(ep["duration"] / 60)} <span data-i18n="ep_min">min</span></span></div>
          <h3 id="latest-h" lang="en"><a href="{ep["article"]}#episode">{esc(ep["title"])}</a></h3>
          <p>{esc(ep["teaser"])}</p>
          <div class="latest-player">
            <button class="pod-round is-lg" type="button" data-pod-toggle aria-label="Play episode" data-i18n-attr="aria-label:play_episode">{ICON}</button>
            <div class="pod-wave" data-pod-wave aria-label="Seek within the episode" data-i18n-attr="aria-label:seek"></div>
            <span class="pod-time"><span data-pod-time>0:00</span> / {clock(ep["duration"])}</span>
          </div>
          <div class="latest-ch" data-pod-chapter-line lang="en"></div>
          <div class="latest-foot"><a class="pod-btn2" href="{ep["article"]}" data-i18n="read_article">Read the article →</a><a href="{ep["article"]}#chapters" data-i18n="pod_chapters">Chapters</a><a href="{ep["article"]}#transcript" data-i18n="pod_transcript">Transcript</a></div>
        </div>
      </article>'''


def more_row(ep):
    d = datetime.fromisoformat(ep['published'])
    return f'''        <li class="more-ep">
          {picture(ep["cover"], 72, 144, "me-cover")}
          <div class="me-txt">
            <div class="me-meta"><b>{ep_tag(ep)}</b><span class="cat">{esc(ep["category"])}</span><span><time datetime="{d.date()}">{d.strftime("%b")} {d.day}, {d.year}</time> · {round(ep["duration"] / 60)} <span data-i18n="ep_min">min</span></span></div>
            <h3 lang="en"><a href="{ep["article"]}#episode">{esc(ep["title"])}</a></h3>
          </div>
          <a href="{ep["article"]}#episode" data-i18n="read_article">Read the article →</a>
          <a class="pod-round is-soft" href="{ep["article"]}#episode" tabindex="-1" aria-hidden="true"><span class="i-play"></span></a>
        </li>'''


def episode_list(eps):
    eps = sorted(eps, key=lambda e: e[0]['number'], reverse=True)
    latest, rest = eps[0], eps[1:]
    n = len(eps)
    out = ['<!-- episodes:start · generated by tools/build-podcast.py from podcast/podcast.json -->',
           f'      <div class="eps-head"><h2 id="episodes-h" data-i18n="episodes_title">Episodes</h2><span class="eps-count">{n} <span data-i18n="{"ep_count_one" if n == 1 else "ep_count_many"}">{"episode" if n == 1 else "episodes"}</span></span></div>',
           latest_card(latest[0], latest[2])]
    if rest:
        out += ['      <ol class="more-eps">'] + [more_row(e[0]) for e in rest] + ['      </ol>']
    out.append('<!-- episodes:end -->')
    return '\n'.join(out)


BELL = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.7 21a2 2 0 0 1-3.4 0"></path></svg>'


def notify_button():
    body = (f'          <button class="pod-btn2" type="button" data-notify-toggle aria-expanded="false" aria-controls="notify">{BELL}<span data-i18n="get_new">Get new episodes</span></button>\n'
            if ENDPOINT else '')
    return '<!-- notify-btn:start · generated by tools/build-podcast.py (show.subscribe_endpoint) -->\n' + body + '<!-- notify-btn:end -->'


def notify_form():
    body = ''
    if ENDPOINT:
        body = f'''        <div class="notify" id="notify"><div class="notify-in">
          <form class="notify-f" action="{esc(ENDPOINT)}" method="POST" data-notify novalidate>
            <label class="sr" for="notify-email" data-i18n="email_label">Email address</label>
            <input id="notify-email" name="email" type="email" autocomplete="email" placeholder="you@company.com" aria-describedby="notify-msg" required>
            <input type="hidden" name="_subject" value="New podcast subscriber: {esc(SHOW["title"])}">
            <button type="submit" data-notify-submit data-i18n="notify_me">Notify me</button>
          </form>
          <p class="notify-help" id="notify-msg" data-notify-msg data-i18n="notify_help" aria-live="polite">One email per new episode. No newsletter, unsubscribe anytime.</p>
        </div></div>
'''
    return '<!-- notify-form:start · generated by tools/build-podcast.py (show.subscribe_endpoint) -->\n' + body + '<!-- notify-form:end -->'


OUT = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"></path><path d="M8 7h9v9"></path></svg>'


def listen_links():
    body = ''.join(f'          <a class="pod-btn2" href="{esc(p["url"])}" target="_blank" rel="noopener"><span class="sr" data-i18n="listen_on">Listen on</span> {esc(p["name"])}{OUT}</a>\n'
                   for p in PLATFORMS)
    return '<!-- listen:start · generated by tools/build-podcast.py (show.platforms) -->\n' + body + '<!-- listen:end -->'


def build_show_page(eps, current):
    path = os.path.join(ROOT, SHOW['page'].strip('/'), 'index.html')
    s = current.get(path) or open(path, encoding='utf-8').read()
    latest = sorted(eps, key=lambda e: e[0]['number'])[-1]
    s = replace_between(s, 'episodes', episode_list(eps), path)
    s = replace_between(s, 'notify-btn', notify_button(), path)
    s = replace_between(s, 'notify-form', notify_form(), path)
    s = replace_between(s, 'listen', listen_links(), path)
    s = replace_between(s, 'pod-mini', mini(latest[0]), path)
    s = replace_between(s, 'pod-data', pod_data(latest[0], latest[2]), path)
    s = rss_autodiscovery(s)

    title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
    description = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    page = SITE + SHOW['page']

    def ld(g):
        graph = g['@graph']
        series = next(n for n in graph if n.get('@type') == 'PodcastSeries')
        series.clear()
        series.update({
            '@type': 'PodcastSeries', '@id': page + '#series', 'name': SHOW['title'], 'description': SHOW['description'],
            'url': page, 'image': SITE + SHOW['cover'], 'inLanguage': 'en-US',
            'author': {'@id': SITE + '/#martin-motlik'}, 'publisher': {'@id': SITE + '/#martin-motlik'},
            'about': [{'@type': 'Thing', 'name': t} for t in SHOW['topics']], 'keywords': ', '.join(SHOW['topics']),
            'isAccessibleForFree': True,
            'hasPart': [{'@id': SITE + ep['article'] + '#episode'} for ep, _, _ in sorted(eps, key=lambda e: e[0]['number'])],
        })
        if PUBLIC:
            series['webFeed'] = SITE + SHOW['feed']
        if PLATFORMS:
            series['sameAs'] = [p['url'] for p in PLATFORMS]
        # The page itself; tools/build-i18n.py gives the language versions their
        # own URL, inLanguage, name and description.
        webpage = {'@type': 'CollectionPage', '@id': page, 'url': page, 'name': title, 'description': description,
                   'inLanguage': 'en-US', 'isPartOf': {'@id': SITE + '/#website'},
                   'about': {'@id': page + '#series'}, 'mainEntity': {'@id': page + '#series'},
                   'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + '/assets/podcast/cover-1200.jpg', 'width': 1200, 'height': 1200},
                   'author': {'@id': SITE + '/#martin-motlik'}}
        keep = [n for n in graph if n.get('@type') not in ('PodcastEpisode', 'CollectionPage')]
        graph[:] = keep + [webpage] + [episode_node(ep) for ep, _, _ in eps]
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
    lp = os.path.join(ROOT, 'insights', 'index.html')          # the Insights list links the feed too
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

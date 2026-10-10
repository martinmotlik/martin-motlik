"""Prepares one Instagram story teaser: the audio track and the render page.

    python3 tools/ig-story/prepare.py <config.json> <episode.wav> <work dir>

Reads a teaser config (see teasers/*.json and README.md) and the episode as
16-bit stereo WAV, then writes into the work dir:

- audio.wav   the story's soundtrack: silence for the opening scene, the clip
              (10 ms fade in, 60 ms fade out), silence for the closing scene
- story.html  the design bundle, patched: the full-quality photo, the clip's
              start and length, word timings measured from the audio, caption
              breaks, the real voice envelope for the waveform, and the Listen
              scene set to the clip length
- timing.json the words and caption chunks, for checking

The design is an exported bundle ("Bundled Page") whose animation component
defines Q_FROM / Q_LEN / Q_TX / Q_CHUNKS / qAmp, as in
"IG Story - Be the source.html". Its scenes are Article → Listen → Hold.
"""
import array, base64, gzip, json, math, os, re, sys, wave

CFG, EP_WAV, WORK = sys.argv[1:4]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cfg = json.load(open(CFG, encoding='utf-8'))
path = lambda p: os.path.join(ROOT, os.path.expanduser(p))
FROM, LEN = cfg['from'], cfg['len']
os.makedirs(WORK, exist_ok=True)

# ── design bundle
html = open(path(cfg['design']), encoding='utf-8').read()


def block(name):
    m = re.search(r'(<script type="__bundler/' + name + r'">\s*)(.*?)(\s*</script>)', html, re.S)
    assert m, f'bundle has no {name} block'
    return m


man = json.loads(block('manifest').group(2))
tpl = json.loads(block('template').group(2))
names = {e['id']: e['uuid'] for e in json.loads(block('ext_resources').group(2))}


def text_of(entry):
    raw = base64.b64decode(entry['data'])
    return (gzip.decompress(raw) if entry.get('compressed') else raw).decode('utf-8', 'replace')


scenes = json.loads(re.search(r"window\.OM_SCENES = '(.*?)';", tpl).group(1))
dur = {s['name']: s['dur'] for s in scenes}
LEAD, TAIL = dur['Article'], dur['Hold']

# ── audio
w = wave.open(EP_WAV)
SR = w.getframerate()
assert w.getnchannels() == 2 and w.getsampwidth() == 2, 'episode WAV must be 16-bit stereo'
w.setpos(round(FROM * SR))
n = round(LEN * SR)
clip = array.array('h', w.readframes(n))
fi, fo = int(0.010 * SR), int(0.060 * SR)
for i in list(range(fi)) + list(range(n - fo, n)):
    g = min(1.0, i / fi, (n - 1 - i) / fo)
    clip[2 * i] = int(clip[2 * i] * g)
    clip[2 * i + 1] = int(clip[2 * i + 1] * g)
track = array.array('h', bytes(4 * round(LEAD * SR))) + clip + array.array('h', bytes(4 * round(TAIL * SR)))
out = wave.open(os.path.join(WORK, 'audio.wav'), 'wb')
out.setnchannels(2); out.setsampwidth(2); out.setframerate(SR)
out.writeframes(track.tobytes()); out.close()

# voice envelope for the waveform: 100 values per second, −52 dB → 0, −12 dB → 1
hop = SR // 100
env = []
for i in range(0, n - hop + 1, hop):
    s = sum(((clip[2 * j] + clip[2 * j + 1]) / 2) ** 2 for j in range(i, i + hop))
    db = 20 * math.log10(max(math.sqrt(s / hop), 1) / 32768)
    env.append(max(0.0, min(1.0, (db + 52) / 40)))
env = [round(sum(env[max(0, k - 1):k + 2]) / len(env[max(0, k - 1):k + 2]), 3) for k in range(len(env))]

# ── words: each span is one stretch of speech between two measured pauses;
# words are spread over it by length. " | " in the text marks a caption break,
# and with manual_breaks every span also ends its caption.
MANUAL = bool(cfg.get('manual_breaks'))
words = []
for a, b, text in cfg['spans']:
    toks = text.split(' ')
    ws = [t for t in toks if t != '|']
    brk, k = set(), -1
    for t in toks:
        if t == '|':
            brk.add(k)
        else:
            k += 1
    weights = [len(x) + 1 for x in ws]
    tot, acc = sum(weights), 0
    for j, (x, wt) in enumerate(zip(ws, weights)):
        words.append({'w': x, 't': round(a - FROM + (b - a) * acc / tot, 3), 'e': round(a - FROM + (b - a) * (acc + wt) / tot, 3),
                      'br': j in brk or (MANUAL and j == len(ws) - 1)})
        acc += wt
assert all(0 <= x['t'] < LEN for x in words), 'a span lies outside the clip'

chunks, cur = [], []
for i, x in enumerate(words):
    cur.append(x)
    auto = (len(cur) >= 2 and re.search(r'[.”]$', x['w'])) or (len(cur) >= 4 and x['w'].endswith(',')) or len(cur) >= 7
    if i == len(words) - 1 or (x['br'] if MANUAL else auto):
        chunks.append({'s': cur[0]['t'], 'e': x['e'], 'words': [{'w': y['w'], 't': y['t']} for y in cur]})
        cur = []

# ── patch the bundle
anim = next(u for u, e in man.items() if e['mime'].endswith(('javascript', 'jsx')) and 'const Q_FROM' in text_of(e))
jsx = text_of(man[anim])


def sub(pattern, new, text):
    out, k = re.subn(pattern, lambda m: new, text, count=1, flags=re.S)
    assert k == 1, pattern
    return out


jsx = sub(r'const Q_FROM = [\d.]+, Q_LEN = [\d.]+;', f'const Q_FROM = {FROM}, Q_LEN = {LEN};', jsx)
jsx = sub(r"const Q_TX = '.*?';\n", 'const Q_TX = ' + json.dumps(' '.join(x['w'] for x in words), ensure_ascii=False) + ';\n'
          + 'const Q_ENV = ' + json.dumps(env) + ';\n', jsx)
jsx = sub(r'const Q_CHUNKS = \(\(\) => \{.*?\}\)\(\);\n', '// caption chunks measured from the audio (tools/ig-story/prepare.py)\nconst Q_CHUNKS = '
          + json.dumps(chunks, ensure_ascii=False) + ';\n', jsx)
jsx = sub(r'const qAmp = .*?\n\};\n', '''// the real voice envelope of the clip, 100 values per second
const qAmp = (t) => {
  if (t < 0 || t > Q_LEN) return 0.04;
  const x = t * 100, i = Math.floor(x), f = x - i;
  const a = Q_ENV[Math.min(i, Q_ENV.length - 1)] || 0, b = Q_ENV[Math.min(i + 1, Q_ENV.length - 1)] || 0;
  return Math.max(0.04, a + (b - a) * f);
};
''', jsx)
man[anim] = {'mime': man[anim]['mime'], 'compressed': False, 'data': base64.b64encode(jsx.encode('utf-8')).decode()}

if cfg.get('photo'):
    hero = names['heroImg']
    man[hero] = {'mime': 'image/jpeg', 'compressed': False, 'data': base64.b64encode(open(path(cfg['photo']), 'rb').read()).decode()}

tpl, k = re.subn(r'(\{"name":"Listen","dur":)[\d.]+', lambda m: m.group(1) + str(LEN), tpl, count=1)
assert k == 1, 'no Listen scene'
if cfg.get('variant'):
    tpl = re.sub(r'("variant": ")[^"]*(")', lambda m: m.group(1) + cfg['variant'] + m.group(2), tpl, count=1)

# the template sits inside <script>: keep "</" escaped
html = html.replace(block('template').group(2), json.dumps(tpl).replace('</', '<\\/'))
html = html.replace(block('manifest').group(2), json.dumps(man))
open(os.path.join(WORK, 'story.html'), 'w', encoding='utf-8').write(html)

total = round(LEAD + LEN + TAIL, 3)
json.dump({'total': total, 'lead': LEAD, 'tail': TAIL, 'chunks': [
    {'from': round(c['s'] + LEAD, 2), 'to': round(c['e'] + LEAD, 2), 'text': ' '.join(y['w'] for y in c['words'])} for c in chunks]},
    open(os.path.join(WORK, 'timing.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'prepared: {total} s ({LEAD} + {LEN} + {TAIL}), {len(words)} words, {len(chunks)} captions')
for c in chunks:
    print(f"  {c['s'] + LEAD:6.2f}–{c['e'] + LEAD:6.2f}  {' '.join(y['w'] for y in c['words'])}")

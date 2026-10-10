"""Turns a podcast script into the scenes JSON for ElevenLabs Text to Dialogue.

    python3 tools/insights/script-to-scenes.py _insights/<slug>/podcast/script.md [--check]

Reads every `### Scene N · Title` block and its `**SPEAKER:** text` lines,
writes `scenes.json` next to the script ([{scene, inputs: [{speaker, text}]}]),
rewrites each scene's `*NNN characters*` line, and prints the totals: characters,
scenes, speaking share per speaker and the estimated length (EP 01: 11,865
characters → 14:08). Fails when a scene has 2,000 characters or more (one
ElevenLabs request per scene) or a scene title looks like a production label.
--check only reports, it writes nothing.
"""
import json, os, re, sys

SEC_PER_CHAR = 848 / 11865          # measured on EP 01
LIMIT = 2000
LABELS = re.compile(r'\b(cold open|scene|take|sting|intro music|outro)\b', re.I)

path = sys.argv[1]
check = '--check' in sys.argv
text = open(path, encoding='utf-8').read()
parts = re.split(r'(?m)^### Scene (\d+) · (.+?)\s*$', text)
if len(parts) < 4:
    sys.exit('no "### Scene N · Title" headings found')

scenes, errors, out = [], [], [parts[0]]
for i in range(1, len(parts), 3):
    num, title, body = parts[i], parts[i + 1], parts[i + 2]
    inputs = [{'speaker': m.group(1), 'text': m.group(2).strip()}
              for m in re.finditer(r'(?m)^\*\*([A-Z][A-Z ]*):\*\* (.+)$', body)]
    chars = sum(len(x['text']) for x in inputs)
    scenes.append({'scene': f'{num} · {title}', 'inputs': inputs, 'chars': chars})
    if chars >= LIMIT:
        errors.append(f'scene {num} has {chars} characters (limit {LIMIT - 1})')
    if LABELS.search(title):
        errors.append(f'scene {num} title "{title}" reads like a production label; chapter titles are public')
    body = re.sub(r'(?m)^\*[\d,]+ characters\*\s*$', f'*{chars} characters*', body, count=1)
    if not re.search(r'(?m)^\*\d+ characters\*', body):
        body = f'  \n*{chars} characters*\n' + body.lstrip('\n')
    out.append(f'### Scene {num} · {title}' + body)

total = sum(s['chars'] for s in scenes)
by = {}
for s in scenes:
    for x in s['inputs']:
        by[x['speaker']] = by.get(x['speaker'], 0) + len(x['text'])
secs = round(total * SEC_PER_CHAR)
print(f'{len(scenes)} scenes, {total:,} characters, about {secs // 60}:{secs % 60:02d}')
for sp, c in sorted(by.items(), key=lambda kv: -kv[1]):
    print(f'  {sp:<8} {c / total:5.1%}')
for s in scenes:
    print(f"  {s['chars']:5}  {s['scene']}")
if errors:
    print('\n'.join('ERROR ' + e for e in errors), file=sys.stderr)
    sys.exit(1)
if not check:
    json.dump([{'scene': s['scene'], 'inputs': s['inputs']} for s in scenes],
              open(os.path.join(os.path.dirname(path), 'scenes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(path, 'w', encoding='utf-8').write(''.join(out))
    print('wrote scenes.json and updated the character counts')

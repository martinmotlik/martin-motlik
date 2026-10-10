"""Exports an Insights article page as readable Markdown (for Google Drive).

    python3 tools/insights/export-article.py insights/<slug>/index.html [out.md]
    python3 tools/insights/export-article.py cs/insights/<cs-slug>/index.html

Keeps the title, dek, lead, headings, paragraphs, lists, quotes, code,
key takeaway and sources; drops navigation, the podcast card, share blocks
and scripts. Writes to stdout without an output path.
"""
import html, re, sys
from html.parser import HTMLParser

SKIP = {'script', 'style', 'nav', 'svg', 'noscript', 'button', 'aside', 'footer', 'header', 'template', 'audio'}
SKIP_CLASS = re.compile(r'\b(ep-card|share|toc|pod-|author|tags|closing|crumbs|byline|cover|h2-chip|ch-chip|sr-only|sr\b)')


class Md(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.buf, self.skip, self.stack, self.in_main = [], [], 0, [], False
        self.list = []

    def flush(self, prefix=''):
        text = re.sub(r'\s+', ' ', ''.join(self.buf)).strip()
        self.buf = []
        if text:
            self.out.append(prefix + text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'main':
            self.in_main = True
        skip = tag in SKIP or SKIP_CLASS.search(a.get('class', '') or '') or a.get('id') == 'episode' or tag == 'details' and 'toc-m' in (a.get('class') or '')
        if self.skip or skip:
            if tag not in ('br', 'img', 'source', 'meta', 'link', 'input'):
                self.stack.append(tag); self.skip += 1
            return
        if not self.in_main:
            return
        if tag in ('h1', 'h2', 'h3', 'p', 'li', 'blockquote', 'pre', 'figcaption'):
            self.flush()
        if tag in ('ul', 'ol'):
            self.list.append([tag, 0])
        if tag == 'a' and 'cite' in (a.get('class') or ''):
            self.buf.append('[')
            self.stack.append('a-cite'); return
        if tag == 'br':
            self.buf.append(' ')
        if tag == 'strong':
            self.buf.append('**')

    def handle_endtag(self, tag):
        if self.skip:
            if self.stack and self.stack[-1] == tag:
                self.stack.pop(); self.skip -= 1
            return
        if tag == 'main':
            self.flush(); self.in_main = False
        if not self.in_main:
            return
        if tag == 'a' and self.stack and self.stack[-1] == 'a-cite':
            self.stack.pop(); self.buf.append(']'); return
        if tag == 'strong':
            self.buf.append('**')
        prefix = {'h1': '# ', 'h2': '\n## ', 'h3': '\n### ', 'blockquote': '> '}.get(tag)
        if prefix:
            self.flush(prefix)
        elif tag == 'li':
            kind = self.list[-1] if self.list else ['ul', 0]
            kind[1] += 1
            self.flush(f'{kind[1]}. ' if kind[0] == 'ol' else '- ')
        elif tag in ('p', 'figcaption'):
            self.flush()
        elif tag == 'pre':
            text = ''.join(self.buf).strip('\n'); self.buf = []
            self.out.append('```\n' + text + '\n```')
        elif tag in ('ul', 'ol') and self.list:
            self.list.pop()

    def handle_data(self, data):
        if not self.skip and self.in_main:
            self.buf.append(data)


src = open(sys.argv[1], encoding='utf-8').read()
canonical = re.search(r'<link rel="canonical" href="([^"]+)"', src)
desc = re.search(r'<meta name="description" content="([^"]*)"', src)
p = Md(); p.feed(src); p.flush()
lines = []
for line in p.out:
    if lines and (line.startswith(('- ', '1.')) or re.match(r'\d+\. ', line)) and re.match(r'(- |\d+\. )', lines[-1]):
        lines.append(line)
    else:
        lines.extend(['', line])
head = [f'Source: {canonical.group(1)}' if canonical else '', f'Description: {html.unescape(desc.group(1))}' if desc else '']
md = '\n'.join(lines).strip() + '\n'
md = md.replace('\n', '\n\n' + '\n'.join(x for x in head if x) + '\n', 1) if head else md
md = re.sub(r'\n{3,}', '\n\n', md)
if len(sys.argv) > 2:
    open(sys.argv[2], 'w', encoding='utf-8').write(md)
else:
    sys.stdout.write(md)

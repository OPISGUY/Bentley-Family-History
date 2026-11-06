#!/usr/bin/env python3
"""Check generated links, anchors, assets and family panels without network access."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1] / 'docs'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets, self.families = [], [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag == 'script' and 'src' in a: self.assets.append(a['src'])
        if tag == 'link' and a.get('rel') == 'stylesheet': self.assets.append(a['href'])
        if tag == 'details' and a.get('class') == 'family': self.families.append(a['id'])

pages, errors = {}, []
for path in ROOT.rglob('*.html'):
    page = Page(); page.feed(path.read_text()); pages[path.resolve()] = page
for path, page in pages.items():
    if len(page.ids) != len(set(page.ids)): errors.append(f'{path.name}: duplicate IDs')
    for link in page.links + page.assets:
        u = urlsplit(link)
        if u.scheme or u.netloc: continue
        target = (path.parent / unquote(u.path)).resolve() if u.path else path
        if not target.is_file(): errors.append(f'{path.name}: missing file {link}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{path.name}: missing anchor {link}')
home = pages[(ROOT / 'index.html').resolve()]
if home.families != [f'family-{n}' for n in range(1,15)]: errors.append('Expected fourteen uniquely ordered family panels')
if not (ROOT / '.nojekyll').is_file(): errors.append('Missing .nojekyll')
if errors: raise SystemExit('\n'.join(errors))
print(f'Passed: {len(pages)} pages, {sum(len(p.links) for p in pages.values())} links, assets, anchors and 14 family panels.')

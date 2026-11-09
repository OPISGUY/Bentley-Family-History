#!/usr/bin/env python3
"""Build the family website using Python's standard library. No network or packages."""
from tree_view import tree
import hashlib
import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
REPO = 'https://github.com/OPISGUY/Bentley-Family-History'
REF = 'ccr-469e384c-x98nc5'

def slug(text):
    return re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')

def inline(text):
    links = []
    def link(m):
        label, url = m.groups()
        if not re.match(r'^(https?://|#|[.\w/-])', url):
            return html.escape(label)
        url = re.sub(r'\.md(?=#|$)', '.html', url)
        links.append(f'<a href="{html.escape(url, quote=True)}">{inline(label)}</a>')
        return f'\x00{len(links)-1}\x00'
    text = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', link, text)
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'^_(.+)_$', r'<em>\1</em>', text)
    return re.sub(r'\x00(\d+)\x00', lambda m: links[int(m[1])], text)

def markdown(text):
    """Render this repository's headings, paragraphs, lists, links, tables and code."""
    lines = text.splitlines()
    output, paragraph = [], []
    list_open = False
    i = 0
    def flush():
        if paragraph:
            output.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            flush()
            if list_open: output.append('</ul>'); list_open = False
            i += 1
            continue
        if s.startswith('```'):
            flush()
            if list_open: output.append('</ul>'); list_open = False
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i]); i += 1
            output.append('<details><summary>Original research diagram / notation</summary><pre>' + html.escape('\n'.join(code)) + '</pre></details>')
        elif s.startswith('|'):
            flush()
            if list_open: output.append('</ul>'); list_open = False
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c.replace(' ', '')) for c in cells): rows.append(cells)
                i += 1
            output.append('<div class="table-scroll" role="region" aria-label="Family records table" tabindex="0"><table>')
            for n, row in enumerate(rows):
                cell = 'th' if n == 0 else 'td'
                output.append('<tr>' + ''.join(f'<{cell}' + (' scope="col"' if n == 0 else '') + '>' + inline(c) + f'</{cell}>' for c in row) + '</tr>')
            output.append('</table></div>')
            continue
        elif re.match(r'^#{1,6} ', s):
            flush()
            if list_open: output.append('</ul>'); list_open = False
            marks, title = s.split(' ', 1)
            output.append(f'<h{len(marks)} id="{slug(title)}">{inline(title)}</h{len(marks)}>')
        elif s.startswith('- '):
            flush()
            if not list_open: output.append('<ul>'); list_open = True
            label = s[2:].replace('[x]', '✓').replace('[ ]', '○')
            output.append('<li>' + inline(label) + '</li>')
        else:
            if list_open and not lines[i].startswith(' '): output.append('</ul>'); list_open = False
            paragraph.append(s)
        i += 1
    flush()
    if list_open: output.append('</ul>')
    return '\n'.join(output)

def shell(title, body, depth=0):
    prefix = '../' * depth
    return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Explore the Bentley family of Marsden and Saddleworth: family groups, historical stories and the evidence behind each connection.">
<title>{html.escape(title)} · Bentley Family History</title><link rel="stylesheet" href="{prefix}style.css"><script defer src="{prefix}app.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a><header><div class="wrap"><a class="brand" href="{prefix}index.html">Bentley<small>A Pennine family history</small></a>
<nav aria-label="Main navigation"><a href="{prefix}index.html#tree">Family tree</a><a href="{prefix}index.html#families">Find a family</a><a href="{prefix}index.html#stories">Our story</a><a href="{prefix}index.html#evidence">The evidence</a></nav></div></header>
<main id="main" class="wrap">{body}</main><footer><div class="wrap"><span>Made for the family. Free to explore. No account needed.<br>Living generations are kept private. Research updated 5 November 2026.</span><span><a href="{prefix}research-plan.html">What we’re researching next</a><br><a href="{REPO}">Research archive on GitHub</a></span></div></footer></body></html>'''

def article(path):
    relative = path.relative_to(ROOT)
    text = path.read_text()
    title = text.splitlines()[0].lstrip('# ')
    depth = len(relative.parts) - 1
    prefix = '../' * depth
    historical = '<div class="note caution"><p>This is an earlier research note. Later findings may change its conclusions. Read the <a href="' + prefix + 'research/2026-11-04-origins-and-limits.html">current explanation of our earliest evidence</a> and the <a href="' + prefix + 'family-groups.html">updated family groups</a>.</p></div>' if relative.name.startswith('2026-10') else ''
    body = f'<article class="reading"><p class="breadcrumb"><a href="{prefix}index.html">← Back to the family home</a></p>{historical}{markdown(text)}<p class="source-link">Research record: <a href="{REPO}/blob/{REF}/{relative.as_posix()}">view this note on GitHub</a></p></article>'
    if relative.name == 'family-tree.md':
        body = body.replace(markdown(text), '<p><a class="button" href="index.html#tree">Browse the tree with siblings →</a></p>' + markdown(text))
    dest = OUT / relative.with_suffix('.html')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(shell(title, body, depth))

def home():
    groups_text = (ROOT / 'family-groups.md').read_text()
    sections = re.split(r'^## ', groups_text, flags=re.M)[1:]
    family_html = []
    for n, section in enumerate(sections, 1):
        title, content = section.split('\n', 1)
        group = 'haigh' if n == 4 else 'platt' if n == 10 else 'bentley'
        clean_title = re.sub(r'^\d+\. ', '', title)
        family_html.append(f'<details class="family" id="family-{n}" data-branch="{group}"><summary>{html.escape(clean_title)}</summary><div class="family-body">{markdown(content)}<a class="permalink" href="#family-{n}">Link to this family</a></div></details>')
    body = tree(sections)
    body += """<section id="families"><h2>Family directory</h2><p>Look up a name, place or year to see the household and its records.</p><div class="tools js-only"><label>Find a person<input id="family-search" type="search" placeholder="Name, place or year"></label><label>Family<select id="branch"><option value="all">All families</option><option value="bentley">Bentley and spouses</option><option value="haigh">Haigh</option><option value="platt">Platt</option></select></label><button id="reset" class="secondary">Clear</button></div><div class="actions js-only"><button id="expand" class="secondary">Open results</button><button id="collapse" class="secondary">Close results</button><button data-print class="secondary">Print</button></div><p id="result-count" role="status"></p><p id="no-results" hidden>No matching household. Try a surname or clear the filters.</p><p class="small">D = documented record · S = supported identification · F = family account</p>""" + ''.join(family_html) + '</section>'
    chapters = (ROOT / 'bentley-lives.md').read_text()
    story_links = ''.join(f'<li><a href="bentley-lives.html#{slug(title)}">{html.escape(title)}</a></li>'
                          for title in re.findall(r'^## (.+)$', chapters, re.M))
    body += '<section id="stories"><h2>Family stories</h2><p>From An’s baptism in 1613 to Roy and Margaret’s wedding in 1953. Choose a life to read.</p><ol class="chapter-list">' + story_links + '</ol><a class="button" href="bentley-lives.html">Read from the beginning →</a></section>'
    body += """<section id="evidence"><h2>Research and sources</h2><p><a href="research-plan.html">Research questions</a> · <a href="research/2026-11-05-earlier-line-search.html">Earlier Bentley records</a> · <a href="family-groups.html">All family records</a></p></section>"""
    page = shell('Our family', body)
    for asset in ('style.css', 'app.js'):
        version = hashlib.sha256((OUT / asset).read_bytes()).hexdigest()[:10]
        page = page.replace(f'"{asset}"', f'"{asset}?v={version}"')
    (OUT / 'index.html').write_text(page)

def build():
    OUT.mkdir(exist_ok=True)
    for asset in ('style.css','app.js'):
        shutil.copyfile(ROOT / 'site' / asset, OUT / asset)
    (OUT / '.nojekyll').write_text('')
    for path in sorted(ROOT.glob('*.md')) + sorted((ROOT / 'research').glob('*.md')):
        article(path)
    home()
    print(f'Built {len(list(OUT.rglob("*.html")))} pages in docs/')

if __name__ == '__main__':
    build()

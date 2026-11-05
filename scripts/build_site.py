#!/usr/bin/env python3
"""Build the family website using Python's standard library. No network or packages."""
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
<main id="main" class="wrap">{body}</main><footer><div class="wrap"><span>Made for the family. Free to explore. No account needed.<br>Living generations are kept private. Research updated 4 November 2026.</span><span><a href="{prefix}research-plan.html">What we’re researching next</a><br><a href="{REPO}">Research archive on GitHub</a></span></div></footer></body></html>'''

def article(path):
    relative = path.relative_to(ROOT)
    text = path.read_text()
    title = text.splitlines()[0].lstrip('# ')
    depth = len(relative.parts) - 1
    prefix = '../' * depth
    historical = '<div class="note caution"><p>This is an earlier research note. Later findings may change its conclusions. Read the <a href="' + prefix + 'research/2026-11-04-origins-and-limits.html">current explanation of our earliest evidence</a> and the <a href="' + prefix + 'family-groups.html">updated family groups</a>.</p></div>' if relative.name.startswith('2026-10') else ''
    body = f'<article class="reading"><p class="breadcrumb"><a href="{prefix}index.html">← Back to the family home</a></p>{historical}{markdown(text)}<p class="source-link">Research record: <a href="{REPO}/blob/{REF}/{relative.as_posix()}">view this note on GitHub</a></p></article>'
    dest = OUT / relative.with_suffix('.html')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(shell(title, body, depth))

LINE = [
 ('Roy Bentley', '1930–1998 · Huddersfield', 'Married Margaret Cartwright, 1953', 1, 'Parent identification: birth index and family evidence', False),
 ('Thomas Herbert Bentley', '1888/9–1965 · Marsden', 'Married Lauretta Jones, 1920', 2, 'Parents named in the 1891 household', False),
 ('John Bentley', '1861–1918 · Marsden', 'Married Sarah Ann Haigh, 1883', 3, 'Parents named in the 1861 and 1871 households', False),
 ('Charles Bentley', 'Baptised 1828 · died 1897', 'Married Sarah Dyson, 1855', 5, 'William and Betty named in his baptism', False),
 ('William Bentley & Betty', 'Parents at Standage in 1828', 'Probably the couple married in 1815', 6, 'GAP: is this the William baptised in 1788?', True),
 ('William Bently, baptised 1788', 'Son of John and Ann', 'A probable match, not a confirmed identity', 7, 'His baptism names John and Ann', False),
 ('John Bentley & Ann Broadbent', 'John baptised 1750 · buried 1789', 'Married in 1771', 7, 'John’s baptism names James and Mary', False),
 ('James Bentley & Mary Nield', 'James baptised 1722', 'Married in 1745', 8, 'James’s baptism names Matthew and Sarah', False),
 ('Matthew Bentley & Sarah', 'Parents by 1722 · Matthew died 1751', 'Standedge / Knowl · clothier', 9, 'GAP: parentage and identity of “old Matthew”', True),
 ('Mathew Bentley & Ellin', 'Proposed Mathew baptised 1664', 'Probably “old Matthew”, buried 1735/6', 11, 'The 1664 baptism names Jonas; adult identity remains probable', True),
 ('Jonas Bentley', 'Children recorded 1654 and 1664', 'Administration and inventory, 1686', 11, 'GAP: no proven parent link to the earliest Mathew', True),
 ('Mathew Bentley', 'Children baptised 1613 and 1614', 'Earliest identified local Bentley; unlinked to Jonas', 11, 'Earliest record found, not proof of first arrival', True),
]

def home():
    groups_text = (ROOT / 'family-groups.md').read_text()
    sections = re.split(r'^## ', groups_text, flags=re.M)[1:]
    family_html = []
    for n, section in enumerate(sections, 1):
        title, content = section.split('\n', 1)
        group = 'haigh' if n == 4 else 'platt' if n == 10 else 'bentley'
        clean_title = re.sub(r'^\d+\. ', '', title)
        family_html.append(f'<details class="family" id="family-{n}" data-branch="{group}"><summary>{html.escape(clean_title)}</summary><div class="family-body">{markdown(content)}<a class="permalink" href="#family-{n}">Link to this family</a></div></details>')
    lineage = ''.join(f'<li class="{"gap" if gap else ""}"><a class="person" href="#family-{family}"><span>{date}</span><strong>{name}</strong><span>{spouse}</span></a><div class="relationship">{connection}</div></li>' for name,date,spouse,family,connection,gap in LINE)
    body = '''<div class="hero"><div><span class="eyebrow">Marsden · Standedge · Saddleworth</span><h1>A family story,<br>rooted in the Pennines.</h1><p class="lede">Meet the Bentleys and the families who joined them. Follow the generations, discover their lives, and see what the records really tell us.</p><div class="actions"><a class="button" href="#tree">Explore the family tree ↓</a><a class="button secondary" href="#families">Find a name</a></div></div>
<figure class="landscape"><svg viewBox="0 0 600 420" role="img" aria-label="Illustration of Pennine hills, a stone farmhouse and a winding path"><rect width="600" height="420" fill="#dbe4d5"/><circle cx="432" cy="85" r="38" fill="#f4edce"/><path d="M0 180 Q100 96 230 169 T600 129 V420 H0Z" fill="#aabcaa"/><path d="M0 260 Q134 154 280 218 T600 184 V420 H0Z" fill="#789780"/><path d="M0 320 Q160 210 354 282 T600 270 V420 H0Z" fill="#4c725c"/><path d="M310 420 Q245 364 330 330 T360 262" fill="none" stroke="#d9d7b6" stroke-width="15"/><path d="M0 365 L230 300 M420 318 L600 340 M130 275 L173 420" stroke="#b5c2a7" stroke-width="3" fill="none"/><path d="M275 240 L327 204 L379 240Z" fill="#344c42"/><path d="M285 238 H369 V292 H285Z" fill="#e4ddc3"/><path d="M305 255 H315 V269 H305Z M341 255 H351 V269 H341Z M324 271 H337 V292 H324Z" fill="#405d4e"/><path d="M347 210 V195 H357 V217" fill="#4d5e4d"/><path d="M0 393 Q140 354 230 400 T600 360" stroke="#244e3d" stroke-width="8" fill="none"/></svg><figcaption>Clothiers, households and a life among the hills.<small>Landscape illustration — not a reconstruction of a Bentley property.</small></figcaption></figure></div>
<div class="intro-strip"><div><b>1613</b><p>Earliest local Bentley entry identified. The connection to Roy is still incomplete.</p></div><div><b>11 family groups</b><p>Explore the direct line, siblings, spouses and wider branches.</p></div><div><b>Evidence first</b><p>Clear labels distinguish a record, a likely connection and a family claim.</p></div></div>
<section id="tree"><div class="section-head"><div><span class="eyebrow">Start with Roy, then step back</span><h2>The family tree</h2></div><p>Select any name to open their family group. Read down the page to travel back in time. The gaps matter as much as the names.</p></div><div class="tree-layout"><ol class="lineage">''' + lineage + '''</ol><aside class="aside"><div class="note"><h3>How far back can we go?</h3><p>Charles’s baptism names his parents William and Betty. Beyond them, identifying the right William is the first unresolved step.</p><p>The proposed earlier line reaches the 1600s, but it is not yet an unbroken pedigree.</p><a href="research/2026-11-04-origins-and-limits.html">Read the evidence and the limits →</a></div><div class="legend"><p><span class="tag">A record says it</span> A named relationship, sometimes read through a transcription.</p><p><span class="tag amber">A connection to test</span> The names fit, but the link is not proven.</p><p>Dashed amber lines mark unresolved steps. Earlier ancestors remain conditional on those steps.</p></div></aside></div></section>
<section id="families"><div class="section-head"><div><span class="eyebrow">People, partners and children</span><h2>Find your family</h2></div><p>Open a family to see the people and records. Search a name, place or year—for example “Lauretta”, “Platt” or “1828”.</p></div><div class="tools js-only"><label for="family-search">Search the family groups<input id="family-search" type="search" placeholder="Name, place or year…" autocomplete="off"></label><label for="branch">Branch<select id="branch"><option value="all">All branches</option><option value="bentley">Bentley and spouses</option><option value="haigh">Haigh parents</option><option value="platt">Platt descendants</option></select></label><button id="reset" class="secondary" type="button">Clear filters</button></div><div class="actions js-only"><button id="expand" class="secondary" type="button">Open all shown</button><button id="collapse" class="secondary" type="button">Close all</button><button class="secondary" type="button" data-print>Print this page</button></div><p id="result-count" class="small" role="status" aria-live="polite"></p><p class="small">In the records below: D = a documented record; S = a supported connection; F = a family claim still to check. “Baptised” does not necessarily mean “born”. <a href="family-groups.html">Read all groups as one page</a>.</p><p id="no-results" class="no-results" hidden>No matching family group. Try a surname, a shorter name, or clear the branch filter.</p>''' + '\n'.join(family_html) + '''</section>
<section id="stories"><div class="section-head"><div><span class="eyebrow">Beyond names and dates</span><h2>The lives behind the tree</h2></div><p>The records leave us stories, but also questions. Here is what we can reasonably say so far.</p></div><div class="story-grid"><article class="story"><span class="eyebrow">The earliest generations</span><h3>Was the first Bentley running from something?</h3><p>We do not know who first arrived or why. Two new legal-record leads name a Mathew Bentley in 1620 and a Mathewe in 1638/9. Neither is yet identified as an ancestor.</p><a href="research/2026-11-04-origins-and-limits.html#was-he-running-from-something">Read the records, without the guesswork →</a></article><article class="story"><span class="eyebrow">A place to make a living</span><h3>Why settle among the hills?</h3><p>Later Bentleys were clothiers. Hillside farms and packhorse routes supported a working textile economy. That gives us context, but not the earliest family’s personal motive.</p><a href="research/2026-11-04-origins-and-limits.html#why-live-in-that-landscape">Explore the landscape and livelihoods →</a></article><article class="story"><span class="eyebrow">A family across the world</span><h3>A lead in St Kilda</h3><p>A Victorian death-index transcription names Joseph Bentley’s parents as William and Betty. It supports an Australian connection, with his household still to establish.</p><a href="research/2026-11-04-wider-family.html#5-joseph-in-victoria">Follow the Australian evidence →</a></article><article class="story"><span class="eyebrow">A newly opened branch</span><h3>Helen and the Platts</h3><p>Helen Bentley’s family connects the Standedge group to Thomas Platt and a further generation at Wham and Ogden Edge. The sources preserve different spellings and one disputed date.</p><a href="#family-10">Meet Helen’s family →</a></article></div></section>
<section id="evidence"><span class="eyebrow">A family history you can check</span><h2>What we know. What we don’t.</h2><div class="evidence-list"><div><h3>Follow a source</h3><p>Each group points to research notes containing record references and public links. A transcription is labelled as such.</p><a href="research/2026-11-04-wider-family.html">Latest wider-family findings →</a></div><div><h3>Understand the gaps</h3><p>Missing pages, similar names and conflicting dates can break a chain. We keep those uncertainties visible.</p><a href="research/2026-11-04-origins-and-limits.html">Why we cannot yet go further →</a></div><div><h3>Bring a family clue</h3><p>An old photograph, certificate or remembered place can help. Share it privately with the family researcher, with names and dates if known. Keep living people’s details off this public site.</p><a href="research-plan.html">See the questions we are working on →</a></div></div></section>'''
    body = body.replace('<p id="no-results"', '<p class="small">Source keys: <a href="research/2026-10-10-line-from-records.html">R — recent generations</a>; <a href="research/2026-10-10-saddleworth-line.html">SAD — Saddleworth records</a>; <a href="research/2026-11-04-charles-william-review.html">CW — Charles and William</a>; <a href="research/2026-11-04-wider-family.html">NEW — wider-family findings</a>.</p><p id="no-results"')
    (OUT / 'index.html').write_text(shell('Our family', body))

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

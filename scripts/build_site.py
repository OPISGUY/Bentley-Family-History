#!/usr/bin/env python3
"""Build the family website using Python's standard library. No network or packages."""
from tree_view import tree
from map_atlas import render_map_atlas
import hashlib
import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
REPO = 'https://github.com/OPISGUY/Bentley-Family-History'
REF = 'ccr-469e384c-x98nc5'

STORY_TREE_LINKS = {
    'mathew-and-his-daughter-an': ('gen-11', 'family-11', 'Mathew Bentley (1613–14)'),
    'the-road-to-york-castle': ('gen-11', 'family-11', '17th-Century Saddleworth Bentleys'),
    'jonas-and-the-two-matthews': ('gen-10', 'family-11', 'Jonas Bentley of Standedge (d. 1686)'),
    'the-carpenter-of-diggle-and-the-summer-wedding': ('gen-10', 'family-11', 'Diggle & Standedge Bentleys (1654–1764)'),
    'old-matthew-of-stone-edge': ('gen-9', 'family-11', 'Mathew (“old Matthew”) of Stone-edge'),
    'matthew-and-sarah-in-the-cloth-country': ('gen-8', 'family-9', 'Matthew & Sarah Bentley of Standedge'),
    'james-and-mary-marry-at-christmas': ('gen-7', 'family-8', 'James Bentley & Mary Nield'),
    'helen-and-the-stone-at-st-chads': ('gen-8', 'family-10', 'Helen Bentley & Thomas Platt'),
    'hannah-and-the-journey-to-liverpool': ('gen-8', 'family-10', 'Platt & Gartside Branch'),
    'john-and-ann-give-a-name-again': ('gen-6', 'family-7', 'John Bentley & Ann Broadbent'),
    'bentleys-at-standedge-foot': ('gen-6', 'family-7', 'Standedge Foot, Bleak Hey Nook & Woodmans'),
    'two-brothers-at-the-font': ('gen-5', 'family-6', 'William & Betty and James & Ann at Standage'),
    'betty-and-the-four-weavers-at-carr-clough': ('gen-5', 'family-6', 'William & Betty Bentley’s Household'),
    'three-houses-on-carlisle-street': ('gen-5', 'family-12', 'St Kilda Brothers (Carlisle Street)'),
    'ann-at-carr-clough': ('gen-4', 'family-5', 'Ann & Charles Bentley at Carr Clough'),
    'charles-leaves-weaving-for-stone': ('gen-4', 'family-5', 'Charles Bentley & Sarah Dyson'),
    'john-the-piecer-becomes-a-weaver': ('gen-3', 'family-3', 'John Bentley & Sarah Ann Haigh'),
    'thomas-herbert-and-lauretta-in-the-local-paper': ('gen-2', 'family-2', 'Thomas Herbert Bentley & Lauretta Jones'),
    'roy-and-margaret-in-postwar-yorkshire': ('gen-1', 'family-1', 'Roy Bentley & Margaret Cartwright'),
    'the-road-below-the-reservoir': ('gen-2', 'family-2', 'Three Generations at Binn Road'),
}

FAMILY_SUBTITLES = {
    1: 'Huddersfield & Slaithwaite · 1920–1998',
    2: 'Binn Road, Marsden & Huddersfield · 1885–1965',
    3: 'Carr Clough & Binn, Marsden · 1857–1934',
    4: 'Marsden Memorial & Census Branch · 1820–1934',
    5: 'Standage, Carr Clough & Binn · 1828–1897',
    6: 'Standage, Coat Hill, Ridge & Carr Clough · 1782–1851',
    7: 'Barn, Standedge & Meerleech · 1750–1789',
    8: 'Deanhead, Barn & Stone-edge · 1722–1790',
    9: 'Deanhead, Knowl, Knar & Stone-edge · c.1692–1751',
    10: 'Standedge, Heyhouse, Wham & Ogden · 1733/4–1833',
    11: 'St Chad’s, Standedge, Diggle & Trans-Pennine Corridors · 1613–1850',
    12: 'Point Nepean & 66 Carlisle Street, St Kilda · 1854–1861',
    13: '“Baroona”, 66 Carlisle Street, St Kilda · 1865–1954',
    14: '62 Carlisle Street, St Kilda · 1858–1950',
}

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
<meta name="description" content="Explore the Bentley family of Saddleworth, Standedge, Marsden and St Kilda: human stories, 11 generations of family groups, and the archival evidence behind every link.">
<title>{html.escape(title)} · Bentley Family History</title><link rel="stylesheet" href="{prefix}style.css"><script defer src="{prefix}app.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap"><a class="brand" href="{prefix}index.html">Bentley family history</a>
<nav aria-label="Main navigation"><a href="{prefix}index.html#tree">Tree</a><a href="{prefix}index.html#atlas-map">Map</a><a href="{prefix}bentley-lives.html">Stories</a><a href="{prefix}index.html#families">Households</a><a href="{prefix}index.html#evidence">Records</a></nav></div></header>
<main id="main" class="wrap">{body}</main><footer><div class="wrap"><div><strong>The Bentley Family Chronicle (1613–1998)</strong><br><span>Rebuilt from parish registers, probate inventories, manor rolls, maps and newspapers. Free to explore, with no account required.<br>Living generations are kept private. Research and stories updated 11 November 2026.</span></div><div><a href="{prefix}bentley-lives.html">Read all 20 family stories</a> · <a href="{prefix}family-tree.html">Full chart &amp; status guide</a><br><a href="{prefix}earlier-research-plan.html">Research checklist</a> · <a href="{REPO}">Source archive on GitHub</a></div></div></footer></body></html>'''

def article(path):
    relative = path.relative_to(ROOT)
    text = path.read_text()
    title = text.splitlines()[0].lstrip('# ')
    depth = len(relative.parts) - 1
    prefix = '../' * depth
    historical = '<div class="note caution"><p><strong>Historical research note:</strong> This is an earlier dated working note preserved for audit trail. Later findings refine several conclusions here—see the <a href="' + prefix + 'research/2026-11-11-standedge-to-1600s-and-beyond.html">11 November Standedge-to-1600s review</a>, the <a href="' + prefix + 'research/2026-11-10-binn-and-carlisle-street.html">10 November Binn &amp; Carlisle Street review</a>, and the <a href="' + prefix + 'family-groups.html">updated family groups</a>.</p></div>' if relative.name.startswith('2026-10') else ''
    body = f'<article class="reading"><p class="breadcrumb"><a href="{prefix}index.html">← Back to the family chronicle</a> · <a href="{prefix}bentley-lives.html">Family stories</a></p>{historical}{markdown(text)}<p class="source-link">Archival markdown source: <a href="{REPO}/blob/{REF}/{relative.as_posix()}">view this document on GitHub</a></p></article>'
    if relative.name == 'family-tree.md':
        body = body.replace(markdown(text), '<p><a class="button" href="index.html#tree">Explore the interactive tree with human portraits &amp; siblings →</a></p>' + markdown(text))
    dest = OUT / relative.with_suffix('.html')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(shell(title, body, depth))

def first_sentence(prose):
    clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', prose.split('\n\n')[0]).replace('*', '')
    m = re.match(r'^(.+?[.!?])(?:\s|$)', clean.strip())
    return m.group(1) if m else clean[:160]

def publish_stories():
    sources = (ROOT / 'bentley-lives.md').read_text()
    chapters = re.findall(r'^## (.+)$', sources, re.M)
    order = [slug(title) for title in chapters[:-1]]
    extra_insertions = [
        ('the-road-to-york-castle', 'mathew-and-his-daughter-an', 'mathew-and-his-daughter-an'),
        ('the-carpenter-of-diggle-and-the-summer-wedding', 'jonas-and-the-two-matthews', 'jonas-and-the-two-matthews'),
        ('old-matthew-of-stone-edge', 'the-carpenter-of-diggle-and-the-summer-wedding', 'jonas-and-the-two-matthews'),
        ('bentleys-at-standedge-foot', 'john-and-ann-give-a-name-again', 'john-and-ann-give-a-name-again'),
        ('two-brothers-at-the-font', 'bentleys-at-standedge-foot', 'john-and-ann-give-a-name-again'),
        ('ann-at-carr-clough', 'three-houses-on-carlisle-street', 'three-houses-on-carlisle-street'),
    ]
    extra_sources = {}
    for key, after_key, source_anchor in extra_insertions:
        order.insert(order.index(after_key) + 1, key)
        extra_sources[key] = source_anchor
    stories = []
    for key in order:
        title, setting, prose = (ROOT / 'stories' / f'{key}.md').read_text().strip().split('\n\n', 2)
        stories.append((key, title.removeprefix('# '), setting, prose))
    (OUT / 'stories').mkdir(exist_ok=True)
    total = len(stories)
    for i, (key, title, setting, prose) in enumerate(stories):
        source = extra_sources.get(key, key)
        gen_id, fam_id, fam_label = STORY_TREE_LINKS.get(key, ('gen-4', 'family-5', 'Bentley Family Household'))
        prev_html = ''
        if i > 0:
            prev_key, prev_title, *_ = stories[i - 1]
            prev_html = f'<a class="nav-card prev" href="{prev_key}.html"><small>← Previous chapter ({i} of {total})</small><strong>{html.escape(prev_title)}</strong></a>'
        else:
            prev_html = '<a class="nav-card prev" href="../bentley-lives.html"><small>← Table of contents</small><strong>All 20 Family Stories</strong></a>'
        if i + 1 < total:
            next_key, next_title, *_ = stories[i + 1]
            next_html = f'<a class="nav-card next" href="{next_key}.html"><small>Next chapter ({i+2} of {total}) →</small><strong>{html.escape(next_title)}</strong></a>'
        else:
            next_html = '<a class="nav-card next" href="../bentley-lives.html"><small>Completed all chapters →</small><strong>Back to the Story Book</strong></a>'
        body = f'''<article class="reading life">
<div class="story-topbar"><a href="../bentley-lives.html">← All 20 family stories</a><span>Chapter {i+1} of {total}</span></div>
<header class="life-header"><p class="dateline">{html.escape(setting)}</p><h1>{html.escape(title)}</h1></header>
<div class="life-prose">{markdown(prose)}</div>
<aside class="story-connections" aria-label="Where this story fits in the family history">
<h3>Where this chapter fits in the family</h3>
<div class="conn-grid">
<a href="../index.html#{gen_id}"><small>Interactive Family Tree</small><strong>View generation &amp; human portrait →</strong></a>
<a href="../index.html#{fam_id}"><small>Household Directory</small><strong>{html.escape(fam_label)} →</strong></a>
<a href="../life-sources.html#{source}"><small>Primary Sources &amp; Citations</small><strong>Verify the original records →</strong></a>
</div>
</aside>
<nav class="story-pager" aria-label="Chapter navigation">{prev_html}{next_html}</nav>
</article>'''
        (OUT / 'stories' / f'{key}.html').write_text(shell(title, body, 1))
    shelf_items = []
    for idx, (key, title, setting, prose) in enumerate(stories, 1):
        teaser = first_sentence(prose)
        shelf_items.append(
            f'<li id="{key}"><a href="stories/{key}.html">'
            f'<span class="chap-num">Chapter {idx}</span>'
            f'<strong>{html.escape(title)}</strong>'
            f'<span class="chap-setting">{html.escape(setting)}</span>'
            f'<span class="chap-teaser">{html.escape(teaser)}</span>'
            f'</a></li>'
        )
    shelf = ''.join(shelf_items)
    body = (
        '<article class="reading story-index-page">'
        '<p class="eyebrow">Twenty Chapters Across Four Centuries · 1613–1998</p>'
        '<h1>The Lives of the Bentleys</h1>'
        '<p class="lede">Commercial genealogy sites turn people into isolated dates on a chart. Here, twenty chronological chapters follow the Bentleys from a May 1613 christening at St Chad’s, Saddleworth and a 1686 inventory on the high ridge of Standedge to the woollen mills and stone quarries of Marsden and three brothers’ houses on Carlisle Street in St Kilda.</p>'
        '<p><a class="button" href="stories/mathew-and-his-daughter-an.html">Start at Chapter 1 (Saddleworth, 1613) →</a> <a class="button secondary" href="life-sources.html">Inspect all source notes →</a></p>'
        '<ol class="bookshelf">' + shelf + '</ol>'
        '<div class="note"><h3 id="audit-note">Newspapers, memorials &amp; military checks</h3>'
        '<p id="' + slug(chapters[-1]) + '">Every story is bound to a companion source note stating exactly what the record proves and what remains open. Read <a href="life-sources.html#' + slug(chapters[-1]) + '">Where the military and newspaper searches led →</a></p></div>'
        '</article>'
    )
    (OUT / 'bentley-lives.html').write_text(shell('Family stories', body))
    (OUT / 'life-sources.html').write_text(shell('Records behind the stories', '<article class="reading"><p class="breadcrumb"><a href="bentley-lives.html">← Back to the 20 family stories</a> · <a href="index.html">Home</a></p>'+markdown(sources.replace('# The lives of the Bentleys', '# Records behind the stories', 1))+'</article>'))
    return shelf

def home(shelf):
    groups_text = (ROOT / 'family-groups.md').read_text()
    sections = re.split(r'^## ', groups_text, flags=re.M)[1:]
    family_html = []
    for n, section in enumerate(sections, 1):
        title, content = section.split('\n', 1)
        group = 'haigh' if n == 4 else 'platt' if n == 10 else 'australia' if n in (12, 13, 14) else 'marsden' if n in (1, 2, 3, 5) else 'saddleworth'
        clean_title = re.sub(r'^\d+\. ', '', title)
        sub = FAMILY_SUBTITLES.get(n, '')
        sub_html = f'<span class="fam-sub">{html.escape(sub)}</span>' if sub else ''
        family_html.append(f'<details class="family" id="family-{n}" data-branch="{group}"><summary><span class="fam-title">{html.escape(clean_title)}</span>{sub_html}</summary><div class="family-body">{markdown(content)}<a class="permalink" href="#family-{n}">Direct link to this household</a></div></details>')

    hero = (ROOT / 'site' / 'welcome.html').read_text()
    body = hero + render_map_atlas() + tree(sections)
    body += '''<section id="stories"><div class="section-head"><div><p class="eyebrow">Twenty Chronological Chapters · 1613 to 1998</p><h2>The Family Stories</h2></div><p>Read the family history as a continuous narrative of real people, places and trades—from the first surviving parish entry in 1613 to living memory in Huddersfield and Marsden.</p></div><ol class="bookshelf">''' + re.sub(r' id="[^"]+"', '', shelf) + '</ol></section>'
    body += """<section id="families"><div class="section-head"><div><p class="eyebrow">Fourteen Populated Households</p><h2>Family &amp; Household Directory</h2></div><p>Search by given name, surname, farm or hamlet (such as <em>Standedge</em>, <em>Diggle</em>, <em>Binn</em>, <em>Carlisle Street</em>, <em>Haigh</em> or <em>Platt</em>), or filter by branch to inspect every child, baptism, census line and source citation.</p></div><div class="tools js-only"><label>Search people, places, trades or years<input id="family-search" type="search" placeholder="e.g. Standedge, Binn, Carlisle Street, Ellin, Wright, 1714..."></label><label>Branch or region<select id="branch"><option value="all">All 14 households</option><option value="marsden">Marsden &amp; Huddersfield (Groups 1–3, 5)</option><option value="saddleworth">Standedge &amp; Saddleworth (Groups 6–9, 11)</option><option value="australia">St Kilda, Australia (Groups 12–14)</option><option value="haigh">Haigh branch (Group 4)</option><option value="platt">Platt branch (Group 10)</option></select></label><button id="reset" class="secondary">Reset</button></div><div class="quick-chips js-only" aria-label="Quick search filters"><span>Quick filters:</span><button type="button" class="chip" data-chip="Standedge">Standedge</button><button type="button" class="chip" data-chip="Binn">Binn &amp; Marsden</button><button type="button" class="chip" data-chip="Carlisle Street">Carlisle Street, St Kilda</button><button type="button" class="chip" data-chip="Diggle">Diggle &amp; Fairbanks</button><button type="button" class="chip" data-chip="Woodmans">Woodmans &amp; Rhodes</button><button type="button" class="chip" data-chip="1819">6 June 1819 Baptism</button></div><div class="actions js-only"><button id="expand" class="secondary">Open all shown</button><button id="collapse" class="secondary">Collapse all</button><button data-print class="secondary">Print directory</button></div><p id="result-count" role="status"></p><p id="no-results" class="no-results" hidden>No matching household found. Try another name, farm, or click Reset.</p><p class="small"><strong>Evidence key:</strong> <code>D</code> = Documented in contemporary record &nbsp;·&nbsp; <code>Probable</code> = Strong multi-point correlation &nbsp;·&nbsp; <code>S</code> = Supported identification &nbsp;·&nbsp; <code>F</code> = Family recollection</p>""" + ''.join(family_html) + '</section>'
    body += """<section id="evidence"><div class="section-head"><div><p class="eyebrow">Key Archival Breakthroughs &amp; Primary Sources</p><h2>How the Records Connect the Line</h2></div><p>Every generation is tested against free parish, civil, census, probate, manorial, map and newspaper records, keeping proven facts distinct from working hypotheses.</p></div>
<div class="evidence-list">
<article class="story"><span class="tag amber">1482–1686 · The 1613 Horizon &amp; 3-Point Link to Jonas</span><h3>Why Mathew didn’t come from thin air</h3><p>St Chad’s registers before 1632 are lost save for three loose sheets (<strong>1612–1614</strong>) after a 67-year blackout since 1545. Born in the 1580s when Elizabethan families first adopted biblical names like <em>Mathew</em> and <em>Jonas</em>, Mathew of 1613–14 links forward to <strong>Jonas of Standedge (d. 1686)</strong> through three facts: the <strong>1615–31 Bishop’s Transcript gap</strong> matches Jonas’s birth window; Mathew and Jonas are the <strong>only two Bentley fathers in Saddleworth across 73 years (1613–86)</strong>; and Jonas named his next son <strong>Mathew</strong> in 1664 after <strong>“Mathey” Bentley</strong> was buried in February 1657/8.</p><p><a href="stories/mathew-and-his-daughter-an.html">Read Mathew &amp; An’s story →</a><br><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html#5-connecting-the-bentley-lines-how-mathew-1613-and-jonas-1654-link-inside-saddleworth-how-the-unplaced-saddleworth-households-connect-and-the-trans-pennine-corridors-across-rochdale-bury-oldham-and-calderdale">Read the 1482–1850 connection audit →</a></p></article>
<article class="story"><span class="tag">1686–1764 · Standedge &amp; Diggle Probate</span><h3>Jonas at Standedge (1686), Old Matthew &amp; the Diggle Carpenter</h3><p>The Leonard Kidd probate abstract (<code>H/KID</code>, p. 248) of <strong>Jonas Bentley’s 18 August 1686 inventory</strong> explicitly places him <strong>“of Standedge, Saddleworth”</strong>—40 years earlier than the parish registers—while a four-point correlation (<em>Ellin</em>, <em>John</em>, <em>Esther</em>, and <em>Matthew</em> born after old Matthew’s 1735/6 burial) connects “old Matthew” to Matthew of Standedge (d. 1751). Down the slope in <strong>Diggle</strong>, carpenter <strong>John Bentley’s</strong> February 1713/14 inventory was followed in July 1714 by <strong>Mary Bentley’s</strong> licence marriage to <strong>James Bradbury of Fairbanks, Diggle</strong>.</p><p><a href="stories/the-carpenter-of-diggle-and-the-summer-wedding.html">Read the Diggle carpenter’s story →</a><br><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html#1-jonas-bentley-at-standedge-in-1686-and-the-four-point-correlation-to-matthew-of-standedge-d-1751">Read the 1686–1751 probate evidence →</a></p></article>
<article class="story"><span class="tag">26 Nov 1791 &amp; 1822 · Standedge Foot &amp; Woodmans</span><h3>Where was “Bentleys” — and who shared Woodmans?</h3><p>The <strong>1822 Map of Saddleworth</strong> marks <strong>“BENTLEYS”</strong> next to <strong>“STANEDGE FOOT”</strong> on the turnpike road (where co-owner <strong>John Bentley of Bentleys</strong> lived on 26 November 1791), distinct from <strong>Bleak Hey Nook</strong> (where co-owner <strong>James Bentley</strong> lived). On that exact same day in November 1791, the two-dwelling farmhouse called <strong>Woodmans</strong> was occupied jointly by <strong>Matthew Bentley</strong> (the 1738/9 uncle) and <strong>Thomas Rhodes</strong> (father of niece Esther Bentley’s 1779 child).</p><p><a href="stories/bentleys-at-standedge-foot.html">Read the “Bentleys” &amp; Woodmans story →</a><br><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html#3-resolving-the-bentleys-tenement-17911822-and-the-6-june-1819-double-baptism-at-st-chads">See the 1822 map, deeds &amp; auction notice →</a></p></article>
<article class="story"><span class="tag amber">6 June 1819 · St Chad’s, Saddleworth</span><h3>Two brothers side by side at the font</h3><p>On Sunday, <strong>6 June 1819</strong>, <strong>William and Betty Bentley of Standage, clothier</strong>, and <strong>James and Ann Bentley of Standage, clothier</strong>, stood at St Chad’s on the same day to baptise their sons <strong>William</strong> and <strong>Charles</strong>—matching the names, hamlet and trade of the surviving brothers baptised in 1788 and 1784 to John and Ann Bentley, and introducing the name <strong>Charles</strong> given to our ancestor in 1828.</p><p><a href="stories/two-brothers-at-the-font.html">Read the 6 June 1819 story →</a><br><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html#32-the-6-june-1819-double-baptism-at-st-chads-connecting-william-bap-1788-and-james-bap-1784-at-standage">Inspect the 1819 baptism evidence →</a></p></article>
<article class="story"><span class="tag">1861–1913 · Carr Clough &amp; Binn, Marsden</span><h3>Stone delvers, child piecers &amp; the drowned mill</h3><p>An <strong>1881 census profile of Binn</strong> counts 18 households and 78 residents, naming both <strong>Bentley</strong> and <strong>Haigh</strong>, while local histories show that <strong>Upper Bank Bottom Mill</strong> (“Th’ Top Bonk”) was demolished in <strong>1891</strong> to build Butterley Reservoir over its site, leaving Lower Bank Bottom Mill and the Crowthers’ five-storey mill at Ottiwells below Binn Road.</p><p><a href="stories/charles-leaves-weaving-for-stone.html">Read the Marsden story →</a><br><a href="research/2026-11-10-binn-and-carlisle-street.html#3-binn-in-1881-and-the-mills-below-binn-road">Read the Binn &amp; mill records →</a></p></article>
<article class="story"><span class="tag">1891–1950 · St Kilda, Victoria</span><h3>Three houses on Carlisle Street</h3><p>Melbourne newspaper notices in Trove place Charles’s three emigrated brothers along the same street in St Kilda: <strong>William and Hannah</strong> at <strong>62 Carlisle Street</strong>, <strong>Wright and Helen</strong> at <strong>“Stockwell”, Carlisle Street</strong>, and <strong>Joseph and Ann</strong> at <strong>“Baroona”, 66 Carlisle Street</strong>, proving that Joseph’s two families (with Irvine Nisbett and Ann Jones) had the same father.</p><p><a href="stories/three-houses-on-carlisle-street.html">Read the Carlisle Street story →</a><br><a href="research/2026-11-10-binn-and-carlisle-street.html#1-three-bentley-households-on-carlisle-street-st-kilda">See the Trove notices →</a></p></article>
</div>
<div class="archive-shelf"><p><strong>Dated Research Dossiers:</strong> <a href="research/2026-11-11-standedge-to-1600s-and-beyond.html">11 Nov: Standedge to the 1600s &amp; Line Connections</a> · <a href="research/2026-11-10-binn-and-carlisle-street.html">10 Nov: Binn, Marsden &amp; Carlisle Street</a> · <a href="research/2026-11-05-earlier-line-search.html">5 Nov: Earlier Line Search</a> · <a href="research/2026-11-05-standedge-households.html">5 Nov: Standedge Households</a> · <a href="research/2026-11-05-australian-households.html">5 Nov: Australian Households</a> · <a href="research/2026-11-04-origins-and-limits.html">4 Nov: Origins &amp; York Castle</a> · <a href="research/2026-11-04-wider-family.html">4 Nov: Wider Family</a> · <a href="earlier-research-plan.html">Full Research Checklist</a></p></div></section>"""
    page = shell('Our family chronicle', body)
    for asset in ('style.css', 'app.js'):
        version = hashlib.sha256((OUT / asset).read_bytes()).hexdigest()[:10]
        page = page.replace(f'"{asset}"', f'"{asset}?v={version}"')
    (OUT / 'index.html').write_text(page)

def build():
    OUT.mkdir(exist_ok=True)
    for asset in ('style.css', 'app.js', 'butterley.jpg'):
        if (ROOT / 'site' / asset).exists():
            shutil.copyfile(ROOT / 'site' / asset, OUT / asset)
    shutil.copytree(ROOT / 'site' / 'album', OUT / 'album', dirs_exist_ok=True)
    (OUT / '.nojekyll').write_text('')
    for path in sorted(ROOT.glob('*.md')) + sorted((ROOT / 'research').glob('*.md')):
        article(path)
    home(publish_stories())
    print(f'Built {len(list(OUT.rglob("*.html")))} pages in docs/')

if __name__ == '__main__':
    build()

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
<main id="main" class="wrap">{body}</main><footer><div class="wrap"><span>Made for the family. Free to explore. No account needed.<br>Living generations are kept private. Research updated 11 November 2026.</span><span><a href="{prefix}research-plan.html">What we’re researching next</a><br><a href="{REPO}">Research archive on GitHub</a></span></div></footer></body></html>'''

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

def publish_stories():
    sources = (ROOT / 'bentley-lives.md').read_text()
    chapters = re.findall(r'^## (.+)$', sources, re.M)
    order = [slug(title) for title in chapters[:-1]]
    extra = {'the-road-to-york-castle': order[0], 'old-matthew-of-stone-edge': order[1], 'ann-at-carr-clough': order[7]}
    for key, source in extra.items():
        order.insert(order.index(source) + 1, key)
    stories = []
    for key in order:
        title, setting, prose = (ROOT / 'stories' / f'{key}.md').read_text().strip().split('\n\n', 2)
        stories.append((key, title.removeprefix('# '), setting, prose))
    (OUT / 'stories').mkdir(exist_ok=True)
    for i, (key, title, setting, prose) in enumerate(stories):
        source = extra.get(key, key)
        next_link = '<a href="../bentley-lives.html">Back to all stories</a>'
        if i + 1 < len(stories):
            next_key, next_title, *_ = stories[i+1]
            next_link = f'<a href="{next_key}.html">Next story: {html.escape(next_title)} →</a>'
        body = f'<article class="reading life"><a href="../bentley-lives.html">← Family stories</a><p class="dateline">{html.escape(setting)}</p><h1>{html.escape(title)}</h1>{markdown(prose)}<details class="records"><summary>Records behind this story</summary><p><a href="../life-sources.html#{source}">Read the evidence and original references</a></p></details><p class="next-life">{next_link}</p></article>'
        (OUT / 'stories' / f'{key}.html').write_text(shell(title, body, 1))
    shelf = ''.join(f'<li id="{key}"><a href="stories/{key}.html"><strong>{html.escape(title)}</strong><span>{html.escape(setting)}</span></a></li>' for key,title,setting,_ in stories)
    body = '<article class="reading"><h1>Family stories</h1><p>From a baptism in Saddleworth to a wedding in postwar Yorkshire.</p><ol class="bookshelf">' + shelf + '</ol><p id="' + slug(chapters[-1]) + '"><a href="life-sources.html#' + slug(chapters[-1]) + '">Newspapers and military searches</a></p></article>'
    (OUT / 'bentley-lives.html').write_text(shell('Family stories', body))
    (OUT / 'life-sources.html').write_text(shell('Records behind the stories', '<article class="reading"><a href="bentley-lives.html">← Family stories</a>'+markdown(sources.replace('# The lives of the Bentleys', '# Records behind the stories', 1))+'</article>'))
    return shelf

def home(shelf):
    groups_text = (ROOT / 'family-groups.md').read_text()
    sections = re.split(r'^## ', groups_text, flags=re.M)[1:]
    family_html = []
    for n, section in enumerate(sections, 1):
        title, content = section.split('\n', 1)
        group = 'haigh' if n == 4 else 'platt' if n == 10 else 'bentley'
        clean_title = re.sub(r'^\d+\. ', '', title)
        family_html.append(f'<details class="family" id="family-{n}" data-branch="{group}"><summary>{html.escape(clean_title)}</summary><div class="family-body">{markdown(content)}<a class="permalink" href="#family-{n}">Link to this family</a></div></details>')
    body = (ROOT / 'site' / 'welcome.html').read_text() + tree(sections)
    body += """<section id="families"><h2>Family directory</h2><p>Look up a name, place or year to see the household and its records.</p><div class="tools js-only"><label>Find a person<input id="family-search" type="search" placeholder="Name, place or year"></label><label>Family<select id="branch"><option value="all">All families</option><option value="bentley">Bentley and spouses</option><option value="haigh">Haigh</option><option value="platt">Platt</option></select></label><button id="reset" class="secondary">Clear</button></div><div class="actions js-only"><button id="expand" class="secondary">Open results</button><button id="collapse" class="secondary">Close results</button><button data-print class="secondary">Print</button></div><p id="result-count" role="status"></p><p id="no-results" hidden>No matching household. Try a surname or clear the filters.</p><p class="small">D = documented record · S = supported identification · F = family account</p>""" + ''.join(family_html) + '</section>'
    body += '<section id="stories"><h2>Family stories</h2><ol class="bookshelf">' + re.sub(r' id="[^"]+"','',shelf) + '</ol></section>'
    body += """<section id="evidence"><div class="section-head"><div><p class="eyebrow">Key findings &amp; primary sources</p><h2>What the records now show</h2></div><p>Every generation is tested against free parish, civil, census, probate, map and newspaper records, keeping proven facts distinct from working hypotheses.</p></div>
<div class="evidence-list">
<article class="story"><span class="tag amber">1379–1658 · The 1400s–1600s Boundary &amp; York Castle</span><h3>From the Tudor border to York Castle</h3><p>No Bentley appears in 14th–16th century Saddleworth tax or muster rolls, and neither <em>Mathew</em> nor <em>Jonas</em> occurs among the Bentleys in the 1538–1593 Halifax registers—separating our line from High Bentley Hall while pointing to the Rochdale/Pennine border. After a Mathew Bentley of Saddleworth was gravely wounded by Henry Platte in 1619–20, the Quarter Sessions in January 1638/9 ordered <strong>Mathewe Bentley, late of Saddleworth, labourer</strong>, committed to <strong>York Castle</strong>—three years before the 1641/2 Protestation found no adult Bentley left in the chapelry.</p><p><a href="stories/the-road-to-york-castle.html">Read the York Castle story →</a><br><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html#43-pushing-back-to-the-1500s-and-1400s-a-border-wide-audit-across-saddleworth-rochdalespotland-and-the-west-riding-13791680">See the 1400s–1600s audit →</a></p></article>
<article class="story"><span class="tag">1686–1751 · Standedge</span><h3>Jonas at Standedge in 1686 &amp; the 4-point link</h3><p>The Leonard Kidd probate abstract (<code>H/KID</code>, p. 248) of <strong>Jonas Bentley’s 18 August 1686 inventory</strong> explicitly places him <strong>“of Standedge, Saddleworth”</strong>—40 years earlier than the parish registers first name the farm—while a four-point residence and child-naming correlation (<em>Ellin</em>, <em>John</em>, <em>Esther</em>, and <em>Matthew</em> born after old Matthew’s 1735/6 burial) connects “old Matthew” to Matthew of Standedge (d. 1751).</p><p><a href="stories/old-matthew-of-stone-edge.html">Read Old Matthew’s story →</a><br><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html#1-jonas-bentley-at-standedge-in-1686-and-the-four-point-correlation-to-matthew-of-standedge-d-1751">Read the 1686–1751 evidence →</a></p></article>
<article class="story"><span class="tag">1791–1822 · Standedge Foot, Bleak Hey Nook &amp; Woodmans</span><h3>Where was “Bentleys” — and who held Woodmans?</h3><p>The <strong>1822 Map of Saddleworth</strong> marks <strong>“BENTLEYS”</strong> next to <strong>“STANEDGE FOOT”</strong> on the turnpike road (where co-owner <strong>John Bentley of Bentleys</strong> lived in 1791), distinct from <strong>Bleak Hey Nook</strong> (where co-owner <strong>James Bentley</strong> lived). Meanwhile, a <strong>19 April 1791</strong> sale notice for <strong>Woodmans</strong> shows <strong>Matthew Bentley</strong> (matching the 1738/9 uncle) and <strong>Thomas Rhodes</strong> (father of niece Esther’s 1779 son) sharing its two dwellings.</p><p><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html#3-resolving-the-bentleys-tenement-17911822-and-the-6-june-1819-double-baptism-at-st-chads">See the 1822 map, deeds &amp; Woodmans notice →</a></p></article>
<article class="story"><span class="tag amber">6 June 1819 · St Chad’s, Saddleworth</span><h3>Two brothers at the font</h3><p>On Sunday, <strong>6 June 1819</strong>, <strong>William and Betty Bentley of Standage, clothier</strong>, and <strong>James and Ann Bentley of Standage, clothier</strong>, stood at St Chad’s on the same day to baptise their sons <strong>William</strong> and <strong>Charles</strong>—matching the names, hamlet and trade of the surviving brothers baptised in 1788 and 1784 to John and Ann Bentley, and introducing the name <strong>Charles</strong> given to our ancestor in 1828.</p><p><a href="stories/john-and-ann-give-a-name-again.html">Read the story →</a><br><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html#32-the-6-june-1819-double-baptism-at-st-chads-connecting-william-bap-1788-and-james-bap-1784-at-standage">Inspect the 1819 baptism evidence →</a></p></article>
<article class="story"><span class="tag">1861–1913 · Carr Clough &amp; Binn, Marsden</span><h3>The mills below Binn Road</h3><p>An <strong>1881 census profile of Binn</strong> counts 18 households and 78 residents, naming both <strong>Bentley</strong> and <strong>Haigh</strong>, while local histories show that <strong>Upper Bank Bottom Mill</strong> (“Th’ Top Bonk”) was demolished in <strong>1891</strong> to build Butterley Reservoir over its site, leaving Lower Bank Bottom Mill and the Crowthers’ five-storey mill at Ottiwells below Binn Road.</p><p><a href="stories/charles-leaves-weaving-for-stone.html">Read the Marsden story →</a><br><a href="research/2026-11-10-binn-and-carlisle-street.html#3-binn-in-1881-and-the-mills-below-binn-road">Read the Binn &amp; mill records →</a></p></article>
<article class="story"><span class="tag">1891–1950 · St Kilda, Victoria</span><h3>Three houses on Carlisle Street</h3><p>Melbourne newspaper notices in Trove place Charles’s three emigrated brothers along the same street in St Kilda: <strong>William and Hannah</strong> at <strong>62 Carlisle Street</strong>, <strong>Wright and Helen</strong> at <strong>“Stockwell”, Carlisle Street</strong>, and <strong>Joseph and Ann</strong> at <strong>“Baroona”, 66 Carlisle Street</strong>, proving that Joseph’s two families (with Irvine Nisbett and Ann Jones) had the same father.</p><p><a href="stories/three-houses-on-carlisle-street.html">Read the Carlisle Street story →</a><br><a href="research/2026-11-10-binn-and-carlisle-street.html#1-three-bentley-households-on-carlisle-street-st-kilda">See the Trove notices →</a></p></article>
</div>
<p style="margin-top:28px"><a href="research/2026-11-11-standedge-to-1600s-and-beyond.html">11 Nov: Standedge to the 1600s</a> · <a href="research/2026-11-10-binn-and-carlisle-street.html">10 Nov: Binn &amp; Carlisle Street</a> · <a href="research/2026-11-04-origins-and-limits.html">4 Nov: Origins, York Castle &amp; limits</a> · <a href="research/2026-11-05-earlier-line-search.html">5 Nov: Earlier Bentley search</a> · <a href="research-plan.html">Next research steps</a> · <a href="family-groups.html">All 14 family groups</a></p></section>"""
    page = shell('Our family', body)
    for asset in ('style.css', 'app.js'):
        version = hashlib.sha256((OUT / asset).read_bytes()).hexdigest()[:10]
        page = page.replace(f'"{asset}"', f'"{asset}?v={version}"')
    (OUT / 'index.html').write_text(page)

def build():
    OUT.mkdir(exist_ok=True)
    for asset in ('style.css','app.js','butterley.jpg'):
        shutil.copyfile(ROOT / 'site' / asset, OUT / asset)
    (OUT / '.nojekyll').write_text('')
    for path in sorted(ROOT.glob('*.md')) + sorted((ROOT / 'research').glob('*.md')):
        article(path)
    home(publish_stories())
    print(f'Built {len(list(OUT.rglob("*.html")))} pages in docs/')

if __name__ == '__main__':
    build()

"""Build the tree from the same household tables as the family directory."""
import re
from html import escape

# Ancestor, dates, partner, own group, parents' group, own entry in its first table.
GENERATIONS = [
    ('Roy Bentley', '1930–1998', 'Margaret Cartwright; later Betty (family account)', 1, 2, 1),
    ('Thomas Herbert Bentley', '1888/9–1965', 'Lauretta Jones', 2, 3, 2),
    ('John Bentley', '1861–1918', 'Sarah Ann Haigh', 3, 5, 2),
    ('Charles Bentley', 'Baptised 1828 · died 1897', 'Sarah Dyson', 5, 6, 6),
    ('William Bentley', 'Father at Standage in 1828', 'Betty, probably Betty Bottomley', 6, 7, 6),
    ('John Bentley', 'Baptised 1750 · buried 1789', 'Ann Broadbent', 7, 8, 1),
    ('James Bentley', 'Baptised 1722', 'Mary Nield', 8, 9, 0),
    ('Matthew Bentley', 'Buried 1751', 'Sarah', 9, None, None),
    ('Mathew Bentley', 'Baptised 1664', 'Possibly Ellin', 11, None, None),
    ('Jonas Bentley', 'Died 1686', '', 11, None, None),
    ('Mathew Bentley', 'Recorded in 1613–14', '', 11, None, None),
]
PARENTS = {2:'Thomas Herbert Bentley & Lauretta Jones',3:'John Bentley & Sarah Ann Haigh',
           5:'Charles Bentley & Sarah Dyson',6:'William Bentley & Betty',
           7:'John Bentley & Ann Broadbent',8:'James Bentley & Mary Nield',
           9:'Matthew Bentley & Sarah'}
EARLY = {
    7: ('Proposed father: Mathew Bentley', [('Ester Bentley','Baptised 1700'),('Unnamed daughter','Buried 1702 · identity open'),('John Bentley','Baptised 1702/3')], 'Possible siblings. These entries name a father Mathew. The clothier buried in 1751 is a proposed son. The unnamed burial may refer to a child listed here.'),
    8: ('Jonas Bentley', [('John Bentley','Baptised 1654')], 'The 1664 baptism names Jonas. Identifying this child with the adult later called “old Matthew” remains uncertain.'),
    9: ('Parents unknown', [], 'The relationship between Jonas and the Bentleys recorded in 1613–14 is unresolved.'),
    10: ('Parents unknown', [], 'The 1613 and 1614 records name Mathew as a father. His own parents and siblings remain unknown.'),
}

LIFE_CHAPTERS = [
    'roy-and-margaret-in-postwar-yorkshire', 'thomas-herbert-and-lauretta-in-the-local-paper',
    'john-the-piecer-becomes-a-weaver', 'charles-leaves-weaving-for-stone',
    'betty-and-the-four-weavers-at-carr-clough', 'john-and-ann-give-a-name-again',
    'james-and-mary-marry-at-christmas', 'matthew-and-sarah-in-the-cloth-country',
    'old-matthew-of-stone-edge', 'jonas-and-the-two-matthews', 'mathew-and-his-daughter-an',
]

def first_table(section):
    table = re.search(r'^\|[^\n]+\n\|[- |:]+\n((?:\|[^\n]+\n)+)', section, re.M)
    return [[cell.strip().replace('**','') for cell in line.strip('|').split('|')]
            for line in table.group(1).splitlines()]

def tree(sections):
    panels, options, links = [], [], []
    for i, (name, dates, partner, own, parents, self_index) in enumerate(GENERATIONS):
        key = f'gen-{i+1}'
        note = ''
        if parents:
            parent = PARENTS[parents]
            rows = first_table(sections[parents-1])
            if name.split()[0] not in rows[self_index][0]:
                raise ValueError(f'Ancestor row mismatch for {name}')
            siblings = [(r[0], r[1].split(';')[0], r[-1]) for j,r in enumerate(rows) if j != self_index]
            if i == 4:
                note = 'Possible siblings. These children belong to the parents of William Bently baptised in 1788. His identification with Betty’s husband remains open.'
        else:
            parent, records, note = EARLY[i]
            siblings = [(n,d,'') for n,d in records]
        cards = []
        for sibling, date, status in siblings:
            label = 'Family account' if status.startswith('F,') or status=='F' else 'Candidate' if 'Candidate' in status else ''
            url = f'#family-{parents or own}'
            if sibling == 'Helen Bentley': url = '#family-10'
            if i == 5 and sibling == 'Mary Bentley': url = '#family-8'
            info = f'<small>{escape(label)}</small>' if label else ''
            cards.append(f'<li><a href="{url}"><b>{escape(sibling)}</b><span>{escape(date)}</span>{info}</a></li>')
        sibling_list = '<ul class="peers">'+''.join(cards)+'</ul>' if cards else '<p class="unknown">No siblings identified in the available records.</p>'
        caption = 'Possible siblings' if i in (4,7) else 'Brothers and sisters'
        partner_line = f'<span>Partner · {escape(partner)}</span>' if partner else ''
        note_html = f'<p class="tree-note">{escape(note)}</p>' if note else ''
        parent_link = f'<a href="#family-{parents or own}">{escape(parent)}</a>'
        panels.append(f'''<article class="generation" id="{key}" aria-label="{escape(name)}, {escape(dates)}">
<div class="parent-node"><small>Parents</small>{parent_link}</div>
<div class="fork"><div class="ancestor"><small>Bentley line</small><h2>{escape(name)}</h2><p>{escape(dates)}</p>{partner_line}<a href="#family-{own}">View household →</a> <a href="stories/{LIFE_CHAPTERS[i]}.html">Read the story →</a></div>
<div class="siblings"><h3>{caption}</h3>{sibling_list}</div></div>{note_html}</article>''')
        options.append(f'<option value="{key}">{name} · {dates}</option>')
        links.append(f'<a href="#{key}"><b>{escape(name)}</b><span>{escape(dates)}</span></a>')
    return f'''<section id="tree" class="atlas"><div class="mast"><div><p>Marsden &nbsp;/&nbsp; Standedge &nbsp;/&nbsp; Saddleworth</p><h1>The Bentley family tree</h1></div><a href="#families">Find a relative ↓</a></div>
<div class="explorer"><div class="index"><h2>Generations</h2>{''.join(links)}</div>
<div class="chart"><div class="chart-tools"><label for="generation-select">Choose an ancestor</label><select id="generation-select">{''.join(options)}</select></div>{''.join(panels)}<div class="step js-only"><button id="younger">← More recent</button><button id="older">Earlier generation →</button></div></div></div></section>'''

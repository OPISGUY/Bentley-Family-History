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
PARENTS = {
    2: 'Thomas Herbert Bentley & Lauretta Jones',
    3: 'John Bentley & Sarah Ann Haigh',
    5: 'Charles Bentley & Sarah Dyson',
    6: 'William Bentley & Betty',
    7: 'John Bentley & Ann Broadbent',
    8: 'James Bentley & Mary Nield',
    9: 'Matthew Bentley & Sarah',
}
EARLY = {
    7: (
        'Proposed father: Mathew Bentley',
        [('Ester Bentley', 'Baptised 1700'), ('Unnamed daughter', 'Buried 1702 · identity open'), ('John Bentley', 'Baptised 1702/3')],
        'Possible siblings. These entries name a father Mathew. The clothier buried in 1751 is a proposed son, supported by shared Standedge residence and four-point child-naming correlations (Ellin, John, Esther and Matthew).',
    ),
    8: (
        'Jonas Bentley of Standedge',
        [('John Bentley', 'Baptised 1654 · fits Diggle carpenter d. 1713/14')],
        'The 1664 baptism names Jonas, whose 18 August 1686 inventory describes him as of Standedge. Identifying the 1664 child with “old Matthew” of Stone-edge remains probable.',
    ),
    9: (
        'Supported link: Mathew Bentley of 1613–14',
        [('An Bentley', 'Baptised 1 May 1613 (1613–14 household)'), ('Mathew Bentley', 'Baptised 2 Dec 1614 (1613–14 household)')],
        'Jonas is documented at Standedge in his 1686 inventory. While no baptism survives from the 1615–31 Bishop’s Transcript gap, Mathew and Jonas are the only two Bentley fathers in Saddleworth across 73 years (1613–86), and Jonas named his next son Mathew in 1664 after “Mathey” Bentley was buried in February 1657/8.',
    ),
    10: (
        'Parents unrecorded (pre-1612 register loss)',
        [],
        'The 1613 and 1614 diocesan transcripts name Mathew as a father after a 67-year local record gap (1545–1611). Born in the 1580s when Elizabethan families first adopted biblical names like Mathew and Jonas, he likely came from a father with a traditional Tudor name in adjacent Spotland/Rochdale (4 miles west) or Norland/Sowerby (6 miles northeast).',
    ),
}

LIFE_CHAPTERS = [
    'roy-and-margaret-in-postwar-yorkshire',
    'thomas-herbert-and-lauretta-in-the-local-paper',
    'john-the-piecer-becomes-a-weaver',
    'charles-leaves-weaving-for-stone',
    'two-brothers-at-the-font',
    'john-and-ann-give-a-name-again',
    'james-and-mary-marry-at-christmas',
    'matthew-and-sarah-in-the-cloth-country',
    'old-matthew-of-stone-edge',
    'jonas-and-the-two-matthews',
    'mathew-and-his-daughter-an',
]

HUMAN_PROFILES = [
    (
        'IV · Living Memory (1918–1998)',
        'Huddersfield, Slaithwaite & Fartown',
        'Postwar Yorkshire & Slaithwaite farm',
        'Documented',
        'verified',
        'Born in Huddersfield in the spring of 1930 to Thomas Herbert Bentley and Lauretta Jones, Roy bridges the archival record and living family memory. After marrying Margaret Cartwright in Upper Agbrigg in the autumn of 1953, family recollection follows him and his father to a farm in Slaithwaite before his later years at Fartown, where he died in 1998 within the childhood memory of the relative who preserved this story.',
    ),
    (
        'IV · Living Memory (1918–1998)',
        'Binn Road, Marsden & Slaithwaite',
        'Weaver’s son · Binn Road below Butterley',
        'Documented',
        'verified',
        'First glimpsed as a two-year-old boy in a woollen weaver’s cottage at Binn in the 1891 census—the very year Huddersfield Corporation tore down Upper Bank Bottom Mill (“Th’ Top Bonk”) below his home to build Butterley Reservoir. He married Lauretta Jones of Barkisland early in 1920; after forty-three years together, Friday’s Colne Valley Guardian recorded Lauretta’s passing in September 1963, and Thomas died eighteen months later in a terrace on Binn Road, back below the reservoir of his boyhood.',
    ),
    (
        'III · Marsden Mills & Quarries (1851–1934)',
        'Carr Clough & Binn, Marsden',
        'Woollen piecer (age 10) → Woollen weaver',
        'Documented',
        'verified',
        'Born at Carr Clough in early 1861 while his father and Aunt Ann wove woollens at home, John was already working in a Marsden mill at ten years old, piecing together broken wool threads while his fifteen-year-old sister Elizabeth wound bobbins. By thirty he was a woollen weaver and head of the household at Binn, married to Sarah Ann Haigh, raising four young children under one roof alongside Sarah Ann’s seventy-one-year-old Uncle Dan Haigh.',
    ),
    (
        'III · Marsden Mills & Quarries (1851–1934)',
        'Standage → Carr Clough & Binn, Marsden',
        'Handloom woollen weaver → Stone delver',
        'Documented',
        'verified',
        'Christened at St Chad’s, Saddleworth on 8 June 1828 as the son of William and Betty of Standage, Charles crossed the moor to Carr Clough in Marsden with his widowed mother and three weaving brothers by 1851. While his brothers Joseph, William and Wright sailed for Australia and remade their neighbourhood at 62–66 Carlisle Street in St Kilda, Charles stayed in Marsden, married Sarah Dyson in 1855, and in his forties put down the weaver’s shuttle to quarry stone on the hillside at Binn.',
    ),
    (
        'II · Standedge Clothiers (1686–1835)',
        'Meerleech, Standage, Coat Hill & Ridge',
        'Pennine woollen clothier',
        'Probable identity (1788 / 1819)',
        'probable',
        'Only nineteen months old when his father John died at Standedge in November 1789, William grew up to marry Betty Bottomley on 5 January 1815 and weave woollen cloth at Standage. On Sunday, 6 June 1819, William and Betty stood at the font of St Chad’s on the exact same day as his elder brother James and wife Ann—James naming a son Charles in 1819, and William and Betty giving that same name to our ancestor in 1828, before William’s death left Betty a widow at Ridge in 1835.',
    ),
    (
        'II · Standedge Clothiers (1686–1835)',
        'Barn, Standedge & Meerleech, Saddleworth',
        'Pennine woollen clothier',
        'Documented',
        'verified',
        'Married to Ann Broadbent at St Chad’s in 1771, John and Ann’s parish entries preserve a poignant portrait of eighteenth-century parental grief and perseverance: in 1776, 1777 and 1779 they buried three infant sons—two Johns and a William—each within forty-eight hours of baptism, before raising three surviving boys (John, James and William) on the Standedge ridge where John died in November 1789 aged thirty-nine.',
    ),
    (
        'II · Standedge Clothiers (1686–1835)',
        'Deanhead, Barn & Stone-edge (Standedge)',
        'Pennine woollen clothier',
        'Documented',
        'verified',
        'Baptised from Deanhead in March 1722 as the eldest child of Matthew and Sarah, James married Mary Nield on the day after Christmas in 1745. Starting their married life at Barn before moving up to Stone-edge by 1753, James carried on his father’s trade as a hillside clothier while raising Sarah, John, Esther, Mary, Betty and James on the Standedge escarpment.',
    ),
    (
        'II · Standedge Clothiers (1686–1835)',
        'Deanhead, Knowl, Knar & Stone-edge',
        'Yeoman clothier (Will dated 18 Nov 1751)',
        'Documented household · Probable son',
        'probable',
        'A hillside clothier whose household can be followed from Deanhead (1722) and Knowl (1723/4) to Stone-edge (1726–1751), where woollen pieces woven in farmhouse looms travelled by packhorse over the moor to market. With his wife Sarah he raised ten children whose names—including John, Esther, Helen (“Ellin” on her 1769 gravestone) and Matthew (born after “old Matthew” died in 1735/6)—bind his family to the elder generation on the same farm.',
    ),
    (
        'II · Standedge Clothiers (1686–1835)',
        'Stone-edge (Standedge), Saddleworth',
        'Hillside householder (“old Matthew”)',
        'Probable identity (1664–1735/6)',
        'probable',
        'Christened on 11 December 1664 as the younger son of Jonas Bentley, he was twenty-one when his father died at Standedge in 1686. He buried an unnamed daughter in December 1702, raised Ester (1700) and John (1702/3), lost his wife Ellin in May 1719, and lived past seventy on the windy escarpment of Stone-edge—so long that when he was buried in February 1735/6 beside the younger Matthew’s household, the parish clerk called him simply “old Matthew”.',
    ),
    (
        'I · The 17th-Century Frontier (1613–1686)',
        'Standedge, Saddleworth',
        'Smallholder at Standedge (1686 Inventory)',
        'Documented at Standedge · Supported link',
        'probable',
        'The earliest Bentley documented on the high ridge of Standedge by name. Born during the 1615–1631 gap in St Chad’s loose diocesan transcripts, Jonas baptised his elder son John in August 1654 (who fits the Diggle carpenter of 1713/14) and—after the burial of old “Mathey” Bentley in February 1657/8—named his next recorded son Mathew in December 1664. His 18 August 1686 probate inventory places him “of Standedge, Saddleworth” forty years earlier than the parish registers.',
    ),
    (
        'I · The 17th-Century Frontier (1613–1686)',
        'Chapelry of St Chad, Saddleworth',
        'Earliest recorded Saddleworth Bentley father',
        'Documented 1613–14 baptisms',
        'probable',
        'On 1 May 1613—on only the second surviving annual sheet of St Chad’s register after a 67-year local blackout—Mathew Bentley brought his daughter An to be christened in Saddleworth, followed nineteen months later by a son Mathew on 2 December 1614. Across 73 years (1613–1686), Mathew and Jonas of Standedge are the only two Bentley fathers recorded anywhere in Saddleworth, while a 1619–20 Manchester hue and cry and a January 1638/9 committal order to York Castle preserve dramatic traces of the name before the Civil War.',
    ),
]

def first_table(section):
    table = re.search(r'^\|[^\n]+\n\|[- |:]+\n((?:\|[^\n]+\n)+)', section, re.M)
    return [[cell.strip().replace('**', '') for cell in line.strip('|').split('|')]
            for line in table.group(1).splitlines()]

def tree(sections):
    panels, options, links = [], [], []
    last_era = None
    for i, (name, dates, partner, own, parents, self_index) in enumerate(GENERATIONS):
        key = f'gen-{i+1}'
        era, place, trade, badge_text, badge_kind, bio = HUMAN_PROFILES[i]
        note = ''
        if parents:
            parent = PARENTS[parents]
            rows = first_table(sections[parents-1])
            if name.split()[0] not in rows[self_index][0]:
                raise ValueError(f'Ancestor row mismatch for {name}')
            siblings = [(r[0], r[1].split(';')[0], r[-1]) for j, r in enumerate(rows) if j != self_index]
            if i == 4:
                note = 'Possible siblings. These children belong to the parents of William Bently baptised in 1788. On 6 June 1819, William & Betty and James & Ann stood at St Chad’s on the same Sunday to baptise sons William and Charles, strongly supporting their brotherhood.'
        else:
            parent, records, note = EARLY[i]
            siblings = [(n, d, '') for n, d in records]
        cards = []
        for sibling, date, status in siblings:
            label = 'Family account' if status.startswith('F,') or status == 'F' else 'Candidate' if 'Candidate' in status else ''
            url = f'#family-{parents or own}'
            if sibling == 'Helen Bentley':
                url = '#family-10'
            if i == 5 and sibling == 'Mary Bentley':
                url = '#family-8'
            info = f'<small>{escape(label)}</small>' if label else ''
            cards.append(f'<li><a href="{url}"><b>{escape(sibling)}</b><span>{escape(date)}</span>{info}</a></li>')
        sibling_list = '<ul class="peers">' + ''.join(cards) + '</ul>' if cards else '<p class="unknown">No siblings identified in the surviving records for this generation.</p>'
        caption = 'Possible brothers, sisters & kin' if i in (4, 7, 9) else 'Brothers and sisters in the household'
        partner_line = f'<span class="partner-line">Partner · <strong>{escape(partner)}</strong></span>' if partner else ''
        note_html = f'<p class="tree-note">{escape(note)}</p>' if note else ''
        parent_link = f'<a href="#family-{parents or own}">{escape(parent)}</a>'
        panels.append(f'''<article class="generation" id="{key}" aria-label="Generation {i+1}: {escape(name)}, {escape(dates)}">
<div class="gen-ribbon"><span class="gen-num">Generation {i+1} of 11</span><span class="gen-era">{escape(era)}</span><span class="gen-badge {badge_kind}">{escape(badge_text)}</span></div>
<div class="parent-node"><small>Preceding generation / household</small>{parent_link}</div>
<div class="fork"><div class="ancestor"><div class="ancestor-top"><small>{escape(place)}</small><h2>{escape(name)}</h2><p class="ancestor-dates">{escape(dates)} &nbsp;·&nbsp; <em>{escape(trade)}</em></p>{partner_line}</div>
<p class="ancestor-bio">{escape(bio)}</p>
<div class="ancestor-links"><a class="card-btn" href="#family-{own}">Explore household records →</a> <a class="card-btn ghost" href="stories/{LIFE_CHAPTERS[i]}.html">Read their story →</a></div></div>
<div class="siblings"><h3>{caption}</h3>{sibling_list}</div></div>{note_html}</article>''')
        options.append(f'<option value="{key}">Gen {i+1}: {name} ({dates})</option>')
        if era != last_era:
            links.append(f'<div class="era-divider">{escape(era)}</div>')
            last_era = era
        links.append(f'<a href="#{key}"><b>{escape(name)}</b><span>{escape(dates)} · {escape(place.split(",")[0])}</span></a>')
    return f'''<section id="tree" class="atlas"><div class="mast"><div><p>Eleven Generations · Marsden, Standedge &amp; Saddleworth (1613–1998)</p><h1>The Interactive Family Chronicle</h1><p class="mast-sub">Select any ancestor to read their human portrait, see the brothers and sisters who grew up beside them, and jump straight to their story or parish records.</p></div><div class="mast-actions"><button type="button" id="toggle-all-gens" class="secondary js-only">Show all 11 generations</button><a class="button secondary" href="#families">Search 14 family groups ↓</a></div></div>
<div class="explorer"><div class="index"><h2>11 Generations</h2>{''.join(links)}</div>
<div class="chart"><div class="chart-tools"><label for="generation-select">Choose an ancestor</label><select id="generation-select">{''.join(options)}</select></div>{''.join(panels)}<div class="step js-only"><button id="younger">← More recent generation</button><span id="step-indicator" class="step-indicator">Generation 4 of 11</span><button id="older">Earlier generation →</button></div></div></div></section>'''

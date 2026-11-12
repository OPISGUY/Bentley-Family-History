'use strict';
document.documentElement.classList.add('js');
const families = [...document.querySelectorAll('.family')];
const search = document.querySelector('#family-search');
const branch = document.querySelector('#branch');
const count = document.querySelector('#result-count');
const empty = document.querySelector('#no-results');
const chips = [...document.querySelectorAll('.chip[data-chip]')];

function updateChips() {
  if (!search) return;
  const val = search.value.trim().toLocaleLowerCase();
  chips.forEach(c => {
    c.classList.toggle('active', val !== '' && c.dataset.chip.toLocaleLowerCase() === val);
  });
}

function filterFamilies() {
  const query = search.value.trim().toLocaleLowerCase();
  let shown = 0;
  families.forEach(f => {
    const match = f.textContent.toLocaleLowerCase().includes(query) && (branch.value === 'all' || f.dataset.branch === branch.value);
    f.hidden = !match;
    if (match) { shown++; if (query) f.open = true; }
  });
  count.textContent = `${shown} of ${families.length} household groups shown`;
  empty.hidden = shown !== 0;
  updateChips();
}

if (search) {
  search.addEventListener('input', filterFamilies);
  branch.addEventListener('change', filterFamilies);
  document.querySelector('#reset').addEventListener('click', () => {
    search.value = '';
    branch.value = 'all';
    filterFamilies();
    search.focus();
  });
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const target = chip.dataset.chip;
      if (search.value.trim().toLocaleLowerCase() === target.toLocaleLowerCase()) {
        search.value = '';
      } else {
        search.value = target;
        branch.value = 'all';
      }
      filterFamilies();
    });
  });
  document.querySelector('#expand').addEventListener('click', () => families.filter(f => !f.hidden).forEach(f => f.open = true));
  document.querySelector('#collapse').addEventListener('click', () => families.forEach(f => f.open = false));
  filterFamilies();
}

function revealFamily() {
  const id = decodeURIComponent(location.hash.slice(1));
  const el = document.getElementById(id);
  const family = el?.closest('.family');
  if (family) {
    if (family.hidden && search) { search.value = ''; branch.value = 'all'; filterFamilies(); }
    family.open = true;
    requestAnimationFrame(() => el.scrollIntoView({block: 'start'}));
  }
}
window.addEventListener('hashchange', revealFamily);
revealFamily();

let beforePrint = [];
window.addEventListener('beforeprint', () => { beforePrint = families.map(f => f.open); families.forEach(f => f.open = true); });
window.addEventListener('afterprint', () => families.forEach((f, i) => f.open = beforePrint[i]));
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));

const generations = [...document.querySelectorAll('.generation')];
if (generations.length) {
  const choice = document.querySelector('#generation-select');
  const younger = document.querySelector('#younger');
  const older = document.querySelector('#older');
  const indicator = document.querySelector('#step-indicator');
  const toggleAll = document.querySelector('#toggle-all-gens');
  const stepBar = document.querySelector('.step');
  let current = 3;
  let showAllMode = false;

  function show(index) {
    current = index;
    const key = generations[index].id;
    choice.value = key;
    generations.forEach((panel, i) => {
      panel.hidden = showAllMode ? false : (i !== index);
    });
    document.querySelectorAll('.index a').forEach((link, i) => {
      if (!showAllMode && i === index) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
    younger.disabled = showAllMode || index === 0;
    older.disabled = showAllMode || index === generations.length - 1;
    if (indicator) {
      const h2 = generations[index].querySelector('h2')?.textContent || '';
      indicator.textContent = showAllMode ? `Showing all ${generations.length} generations` : `Generation ${index + 1} of ${generations.length} · ${h2}`;
    }
    if (stepBar) stepBar.hidden = showAllMode;
  }

  function followHash() {
    const index = generations.findIndex(panel => '#' + panel.id === location.hash);
    if (index >= 0) {
      if (showAllMode) {
        generations[index].scrollIntoView({block: 'start'});
      } else {
        show(index);
      }
    }
  }

  function jump(index) {
    showAllMode = false;
    if (toggleAll) toggleAll.textContent = 'Show all 11 generations';
    show(index);
    location.hash = generations[index].id;
  }

  if (toggleAll) {
    toggleAll.addEventListener('click', () => {
      showAllMode = !showAllMode;
      toggleAll.textContent = showAllMode ? 'Step one generation at a time' : 'Show all 11 generations';
      show(current);
    });
  }

  choice.addEventListener('change', () => jump(choice.selectedIndex));
  younger.addEventListener('click', () => jump(current - 1));
  older.addEventListener('click', () => jump(current + 1));
  window.addEventListener('hashchange', followHash);
  show(current);
  followHash();
}

/* ==========================================================================
   Interactive Cartographic Atlas Engine (#atlas-map)
   ========================================================================== */
const atlasSvg = document.querySelector('#bentley-atlas-svg');
if (atlasSvg) {
  const PLACES = [
    {
      short: '1. St Chad’s',
      stop: 'Place 1 of 15 · 1613–1835',
      grid: 'St Chad’s, Uppermill · Saddleworth',
      title: 'St Chad’s Church, Saddleworth',
      who: 'Generations here: Mathew & An (1613–14) · Jonas (1654–86) · Old Matthew & Ellin (1700–35/6) · Helen (“Ellin”) Platt (1769 gravestone) · Brothers William & James at the font (6 June 1819)',
      story: 'Founded in 1215 as a moorland chapelry of St Chad, Rochdale, this hillside church is the cradle of the surviving Bentley record. On 1 May 1613—on only the second surviving annual sheet of St Chad’s register—Mathew Bentley christened his daughter An here. Here “old Matthew” of Stone-edge was buried in February 1735/6, here Helen Platt’s 1769 gravestone still spells her name “Ellin”, and here on Sunday, 6 June 1819, brothers William and James Bentley of Standage stood side by side at the font to christen their sons William and Charles.',
      evidence: 'St Chad’s Diocesan Transcripts (1613–14); Parish Registers (1632–1835); Ellin & Thomas Platt Gravestone in the Old Churchyard (1769 / 1789, Kidd 1994, p. 4); Double Baptism of 6 June 1819.',
      storyUrl: 'stories/mathew-and-his-daughter-an.html',
      familyUrl: '#family-11',
      era: 'early',
      coords: [125, 425],
      cam: [20, 210, 480, 300]
    },
    {
      short: '2. Diggle & Fairbanks',
      stop: 'Place 2 of 15 · 1654–1764',
      grid: 'Diggle Brook & Fairbanks · Saddleworth',
      title: 'Diggle & Fairbanks',
      who: 'Generations here: John Bentley of Diggle, Carpenter (inv. Feb 1713/14) · Mary Bentley & James Bradbury of Fairbanks (m. July 1714, wills 1756 & 1764)',
      story: 'Just below the Standedge escarpment where Diggle Brook gathers from the moss, John Bentley worked as a village carpenter—shaping roof timbers, loom frames and oak chests for his clothier neighbours until his probate inventory was proved at Chester in February 1713/14. Five months later, in July 1714, Mary Bentley married yeoman-clothier James Bradbury of Fairbanks, Diggle by ecclesiastical licence, founding a prosperous household documented in wills of 1756 and 1764.',
      evidence: 'Chester Probate Inventory of John Bentley of Diggle, Carpenter (Feb 1713/14); Marriage Licence Bond (3 July 1714) & St Chad’s Marriage (10 July 1714); Wills of James Bradbury (1756) & Mary Bradbury (1764).',
      storyUrl: 'stories/the-carpenter-of-diggle-and-the-summer-wedding.html',
      familyUrl: '#family-11',
      era: 'early',
      coords: [295, 295],
      cam: [90, 145, 480, 300]
    },
    {
      short: '3. Stone-edge',
      stop: 'Place 3 of 15 · 1686–1792',
      grid: 'High Standedge Escarpment · 1,400 ft',
      title: 'Stone-edge (High Standedge)',
      who: 'Generations here: Jonas Bentley of Standedge (inv. 18 Aug 1686) · Mathew (“old Matthew”) & Ellin of Stone-edge (bur. 1735/6 & 1721/2) · Matthew & Sarah Bentley (d. 1751) · James & Mary (née Nield)',
      story: 'Before St Chad’s clerks wrote hamlet names into the parish book, Jonas Bentley’s 18 August 1686 probate inventory already places the family “of Standedge, Saddleworth”. Here on the wind-scoured Pennine ridge—“Stone-edge” in the 18th-century registers—old Matthew and Ellin raised their children, Matthew and Sarah kept their woollen looms and three cows until the winter of 1750/1, and James and Mary raised ten children between 1750 and 1775.',
      evidence: 'Leonard Kidd Probate Abstract of Jonas Bentley of Standedge (18 Aug 1686, H/KID p. 248); Burials of Ellin (12 Jan 1721/2) & Mathew of Stone-edge (7 Feb 1735/6); Will & Inventory of Matthew Bentley of Standedge (1751, H/KID p. 79).',
      storyUrl: 'stories/old-matthew-of-stone-edge.html',
      familyUrl: '#family-9',
      era: 'early',
      coords: [385, 195],
      cam: [145, 75, 480, 300]
    },
    {
      short: '4. Deanhead & Acre',
      stop: 'Place 4 of 15 · 1722–1750',
      grid: 'Northern Castleshaw Rim · Saddleworth',
      title: 'Deanhead & Acre',
      who: 'Generations here: Matthew & Sarah Bentley (at Deanhead in Oct 1722) · Michael Bentley of Acre, Clothier (at Acre 1730–50)',
      story: 'When Matthew and Sarah Bentley brought their infant son James to St Chad’s on 20 October 1722, their abode was recorded as Deanhead, high on the northern rim of the Castleshaw valley beneath Standedge. A mile away at Acre, clothier Michael Bentley and his wife Mary (née Radcliffe) raised eight children between 1727 and 1750, repeating the signature Standedge names John, James and Sarah.',
      evidence: 'St Chad’s Baptism of James, son of Matthew & Sarah Bentley of Deanhead (20 Oct 1722); Baptisms & Burials of Michael Bentley of Acre, clothier (1727–1750).',
      storyUrl: 'stories/matthew-and-sarah-in-the-cloth-country.html',
      familyUrl: '#family-9',
      era: 'standedge',
      coords: [255, 138],
      cam: [60, 45, 480, 300]
    },
    {
      short: '5. Knowl & Knar',
      stop: 'Place 5 of 15 · 1723/4–1744',
      grid: 'Castleshaw & Delph Slope · Saddleworth',
      title: 'Knowl (Knowle Farm) & Knar',
      who: 'Generations here: Matthew & Sarah Bentley · Children baptised here: John (1723/4), Mary (1726), Sarah (1729), Patience (1731), Helen/Ellin (1733/4) & Matthew (1738/9)',
      story: 'Between 1723/4 and 1738/9, Matthew and Sarah Bentley lived at Knowl (modern Knowle Farm above Castleshaw), moving to Knar by 1744 when seventeen-year-old Mary was buried. Like many Saddleworth yeoman-clothier families, they shifted tenancies among neighbouring hillside farmsteads while remaining part of the same tight-knit Standedge community.',
      evidence: 'St Chad’s Baptisms at Knowl (9 Feb 1723/4 to 14 Jan 1738/9) and Burial of Mary Bentley of Knar (9 June 1744).',
      storyUrl: 'stories/matthew-and-sarah-in-the-cloth-country.html',
      familyUrl: '#family-9',
      era: 'standedge',
      coords: [225, 295],
      cam: [45, 145, 480, 300]
    },
    {
      short: '6. Heyhouse & Whams',
      stop: 'Place 6 of 15 · 1752–1833',
      grid: 'Denshaw Moor & Castleshaw · Saddleworth',
      title: 'Heyhouse, Whams Inn & Ogden',
      who: 'Generations here: Helen (“Ellin”) Bentley & Thomas Platt (m. 1752, d. 1769 & 1789) · John & Alice Platt of Wham · Granddaughter Hannah Platt & Joseph Gartside of Heyhouse (m. 1806, emigrated to New Jersey 1831)',
      story: 'After Helen (“Ellin”) Bentley married clothier Thomas Platt on 6 August 1752, their family worked the high farms at Standedge, Wham (by the old Whams Inn above Denshaw) and Heyhouse. From Heyhouse, their granddaughter Hannah Platt and her husband Joseph Gartside walked twenty-six miles to Liverpool in May 1831 with eight children and twenty gold sovereigns to sail for America aboard the ship Manchester.',
      evidence: 'St Chad’s Marriage (6 Aug 1752); Gravestone of Ellin (1769) & Thomas Platt (1789); Gartside Family Reminiscence of Joseph & Hannah (née Platt) Gartside (1831).',
      storyUrl: 'stories/hannah-and-the-journey-to-liverpool.html',
      familyUrl: '#family-10',
      era: 'standedge',
      coords: [155, 165],
      cam: [25, 50, 480, 300]
    },
    {
      short: '7. “Bentleys” & Standedge Foot',
      stop: 'Place 7 of 15 · 1791–1822',
      grid: '1822 Map of Saddleworth · Burk Clough',
      title: '“Bentleys” at Rough & Standedge Foot',
      who: 'Generations here: John & Ann Bentley (née Broadbent, m. 1779) · Co-owners John Bentley of Bentleys & James Bentley of Bleak Hey Nook (26 Nov 1791) · William & James Bentley (1819)',
      story: 'For over a century a freehold two-cottage farmstead on the old packhorse climb beside Burk Clough literally bore the family’s surname: “Bentleys” at Rough, printed in capital letters right beside “STANEDGE FOOT” on the 1822 Map of Saddleworth. On 26 November 1791, Saddleworth Moor enclosure deeds record John Bentley living inside “Bentleys” while co-owning the two cottages and eight acres with his brother James.',
      evidence: 'Saddleworth Manor Court Roll (1680); Saddleworth Moor Enclosure Deeds (26 Nov 1791); Manchester Mercury Auction Notice for the Rose & Crown, Standedge-Foot (12 May 1806); 1822 Map of Saddleworth.',
      storyUrl: 'stories/bentleys-at-standedge-foot.html',
      familyUrl: '#family-7',
      era: 'standedge',
      coords: [338, 228],
      cam: [110, 85, 480, 300]
    },
    {
      short: '8. Bleak Hey Nook',
      stop: 'Place 8 of 15 · 1791–1806',
      grid: 'Stanedge Turnpike · Delph Slope',
      title: 'Bleak Hey Nook (Bentley Farmhouse)',
      who: 'Generations here: James Bentley of Bleak Hey Nook, Clothier (1791–1806, co-owner of “Bentleys”) · John & Ann Bentley at Barn & Meerleech',
      story: 'Half a mile down the Stanedge turnpike towards Delph stands Bleak Hey Nook, where a Grade II listed three-storey weavers’ cottage still bears the historic name “Bentley Farmhouse”. On 26 November 1791, clothier James Bentley lived here at Bleak Hey Nook while co-owning the two cottages at “Bentleys” up the hill with John Bentley.',
      evidence: 'Saddleworth Moor Enclosure Deeds (26 Nov 1791); 1806 Auction Notice naming James Bentley of Bleak-Hey-Nook; Historic England Grade II Listing (Bentley Farmhouse, Bleak Hey Nook).',
      storyUrl: 'stories/bentleys-at-standedge-foot.html',
      familyUrl: '#family-7',
      era: 'standedge',
      coords: [262, 232],
      cam: [70, 90, 480, 300]
    },
    {
      short: '9. Woodmans',
      stop: 'Place 9 of 15 · 1784–1791',
      grid: 'Heights Side above Delph · Saddleworth',
      title: 'Woodmans (Two-Dwelling Farmhouse)',
      who: 'Generations here: Uncle Matthew Bentley (bap. 1738/9, at Woodmans 1784–91) & Thomas Rhodes (father of niece Esther Bentley’s 1779 child James)',
      story: 'On 26 November 1791—the very same day John and James Bentley were recorded at “Bentleys” and Bleak Hey Nook—a conveyance for the two-dwelling farmhouse called Woodmans names its two sitting tenants side by side: Matthew Bentley and Thomas Rhodes. Thomas Rhodes was the father of Esther Bentley’s 1779 Standedge child, showing uncle and niece’s partner sharing the same roof.',
      evidence: 'St Chad’s Baptism of James, son of Esther Bentley of Standedge & Thomas Rhodes of Intack (6 June 1779); Burial of John s. of Mathew Bentley of Woodmans (17 May 1784); Woodmans Conveyance (26 Nov 1791).',
      storyUrl: 'stories/bentleys-at-standedge-foot.html',
      familyUrl: '#family-8',
      era: 'standedge',
      coords: [145, 255],
      cam: [25, 110, 480, 300]
    },
    {
      short: '10. Coat Hill & Ridge',
      stop: 'Place 10 of 15 · 1831–1835',
      grid: 'Diggle Edge & Delph Slope · Saddleworth',
      title: 'Coat Hill & Ridge',
      who: 'Generations here: William & Betty Bentley (at Coat Hill in 1831 & Ridge in 1835) · Children: Joseph, William, Charles (bap. 1828), John (bap. 1831) & Wright (bap. 1835)',
      story: 'After standing with his brother James at St Chad’s font on 6 June 1819 as a clothier of Standage, William Bentley and his wife Betty lived at Standage through 1828 (when our ancestor Charles was baptised), then worked looms at Coat Hill in April 1831 and Ridge above Diggle in February 1835 before crossing the Pennine watershed into Marsden.',
      evidence: 'St Chad’s Baptisms of Charles (15 June 1828, Standage), John (17 April 1831, Coat Hill, weaver) & Wright (15 Feb 1835, Ridge, weaver).',
      storyUrl: 'stories/two-brothers-at-the-font.html',
      familyUrl: '#family-6',
      era: 'standedge',
      coords: [215, 358],
      cam: [45, 185, 480, 300]
    },
    {
      short: '11. Carr Clough, Marsden',
      stop: 'Place 11 of 15 · 1851–1861',
      grid: '1851 & 1861 Census · West Riding of Yorkshire',
      title: 'Carr Clough & Clough Lee, Marsden',
      who: 'Generations here: Widowed Betty Bentley (1851) · Four weaving brothers: Joseph, William, Charles & Wright · Ann Bentley (aged 5 in 1851) · Charles & Sarah (née Dyson) & infant John (1861)',
      story: 'By 1851 widowed Betty Bentley had brought her household across the Standedge ridge into Carr Clough on the western edge of Marsden. All four sons—Joseph (27), William (25), Charles (22) and Wright (16)—worked as woollen power-loom or handloom weavers, while five-year-old Ann sat by the hearth. Within ten years Joseph, William and Wright sailed for Australia, leaving Charles and his new bride Sarah Dyson at Carr Clough.',
      evidence: '1851 Census of Marsden (HO107/2296, Carr Clough); St Bartholomew’s Marriage of Charles Bentley & Sarah Dyson (1856); 1861 Census (RG9/3269, Carr Clough).',
      storyUrl: 'stories/betty-and-the-four-weavers-at-carr-clough.html',
      familyUrl: '#family-6',
      era: 'marsden',
      coords: [565, 165],
      cam: [430, 50, 520, 325]
    },
    {
      short: '12. Binn & Lane Syke Quarry',
      stop: 'Place 12 of 15 · 1871–1965',
      grid: 'OS Sheet CCLIX.11 · Above Wessenden Brook',
      title: 'Binn, Lane Syke Quarry & Binn Road',
      who: 'Generations here: Charles & Sarah Bentley (1871–97) · John & Sarah Ann (née Haigh, 1881–1913) · Uncle Dan Haigh · Thomas Herbert & Lauretta Bentley (at 132 Binn Road until 1965)',
      story: 'Between 1861 and 1871 Charles Bentley traded the weaver’s shuttle for the crowbar and wedge, becoming a stone quarryman at Binn above the widened Wessenden Reservoir Road. In 1881 Binn held 18 households and 78 neighbours—including both the Bentleys and the Haighs. John married Sarah Ann Haigh in 1880, and three generations of Bentleys lived on Binn hillside and Binn Road for nearly a century.',
      evidence: '1871, 1881, 1891, 1901 & 1911 Censuses of Binn, Marsden; 1881 Binn Hamlet Profile (18 households, 78 residents); Probate of Thomas Herbert Bentley of 132 Binn Road (1965).',
      storyUrl: 'stories/charles-leaves-weaving-for-stone.html',
      familyUrl: '#family-3',
      era: 'marsden',
      coords: [682, 268],
      cam: [460, 75, 520, 325]
    },
    {
      short: '13. Butterley & Drowned Mill',
      stop: 'Place 13 of 15 · 1876–1913',
      grid: 'Wessenden Mouth · Below Binn Road',
      title: 'Butterley Reservoir, “Th’ Top Bonk” & Ottiwells Mill',
      who: 'Generations here: John Bentley (10-year-old woollen piecer in 1871; woollen weaver 1881–1913) · Sarah Ann (née Haigh) · Young Thomas Herbert Bentley (born 1885)',
      story: 'When ten-year-old John Bentley walked down from Binn in 1871 as a woollen piecer, two mills stood in the clough below: Lower Bank Bottom Mill and Upper Bank Bottom Mill (“Th’ Top Bonk”, rebuilt after an 1876 fire). In 1891—when young Thomas Herbert was six—Huddersfield Corporation demolished Upper Bank Bottom Mill and built the huge stone spillway of Butterley Reservoir directly over its site.',
      evidence: '1871–1911 Censuses; Colne Valley Museum & Huddersfield Exposed histories of Upper/Lower Bank Bottom Mills and Ottiwells Mill; Butterley Reservoir Act (1890–1907).',
      storyUrl: 'stories/john-the-piecer-becomes-a-weaver.html',
      familyUrl: '#family-3',
      era: 'marsden',
      coords: [695, 198],
      cam: [465, 55, 520, 325]
    },
    {
      short: '14. Marsden Church & Slaithwaite',
      stop: 'Place 14 of 15 · 1918–1998',
      grid: 'Colne Valley · Marsden, Slaithwaite & Huddersfield',
      title: 'St Bartholomew’s Marsden, Slaithwaite & Huddersfield',
      who: 'Generations here: Thomas Herbert Bentley & Lauretta Jones (m. 1920) · Roy Bentley (1920–1998) & Margaret Cartwright (m. 1945) · Living generations',
      story: 'After Sarah Ann died in 1913 and John in 1918 (commemorated on the Haigh-Bentley stone at St Bartholomew’s, Marsden), Thomas Herbert Bentley married Lauretta Jones in 1920—celebrated in the Huddersfield Daily Examiner. They farmed in Slaithwaite alongside their son Roy before retiring to 132 Binn Road, while Roy and Margaret Cartwright carried the family into postwar Huddersfield.',
      evidence: 'St Bartholomew’s Memorial Inscription; Huddersfield Daily Examiner Marriage Notice (1920); GRO Civil Registrations (1920, 1945, 1965, 1998).',
      storyUrl: 'stories/thomas-herbert-and-lauretta-in-the-local-paper.html',
      familyUrl: '#family-1',
      era: 'marsden',
      coords: [845, 118],
      cam: [480, 25, 510, 320]
    },
    {
      short: '15. Carlisle St, St Kilda',
      stop: 'Place 15 of 15 · 1854–1950',
      grid: 'Melbourne, Victoria · Nos. 62, “Stockwell” & 66',
      title: '62–66 Carlisle Street, St Kilda (Melbourne)',
      who: 'Generations here: Three sons of William & Betty of Standage: William & Hannah (No. 62) · Wright & Helen (“Stockwell”) · Joseph & Ann (“Baroona”, No. 66)',
      story: 'Twelve thousand miles from Standedge and Carr Clough, Charles’s three brothers recreated their Yorkshire closeness along a single street in St Kilda, Melbourne. William and Hannah lived at 62 Carlisle Street, Wright and Helen lived next door at “Stockwell”, and Joseph and Ann lived at “Baroona”, 66 Carlisle Street—where newspaper notices prove that Joseph’s first family (begun in quarantine at Point Nepean on the Tornado in 1854) and second family shared the same father.',
      evidence: 'Point Nepean Quarantine Register (1854); Melbourne Argus & Age Family Notices via Trove (1891, 1901, 1902, 1907, 1915, 1950); Victorian BDM Certificates.',
      storyUrl: 'stories/three-houses-on-carlisle-street.html',
      familyUrl: '#family-12',
      era: 'stkilda',
      coords: [815, 498],
      cam: [525, 350, 465, 260]
    }
  ];

  const pins = [...atlasSvg.querySelectorAll('.map-pin')];
  const camBtns = [...document.querySelectorAll('.cam-btn')];
  const eraPills = [...document.querySelectorAll('.era-pill')];
  const hopLine = document.querySelector('#active-hop-line');
  const dossierPanel = document.querySelector('#map-dossier-panel');
  const stopEl = document.querySelector('#dossier-stop');
  const gridEl = document.querySelector('#dossier-grid');
  const titleEl = document.querySelector('#dossier-title');
  const whoEl = document.querySelector('#dossier-who');
  const storyEl = document.querySelector('#dossier-story');
  const evidenceEl = document.querySelector('#dossier-evidence');
  const storyLinkEl = document.querySelector('#dossier-story-link');
  const familyLinkEl = document.querySelector('#dossier-family-link');
  const pillNav = document.querySelector('#place-pill-nav');
  const prevBtn = document.querySelector('#map-prev');
  const nextBtn = document.querySelector('#map-next');
  const playBtn = document.querySelector('#map-play');
  const progressBar = document.querySelector('#tour-progress-bar');
  const counterEl = document.querySelector('#tour-counter');

  let currentPlace = 0;
  let currentViewBox = [0, 0, 1000, 620];
  let animFrameId = null;
  let tourTimer = null;
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Build 15 quick-jump pills inside the dossier panel
  const quickPills = PLACES.map((p, idx) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'place-pill' + (idx === 0 ? ' active' : '');
    btn.textContent = p.short;
    btn.addEventListener('click', () => {
      stopTour();
      selectPlace(idx, { zoom: true });
    });
    if (pillNav) pillNav.appendChild(btn);
    return btn;
  });

  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function animateViewBox(targetBox, duration = 720) {
    if (animFrameId) cancelAnimationFrame(animFrameId);
    if (prefersReducedMotion || duration <= 0) {
      currentViewBox = [...targetBox];
      atlasSvg.setAttribute('viewBox', currentViewBox.map(n => n.toFixed(1)).join(' '));
      return;
    }
    const startBox = [...currentViewBox];
    const startTime = performance.now();
    function step(now) {
      const elapsed = now - startTime;
      const t = Math.min(1, elapsed / duration);
      const e = easeInOutCubic(t);
      currentViewBox = startBox.map((s, i) => s + (targetBox[i] - s) * e);
      atlasSvg.setAttribute('viewBox', currentViewBox.map(n => n.toFixed(1)).join(' '));
      if (t < 1) {
        animFrameId = requestAnimationFrame(step);
      } else {
        animFrameId = null;
      }
    }
    animFrameId = requestAnimationFrame(step);
  }

  function updateDossier(place) {
    if (!dossierPanel) return;
    dossierPanel.classList.add('dossier-updating');
    setTimeout(() => {
      stopEl.textContent = place.stop;
      gridEl.textContent = place.grid;
      titleEl.textContent = place.title;
      whoEl.textContent = place.who;
      storyEl.textContent = place.story;
      evidenceEl.textContent = place.evidence;
      storyLinkEl.setAttribute('href', place.storyUrl);
      familyLinkEl.setAttribute('href', place.familyUrl);
      dossierPanel.classList.remove('dossier-updating');
    }, prefersReducedMotion ? 0 : 120);
  }

  function selectPlace(index, { zoom = false } = {}) {
    const prevIndex = currentPlace;
    currentPlace = (index + PLACES.length) % PLACES.length;
    const place = PLACES[currentPlace];

    pins.forEach((pin, i) => {
      pin.classList.toggle('active', i === currentPlace);
    });
    quickPills.forEach((pill, i) => {
      pill.classList.toggle('active', i === currentPlace);
    });

    // Draw animated connection hop line from previous place to newly selected place
    if (hopLine && prevIndex !== currentPlace) {
      const [x1, y1] = PLACES[prevIndex].coords;
      const [x2, y2] = place.coords;
      hopLine.setAttribute('x1', String(x1));
      hopLine.setAttribute('y1', String(y1));
      hopLine.setAttribute('x2', String(x2));
      hopLine.setAttribute('y2', String(y2));
      hopLine.style.opacity = '0.9';
    }

    if (progressBar) {
      progressBar.style.width = `${((currentPlace + 1) / PLACES.length) * 100}%`;
    }
    if (counterEl) {
      counterEl.textContent = `Place ${currentPlace + 1} of ${PLACES.length}`;
    }

    updateDossier(place);

    if (zoom && place.cam) {
      animateViewBox(place.cam, 780);
      camBtns.forEach(b => b.classList.remove('active'));
    }
  }

  function stopTour() {
    if (tourTimer) {
      clearInterval(tourTimer);
      tourTimer = null;
    }
    if (playBtn) {
      playBtn.classList.remove('playing');
      playBtn.textContent = '▶ Auto-Walk All 15 Places';
    }
  }

  function toggleTour() {
    if (tourTimer) {
      stopTour();
      return;
    }
    if (playBtn) {
      playBtn.classList.add('playing');
      playBtn.textContent = '⏸ Pause Guided Walk';
    }
    selectPlace(currentPlace, { zoom: true });
    tourTimer = setInterval(() => {
      const nextIdx = (currentPlace + 1) % PLACES.length;
      selectPlace(nextIdx, { zoom: true });
    }, 4400);
  }

  pins.forEach((pin, idx) => {
    pin.addEventListener('click', () => {
      stopTour();
      selectPlace(idx, { zoom: true });
    });
    pin.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        stopTour();
        selectPlace(idx, { zoom: true });
      }
    });
  });

  camBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      stopTour();
      camBtns.forEach(b => b.classList.toggle('active', b === btn));
      const target = btn.dataset.cam.split(' ').map(Number);
      animateViewBox(target, 720);
      if (btn.dataset.theater === 'stkilda') {
        selectPlace(14, { zoom: false });
      }
    });
  });

  eraPills.forEach(pill => {
    pill.addEventListener('click', () => {
      stopTour();
      const filter = pill.dataset.eraFilter;
      eraPills.forEach(p => p.classList.toggle('active', p === pill));
      pins.forEach(pin => {
        const match = filter === 'all' || pin.dataset.era === filter;
        pin.classList.toggle('dimmed', !match);
      });
      if (filter === 'early') {
        animateViewBox([20, 90, 480, 380], 700);
        selectPlace(0, { zoom: false });
      } else if (filter === 'standedge') {
        animateViewBox([40, 60, 500, 350], 700);
        selectPlace(6, { zoom: false });
      } else if (filter === 'marsden') {
        animateViewBox([450, 45, 530, 340], 700);
        selectPlace(10, { zoom: false });
      } else if (filter === 'stkilda') {
        animateViewBox([525, 350, 465, 260], 700);
        selectPlace(14, { zoom: false });
      } else {
        animateViewBox([0, 0, 1000, 620], 700);
      }
    });
  });

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      stopTour();
      selectPlace(currentPlace - 1, { zoom: true });
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      stopTour();
      selectPlace(currentPlace + 1, { zoom: true });
    });
  }
  if (playBtn) {
    playBtn.addEventListener('click', toggleTour);
  }

  // Double-click anywhere on the map background to reset to full Pennine & St Kilda view
  atlasSvg.addEventListener('dblclick', e => {
    if (e.target.closest('.map-pin')) return;
    stopTour();
    animateViewBox([0, 0, 1000, 620], 650);
    camBtns.forEach((b, i) => b.classList.toggle('active', i === 0));
  });
}

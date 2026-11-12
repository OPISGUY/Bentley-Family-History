"""Interactive cartographic atlas of the 15 places where the Bentley family lived (1613–1998)."""

def render_map_atlas():
    return '''<section id="atlas-map" class="map-atlas-section" aria-label="Interactive historical map of the places of the Bentley family">
<div class="section-head map-head">
  <div>
    <p class="eyebrow">Interactive Cartographic Atlas · 15 Documented Places (1613–1998)</p>
    <h2>Walk the Landscapes of the Bentleys</h2>
  </div>
  <p>From the packhorse farms of Standedge and Diggle on the Yorkshire–Lancashire border, across the moor to the quarries and drowned mills of Binn in Marsden, and across the sea to Carlisle Street in St Kilda. Select any pin or play the guided tour.</p>
</div>

<div class="map-toolbar js-only" role="toolbar" aria-label="Map camera and era controls">
  <div class="map-cameras">
    <span class="toolbar-label">Camera view:</span>
    <button type="button" class="cam-btn active" data-cam="0 0 1000 620" data-theater="pennine">Full Pennine Crossing</button>
    <button type="button" class="cam-btn" data-cam="40 80 540 360" data-theater="pennine">Standedge &amp; Saddleworth Zoom</button>
    <button type="button" class="cam-btn" data-cam="450 50 530 350" data-theater="pennine">Marsden, Binn &amp; Butterley Zoom</button>
    <button type="button" class="cam-btn" data-cam="530 355 455 255" data-theater="stkilda">Carlisle Street, St Kilda (Australia)</button>
  </div>
  <div class="map-eras">
    <span class="toolbar-label">Filter era:</span>
    <button type="button" class="era-pill active" data-era-filter="all">All 15 Places</button>
    <button type="button" class="era-pill" data-era-filter="early">1613–1764 · Early Saddleworth</button>
    <button type="button" class="era-pill" data-era-filter="standedge">1722–1835 · Standedge Clothiers</button>
    <button type="button" class="era-pill" data-era-filter="marsden">1851–1998 · Marsden &amp; Binn</button>
    <button type="button" class="era-pill" data-era-filter="stkilda">1854–1950 · St Kilda</button>
  </div>
</div>

<div class="map-stage">
  <div class="map-canvas-wrap">
    <div class="map-hud-top">
      <span class="hud-compass" aria-hidden="true">N ↑ · Pennine Watershed (1,500 ft) &amp; St Kilda Inset</span>
      <span class="hud-scale" aria-hidden="true">Scale: 1822 Saddleworth Survey &amp; 1890 OS Sheet CCLIX.11</span>
    </div>
    <svg id="bentley-atlas-svg" viewBox="0 0 1000 620" role="img" aria-label="Historical map of Saddleworth, Standedge, Marsden and St Kilda with 15 interactive family pins">
      <defs>
        <linearGradient id="atlas-parchment" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#f3ebd9"/>
          <stop offset="50%" stop-color="#e9dec6"/>
          <stop offset="100%" stop-color="#dfd1b4"/>
        </linearGradient>
        <radialGradient id="atlas-ridge-glow" cx="0.48" cy="0.38" r="0.42">
          <stop offset="0%" stop-color="#b69d74" stop-opacity="0.42"/>
          <stop offset="65%" stop-color="#8b7350" stop-opacity="0.15"/>
          <stop offset="100%" stop-color="#8b7350" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="atlas-water" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#35657d"/>
          <stop offset="100%" stop-color="#5d8ea3"/>
        </linearGradient>
        <linearGradient id="atlas-bay" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#27536b"/>
          <stop offset="100%" stop-color="#4e8099"/>
        </linearGradient>
        <filter id="pin-shadow" x="-30%" y="-30%" width="160%" height="160%">
          <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#101d28" flood-opacity="0.45"/>
        </filter>
      </defs>

      <!-- Base Parchment & Graticule Grid -->
      <rect width="1000" height="620" fill="url(#atlas-parchment)"/>
      <g class="map-grid" stroke="#cbbda0" stroke-width="0.6" opacity="0.55">
        <line x1="0" y1="100" x2="1000" y2="100"/><line x1="0" y1="200" x2="1000" y2="200"/>
        <line x1="0" y1="300" x2="1000" y2="300"/><line x1="0" y1="400" x2="1000" y2="400"/>
        <line x1="0" y1="500" x2="1000" y2="500"/>
        <line x1="150" y1="0" x2="150" y2="620"/><line x1="300" y1="0" x2="300" y2="620"/>
        <line x1="450" y1="0" x2="450" y2="620"/><line x1="600" y1="0" x2="600" y2="620"/>
        <line x1="750" y1="0" x2="750" y2="620"/><line x1="900" y1="0" x2="900" y2="620"/>
      </g>

      <!-- Topographic Elevation Contours & Standedge / Wessenden Moor Relief -->
      <ellipse cx="455" cy="245" rx="340" ry="195" fill="url(#atlas-ridge-glow)"/>
      <g fill="none" stroke="#b5a382" stroke-width="1.1" stroke-dasharray="6,4" opacity="0.7">
        <!-- 1,000 ft contour -->
        <path d="M120 85 Q280 40 465 65 T820 95 Q880 185 830 295 T480 390 Q240 420 115 330 Z"/>
        <!-- 1,250 ft Standedge & Pule Hill contour -->
        <path d="M210 115 Q350 75 475 95 T720 135 Q760 210 695 275 T460 335 Q285 350 205 265 Z"/>
        <!-- 1,450 ft High Escarpment (Standedge / Millstone Edge / Binn Moor) -->
        <path d="M315 135 Q415 105 495 125 T615 180 Q630 235 555 265 T365 280 Q295 235 315 135 Z" fill="#cbb997" fill-opacity="0.28"/>
      </g>

      <!-- County / Parish Watershed Boundary (Yorkshire / Saddleworth–Marsden Ridge) -->
      <path d="M395 20 Q435 125 452 215 T430 395 L410 595" fill="none" stroke="#7d5a38" stroke-width="2" stroke-dasharray="10,6" opacity="0.65"/>
      <text x="442" y="42" font-family="Georgia, serif" font-size="11" font-style="italic" fill="#6b4c2b">← Saddleworth (Rochdale Parish) &nbsp;|&nbsp; Standedge Watershed (1,490 ft) &nbsp;|&nbsp; Marsden (Almondbury / Colne Valley) →</text>

      <!-- Waterways: Diggle Brook, River Tame, Burk Clough, River Colne & Wessenden Brook -->
      <g fill="none" stroke="#49788f" stroke-linecap="round">
        <!-- Diggle Brook & River Tame (West) -->
        <path d="M355 225 Q285 265 235 310 T135 435 L75 535" stroke-width="3" opacity="0.75"/>
        <!-- Burk Clough dropping past Standedge Foot & Bentleys -->
        <path d="M385 180 Q335 198 295 225 T235 310" stroke-width="2" opacity="0.7"/>
        <!-- River Colne & Wessenden Brook (East) -->
        <path d="M525 275 Q625 245 685 198 T845 115 L955 75" stroke-width="3.2" opacity="0.8"/>
        <path d="M645 315 Q670 265 685 198" stroke-width="2.2" opacity="0.75"/>
      </g>

      <!-- Butterley Reservoir (1891–1907) with Drowned Mill Marker -->
      <g class="water-body">
        <path d="M648 192 Q695 182 742 195 L734 222 Q690 230 652 216 Z" fill="url(#atlas-water)" stroke="#274c5e" stroke-width="1.3"/>
        <path d="M662 204 L725 204" stroke="#b8d8e6" stroke-width="1" stroke-dasharray="3,3" opacity="0.8"/>
        <text x="695" y="240" text-anchor="middle" font-family="Georgia, serif" font-size="10.5" font-style="italic" fill="#234859">Butterley Reservoir (1891)</text>
      </g>

      <!-- Historic Packhorse & Turnpike Roads (Animated Paths) -->
      <!-- 1. Stanedge Turnpike & Packhorse Trail across the Pennines -->
      <path id="trail-pennine" class="map-trail" d="M125 425 Q185 355 245 265 T345 198 Q405 182 485 168 T615 162 Q695 178 785 135 L885 95" fill="none" stroke="#9e5a26" stroke-width="3.2" stroke-dasharray="7,5" opacity="0.8"/>
      <!-- 2. Northern Saddleworth Spur (Woodmans, Heyhouse, Knowl, Deanhead, Acre) -->
      <path id="trail-saddleworth" class="map-trail" d="M145 245 Q195 175 265 135 T338 228 L295 295" fill="none" stroke="#8c5830" stroke-width="2.2" stroke-dasharray="4,4" opacity="0.7"/>
      <!-- 3. Binn Road & Wessenden Reservoir Road (Widened 1870) -->
      <path id="trail-marsden" class="map-trail" d="M615 162 Q655 205 682 252 T785 135" fill="none" stroke="#8c5830" stroke-width="2.4" stroke-dasharray="5,4" opacity="0.75"/>

      <!-- Active Connection Highlight Line (dynamically updated by JS) -->
      <line id="active-hop-line" x1="125" y1="425" x2="295" y2="295" stroke="#d4882a" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="8,6" opacity="0"/>

      <!-- Region Watermark Labels -->
      <g font-family="Georgia, serif" fill="#5e4d36" opacity="0.55" pointer-events="none">
        <text x="72" y="88" font-size="20" font-weight="bold" letter-spacing="2">SADDLEWORTH</text>
        <text x="72" y="106" font-size="11" letter-spacing="1">ANCIENT CHAPELRY OF ROCHDALE · 1613–1835</text>
        <text x="385" y="108" font-size="14" font-weight="bold" letter-spacing="1.5" text-anchor="middle">STANDEDGE ESCARPMENT</text>
        <text x="695" y="68" font-size="20" font-weight="bold" letter-spacing="2">MARSDEN &amp; COLNE VALLEY</text>
        <text x="695" y="86" font-size="11" letter-spacing="1">CARR CLOUGH, BINN &amp; SLAITHWAITE · 1851–1998</text>
      </g>

      <!-- ================================================================= -->
      <!-- INSET THEATER: CARLISLE STREET, ST KILDA, MELBOURNE (1854–1950)   -->
      <!-- ================================================================= -->
      <g id="stkilda-inset" transform="translate(535, 360)">
        <rect x="0" y="0" width="445" height="242" rx="8" fill="#f7f1e3" stroke="#7d5a38" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <!-- Port Phillip Bay Coastline (Left of St Kilda) -->
        <path d="M0 0 L92 0 Q108 65 96 135 T114 242 L0 242 Z" fill="url(#atlas-bay)"/>
        <path d="M84 0 Q100 65 88 135 T106 242" fill="none" stroke="#bfe0ee" stroke-width="1.5" stroke-dasharray="4,3"/>
        <text x="44" y="118" text-anchor="middle" font-family="Georgia, serif" font-size="11" font-style="italic" fill="#e9f6fc" transform="rotate(-90 44 118)">Port Phillip Bay · St Kilda Foreshore</text>

        <!-- Inset Header -->
        <rect x="92" y="0" width="353" height="32" rx="0" fill="#1b3244"/>
        <text x="106" y="20" font-family="Georgia, serif" font-size="12.5" font-weight="bold" fill="#fff8eb">III. Australian Emigration Inset · Carlisle Street, St Kilda (1854–1950)</text>

        <!-- St Kilda Street Grid & Carlisle Street Corridor -->
        <g stroke="#d1c4ab" stroke-width="1" fill="none">
          <line x1="105" y1="75" x2="430" y2="75"/>
          <line x1="105" y1="195" x2="430" y2="195"/>
          <line x1="165" y1="35" x2="165" y2="235"/>
          <line x1="275" y1="35" x2="275" y2="235"/>
          <line x1="385" y1="35" x2="385" y2="235"/>
        </g>
        <!-- Carlisle Street Main Thoroughfare -->
        <path d="M100 138 L435 138" stroke="#c89b5c" stroke-width="12" opacity="0.35"/>
        <path d="M100 138 L435 138" stroke="#8f5424" stroke-width="2" stroke-dasharray="6,4"/>
        <text x="268" y="158" text-anchor="middle" font-family="Georgia, serif" font-size="11.5" font-weight="bold" fill="#593a1e" letter-spacing="1.2">CARLISLE STREET, ST KILDA</text>

        <!-- Architectural Mini-Cards for the Three Brothers' Houses -->
        <!-- House 1: 62 Carlisle Street (William & Hannah, John William) -->
        <g transform="translate(132, 82)">
          <rect x="0" y="0" width="92" height="42" rx="3" fill="#fffdf8" stroke="#8f5424" stroke-width="1.4"/>
          <text x="46" y="15" text-anchor="middle" font-family="Georgia, serif" font-size="10.5" font-weight="bold" fill="#1a2632">62 Carlisle St</text>
          <text x="46" y="27" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#52606d">William &amp; Hannah</text>
          <text x="46" y="37" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8.5" fill="#8f5424">1891 · 1901 · 1950</text>
        </g>
        <!-- House 2: "Stockwell", Carlisle Street (Wright & Helen) -->
        <g transform="translate(234, 82)">
          <rect x="0" y="0" width="92" height="42" rx="3" fill="#fffdf8" stroke="#8f5424" stroke-width="1.4"/>
          <text x="46" y="15" text-anchor="middle" font-family="Georgia, serif" font-size="10.5" font-weight="bold" fill="#1a2632">“Stockwell”</text>
          <text x="46" y="27" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#52606d">Wright &amp; Helen</text>
          <text x="46" y="37" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8.5" fill="#8f5424">d. 27 July 1902</text>
        </g>
        <!-- House 3: "Baroona", 66 Carlisle Street (Joseph & Ann) -->
        <g transform="translate(336, 82)">
          <rect x="0" y="0" width="94" height="42" rx="3" fill="#fffdf8" stroke="#8f5424" stroke-width="1.4"/>
          <text x="47" y="15" text-anchor="middle" font-family="Georgia, serif" font-size="10.5" font-weight="bold" fill="#1a2632">“Baroona” No. 66</text>
          <text x="47" y="27" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#52606d">Joseph &amp; Ann</text>
          <text x="47" y="37" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8.5" fill="#8f5424">1907 &amp; Nov 1915</text>
        </g>
        <text x="272" y="222" text-anchor="middle" font-family="Georgia, serif" font-size="10.5" fill="#465461">Three sons of William &amp; Betty of Standage living within doors of one another in Victoria</text>
      </g>

      <!-- ================================================================= -->
      <!-- 15 INTERACTIVE LANDMARK PINS                                      -->
      <!-- ================================================================= -->
      <!-- Pin 1: St Chad's Church, Saddleworth (1613–1835) -->
      <g class="map-pin active" id="place-pin-1" data-place="0" data-era="early" transform="translate(125, 425)" tabindex="0" role="button" aria-label="1. St Chad's Church, Saddleworth (1613–1835)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#1b3548" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">1</text>
        <text class="pin-label" x="0" y="27" text-anchor="middle">St Chad’s (1613)</text>
      </g>

      <!-- Pin 2: Diggle & Fairbanks (1654–1764) -->
      <g class="map-pin" id="place-pin-2" data-place="1" data-era="early" transform="translate(295, 295)" tabindex="0" role="button" aria-label="2. Diggle & Fairbanks (1654–1764)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#1b3548" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">2</text>
        <text class="pin-label" x="0" y="27" text-anchor="middle">Diggle &amp; Fairbanks</text>
      </g>

      <!-- Pin 3: Stone-edge / High Standedge (1686–1792) -->
      <g class="map-pin" id="place-pin-3" data-place="2" data-era="early" transform="translate(385, 195)" tabindex="0" role="button" aria-label="3. Stone-edge / Standedge (1686–1792)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#8f5122" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">3</text>
        <text class="pin-label" x="0" y="-19" text-anchor="middle">Stone-edge (1686)</text>
      </g>

      <!-- Pin 4: Deanhead & Acre (1722–1750) -->
      <g class="map-pin" id="place-pin-4" data-place="3" data-era="standedge" transform="translate(255, 138)" tabindex="0" role="button" aria-label="4. Deanhead & Acre (1722–1750)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#8f5122" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">4</text>
        <text class="pin-label" x="0" y="-19" text-anchor="middle">Deanhead &amp; Acre</text>
      </g>

      <!-- Pin 5: Knowl (Knowle Farm) & Knar (1723/4–1744) -->
      <g class="map-pin" id="place-pin-5" data-place="4" data-era="standedge" transform="translate(225, 295)" tabindex="0" role="button" aria-label="5. Knowl & Knar (1723/4–1744)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#8f5122" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">5</text>
        <text class="pin-label" x="-6" y="27" text-anchor="end">Knowl &amp; Knar</text>
      </g>

      <!-- Pin 6: Heyhouse, Whams Inn & Ogden (1752–1833) -->
      <g class="map-pin" id="place-pin-6" data-place="5" data-era="standedge" transform="translate(155, 165)" tabindex="0" role="button" aria-label="6. Heyhouse, Whams Inn & Ogden (1752–1833)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#8f5122" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">6</text>
        <text class="pin-label" x="0" y="-19" text-anchor="middle">Heyhouse &amp; Whams</text>
      </g>

      <!-- Pin 7: "Bentleys" at Rough & Standedge Foot (1680–1822) -->
      <g class="map-pin" id="place-pin-7" data-place="6" data-era="standedge" transform="translate(338, 228)" tabindex="0" role="button" aria-label="7. Bentleys at Rough & Standedge Foot (1791–1822)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#8f5122" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">7</text>
        <text class="pin-label" x="0" y="27" text-anchor="middle">“Bentleys” &amp; Standedge Foot</text>
      </g>

      <!-- Pin 8: Bleak Hey Nook — Bentley Farmhouse (1791–1806) -->
      <g class="map-pin" id="place-pin-8" data-place="7" data-era="standedge" transform="translate(262, 232)" tabindex="0" role="button" aria-label="8. Bleak Hey Nook — Bentley Farmhouse (1791–1806)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#8f5122" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">8</text>
        <text class="pin-label" x="-14" y="4" text-anchor="end">Bleak Hey Nook</text>
      </g>

      <!-- Pin 9: Woodmans, near Delph (1784–1791) -->
      <g class="map-pin" id="place-pin-9" data-place="8" data-era="standedge" transform="translate(145, 255)" tabindex="0" role="button" aria-label="9. Woodmans, near Delph (1784–1791)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#8f5122" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">9</text>
        <text class="pin-label" x="0" y="27" text-anchor="middle">Woodmans (1791)</text>
      </g>

      <!-- Pin 10: Coat Hill & Ridge (1831–1835) -->
      <g class="map-pin" id="place-pin-10" data-place="9" data-era="standedge" transform="translate(215, 358)" tabindex="0" role="button" aria-label="10. Coat Hill & Ridge (1831–1835)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#8f5122" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">10</text>
        <text class="pin-label" x="0" y="27" text-anchor="middle">Coat Hill &amp; Ridge</text>
      </g>

      <!-- Pin 11: Carr Clough & Clough Lee Mills, Marsden (1851–1861) -->
      <g class="map-pin" id="place-pin-11" data-place="10" data-era="marsden" transform="translate(565, 165)" tabindex="0" role="button" aria-label="11. Carr Clough & Clough Lee Mills, Marsden (1851–1861)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#234b3c" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">11</text>
        <text class="pin-label" x="0" y="-19" text-anchor="middle">Carr Clough (1851)</text>
      </g>

      <!-- Pin 12: Binn, Lane Syke Quarry & Binn Lodge Farm (1871–1965) -->
      <g class="map-pin" id="place-pin-12" data-place="11" data-era="marsden" transform="translate(682, 268)" tabindex="0" role="button" aria-label="12. Binn, Lane Syke Quarry & Binn Road (1871–1965)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#234b3c" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">12</text>
        <text class="pin-label" x="0" y="27" text-anchor="middle">Binn &amp; Quarry (1871)</text>
      </g>

      <!-- Pin 13: Butterley Reservoir, Drowned "Th' Top Bonk" & Ottiwells Mill (1876–1913) -->
      <g class="map-pin" id="place-pin-13" data-place="12" data-era="marsden" transform="translate(695, 198)" tabindex="0" role="button" aria-label="13. Butterley Reservoir, Upper Bank Bottom Mill & Ottiwells (1876–1913)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#234b3c" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">13</text>
        <text class="pin-label" x="0" y="-19" text-anchor="middle">Butterley &amp; Mills</text>
      </g>

      <!-- Pin 14: St Bartholomew's Marsden, Slaithwaite & Huddersfield (1918–1998) -->
      <g class="map-pin" id="place-pin-14" data-place="13" data-era="marsden" transform="translate(845, 118)" tabindex="0" role="button" aria-label="14. St Bartholomew's Marsden, Slaithwaite & Huddersfield (1918–1998)">
        <circle class="pin-pulse" r="20" fill="none" stroke="#c87d32" stroke-width="2"/>
        <circle class="pin-bg" r="13" fill="#234b3c" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">14</text>
        <text class="pin-label" x="0" y="-19" text-anchor="middle">Marsden Church &amp; Slaithwaite</text>
      </g>

      <!-- Pin 15: 62–66 Carlisle Street, St Kilda, Melbourne (1854–1950) -->
      <g class="map-pin" id="place-pin-15" data-place="14" data-era="stkilda" transform="translate(815, 498)" tabindex="0" role="button" aria-label="15. 62–66 Carlisle Street, St Kilda, Victoria (1854–1950)">
        <circle class="pin-pulse" r="22" fill="none" stroke="#c87d32" stroke-width="2.2"/>
        <circle class="pin-bg" r="14" fill="#7c3f23" stroke="#fffdf8" stroke-width="2.2" filter="url(#pin-shadow)"/>
        <text y="4" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#fffdf8">15</text>
        <text class="pin-label" x="0" y="29" text-anchor="middle">Carlisle St, St Kilda</text>
      </g>
    </svg>

    <!-- Guided Tour Scrubber Bar Below Map Canvas -->
    <div class="map-tour-bar js-only" aria-label="Guided chronological tour controls">
      <button type="button" id="map-prev" class="secondary">← Prev Place</button>
      <button type="button" id="map-play" class="tour-play-btn">▶ Auto-Walk All 15 Places</button>
      <button type="button" id="map-next" class="secondary">Next Place →</button>
      <div class="tour-progress-wrap" aria-hidden="true">
        <div id="tour-progress-bar" class="tour-progress-bar"></div>
      </div>
      <span id="tour-counter" class="tour-counter">Place 1 of 15</span>
    </div>
  </div>

  <!-- Right-Hand Interactive Place Dossier Panel -->
  <aside class="map-dossier" id="map-dossier-panel" aria-live="polite">
    <div class="dossier-ribbon">
      <span id="dossier-stop" class="dossier-stop">Place 1 of 15 · 1613–1835</span>
      <span id="dossier-grid" class="dossier-grid">St Chad’s, Uppermill · Saddleworth</span>
    </div>
    <h3 id="dossier-title">St Chad’s Church, Saddleworth</h3>
    <p id="dossier-who" class="dossier-who"><strong>Generations here:</strong> Mathew &amp; An (1613–14) · Jonas (1654–86) · Old Matthew &amp; Ellin (1700–35/6) · Helen (“Ellin”) Platt (1769 gravestone) · Brothers William &amp; James at the font (6 June 1819)</p>
    <p id="dossier-story" class="dossier-story">Founded in 1215 as a moorland chapelry of St Chad, Rochdale, this hillside church is the cradle of the surviving Bentley record. On 1 May 1613—on only the second surviving annual sheet of St Chad’s register—Mathew Bentley christened his daughter An here. Here “old Matthew” of Stone-edge was buried in February 1735/6, here Helen Platt’s 1769 gravestone still spells her name “Ellin”, and here on Sunday, 6 June 1819, brothers William and James Bentley of Standage stood side by side at the font to christen their sons William and Charles.</p>
    <div class="dossier-proof">
      <small>Primary Archival Evidence</small>
      <p id="dossier-evidence">St Chad’s Diocesan Transcripts (1613–14); Parish Registers (1632–1835); Ellin &amp; Thomas Platt Gravestone in the Old Churchyard (1769 / 1789, Kidd 1994, p. 4); Double Baptism of 6 June 1819.</p>
    </div>
    <div class="dossier-links">
      <a id="dossier-story-link" class="button" href="stories/mathew-and-his-daughter-an.html">Read this place’s story →</a>
      <a id="dossier-family-link" class="button secondary" href="#family-11">View household records ↓</a>
    </div>
    <div class="place-quick-list js-only" aria-label="Jump to any of the 15 places">
      <small>All 15 documented family places:</small>
      <div class="place-pills" id="place-pill-nav"></div>
    </div>
  </aside>
</div>
</section>'''

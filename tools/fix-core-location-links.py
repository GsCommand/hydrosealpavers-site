from pathlib import Path
import re

ROOT = Path('.')

JAX = [
    ('Jacksonville', '/service-areas/jacksonville'),
    ('Jacksonville Beach', '/service-areas/jacksonville/jacksonville-beach'),
    ('Mandarin', '/service-areas/jacksonville/mandarin'),
    ('Southside', '/service-areas/jacksonville/southside'),
]
STJ = [
    ('St. Johns County', '/service-areas/st-johns-county'),
    ('Durbin Crossing', '/service-areas/st-johns-county/durbin-crossing'),
    ('Fruit Cove', '/service-areas/st-johns-county/fruit-cove'),
    ('Julington Creek', '/service-areas/st-johns-county/julington-creek'),
    ('Nocatee', '/service-areas/st-johns-county/nocatee'),
    ('Ponte Vedra', '/service-areas/st-johns-county/ponte-vedra'),
    ('Ponte Vedra Beach', '/service-areas/st-johns-county/ponte-vedra-beach'),
    ('TrailMark', '/service-areas/st-johns-county/trailmark'),
]
CLAY = [
    ('Clay County', '/service-areas/clay-county'),
    ('Fleming Island', '/service-areas/clay-county/fleming-island'),
    ('Middleburg', '/service-areas/clay-county/middleburg'),
    ('Oakleaf Plantation', '/service-areas/clay-county/oakleaf-plantation'),
    ('Orange Park', '/service-areas/clay-county/orange-park'),
]
NASSAU = [('Yulee & Wildlight', '/service-areas/yulee')]
CORE = JAX + STJ + CLAY + NASSAU
CORE_PATHS = {path for _, path in CORE}

RETIRED_LABELS = [
    'Atlantic Beach', 'Bartram Park', 'Deerwood', 'eTown', 'Etown', 'Glen Kernan',
    'Neptune Beach', 'Ortega', 'Pablo Creek Reserve', 'Queens Harbour',
    'Riverside / Avondale', 'Riverside & Avondale', 'Riverside Avondale', 'Tamaya',
    'Beachwalk', 'Del Webb Ponte Vedra', 'Marsh Landing', 'Murabella', 'Palencia',
    'Palm Valley', 'RiverTown', 'Rivertown', 'Sawgrass', 'Shearwater', 'SilverLeaf',
    'Silverleaf', 'World Golf Village', 'Green Cove Springs', 'Wildlight',
]
RETIRED_PATHS = [
    '/service-areas/jacksonville/atlantic-beach',
    '/service-areas/jacksonville/bartram-park',
    '/service-areas/jacksonville/deerwood',
    '/service-areas/jacksonville/etown',
    '/service-areas/jacksonville/glen-kernan',
    '/service-areas/jacksonville/neptune-beach',
    '/service-areas/jacksonville/ortega',
    '/service-areas/jacksonville/pablo-creek-reserve',
    '/service-areas/jacksonville/queens-harbour',
    '/service-areas/jacksonville/riverside-avondale',
    '/service-areas/jacksonville/tamaya',
    '/service-areas/st-johns-county/beachwalk',
    '/service-areas/st-johns-county/del-webb-ponte-vedra',
    '/service-areas/st-johns-county/marsh-landing',
    '/service-areas/st-johns-county/murabella',
    '/service-areas/st-johns-county/palencia',
    '/service-areas/st-johns-county/palm-valley',
    '/service-areas/st-johns-county/rivertown',
    '/service-areas/st-johns-county/sawgrass',
    '/service-areas/st-johns-county/shearwater',
    '/service-areas/st-johns-county/silverleaf',
    '/service-areas/st-johns-county/world-golf-village',
    '/service-areas/clay-county/green-cove-springs',
    '/service-areas/wildlight',
]

SURVIVING_FILES = {
    'service-areas/jacksonville/index.html': JAX,
    'service-areas/jacksonville/jacksonville-beach.html': JAX,
    'service-areas/jacksonville/mandarin.html': JAX,
    'service-areas/jacksonville/southside.html': JAX,
    'service-areas/st-johns-county/index.html': STJ,
    'service-areas/st-johns-county/durbin-crossing.html': STJ,
    'service-areas/st-johns-county/fruit-cove.html': STJ,
    'service-areas/st-johns-county/julington-creek.html': STJ,
    'service-areas/st-johns-county/nocatee.html': STJ,
    'service-areas/st-johns-county/ponte-vedra.html': STJ,
    'service-areas/st-johns-county/ponte-vedra-beach.html': STJ,
    'service-areas/st-johns-county/trailmark.html': STJ,
    'service-areas/clay-county/index.html': CLAY,
    'service-areas/clay-county/fleming-island.html': CLAY,
    'service-areas/clay-county/middleburg.html': CLAY,
    'service-areas/clay-county/oakleaf-plantation.html': CLAY,
    'service-areas/clay-county/orange-park.html': CLAY,
    'service-areas/yulee.html': NASSAU,
}

PATH_BY_FILE = {
    'service-areas/jacksonville/index.html': '/service-areas/jacksonville',
    'service-areas/jacksonville/jacksonville-beach.html': '/service-areas/jacksonville/jacksonville-beach',
    'service-areas/jacksonville/mandarin.html': '/service-areas/jacksonville/mandarin',
    'service-areas/jacksonville/southside.html': '/service-areas/jacksonville/southside',
    'service-areas/st-johns-county/index.html': '/service-areas/st-johns-county',
    'service-areas/st-johns-county/durbin-crossing.html': '/service-areas/st-johns-county/durbin-crossing',
    'service-areas/st-johns-county/fruit-cove.html': '/service-areas/st-johns-county/fruit-cove',
    'service-areas/st-johns-county/julington-creek.html': '/service-areas/st-johns-county/julington-creek',
    'service-areas/st-johns-county/nocatee.html': '/service-areas/st-johns-county/nocatee',
    'service-areas/st-johns-county/ponte-vedra.html': '/service-areas/st-johns-county/ponte-vedra',
    'service-areas/st-johns-county/ponte-vedra-beach.html': '/service-areas/st-johns-county/ponte-vedra-beach',
    'service-areas/st-johns-county/trailmark.html': '/service-areas/st-johns-county/trailmark',
    'service-areas/clay-county/index.html': '/service-areas/clay-county',
    'service-areas/clay-county/fleming-island.html': '/service-areas/clay-county/fleming-island',
    'service-areas/clay-county/middleburg.html': '/service-areas/clay-county/middleburg',
    'service-areas/clay-county/oakleaf-plantation.html': '/service-areas/clay-county/oakleaf-plantation',
    'service-areas/clay-county/orange-park.html': '/service-areas/clay-county/orange-park',
    'service-areas/yulee.html': '/service-areas/yulee',
}


def replace_once(text, pattern, repl, label, flags=re.S):
    new, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 replacement, got {count}')
    return new


def card(href, title, description, extra=''):
    cls = f'card service-card {extra}'.strip()
    return f'''        <a class="{cls}" href="{href}">
          <h3>{title}</h3>
          <p>{description}</p>
          <strong>View {title} <span class="arrow" aria-hidden="true">→</span></strong>
        </a>'''


def link_list(items, current):
    rows = []
    for name, href in items:
        if href == current:
            continue
        label = name.replace('Yulee & Wildlight', 'Yulee &amp; Wildlight')
        rows.append(f'              <li><a href="{href}">{label} Paver Sealing</a></li>')
    return '\n'.join(rows)


def nearby_section(items, current, heading='Nearby Core Service Areas'):
    rows = link_list(items, current)
    return f'''
<section class="section hs-core-nearby-links" aria-label="Nearby core service areas">
  <div class="container">
    <div class="card">
      <h2 style="margin-top:0;">{heading}</h2>
      <p class="muted">Explore HydroSeal's dedicated local paver sealing pages. Smaller nearby communities are covered through these primary market pages so each location has a clearer, stronger local resource.</p>
      <ul style="columns:2;column-gap:28px;margin:14px 0 0;padding-left:20px;">
{rows}
      </ul>
    </div>
  </div>
</section>
'''

# 1) Replace the three county hub card groups with only real surviving child pages.
jax_path = ROOT / 'service-areas/jacksonville/index.html'
s = jax_path.read_text(encoding='utf-8')
jax_cards = '\n\n'.join([
    card('/service-areas/jacksonville/jacksonville-beach', 'Jacksonville Beach', 'Core Beaches page covering Jacksonville Beach plus Atlantic Beach and Neptune Beach.', 'featured-card'),
    card('/service-areas/jacksonville/mandarin', 'Mandarin', 'Dedicated Mandarin page for shaded driveways, patios, walkways and pool-deck pavers.', 'featured-card'),
    card('/service-areas/jacksonville/southside', 'Southside', 'Core Southside page covering Deerwood, eTown, Glen Kernan, Pablo Creek Reserve and Tamaya.', 'featured-card'),
])
jax_section = f'''<!-- COUNTY LINKS -->
<section class="section" id="county-links-duval">
  <div class="container">
    <h2 class="section-title">Core Jacksonville Paver Sealing Areas</h2>
    <p class="section-sub">These are HydroSeal's dedicated Jacksonville location pages. Smaller Duval communities are covered inside the closest core market instead of being split into thin standalone pages.</p>
    <div class="county-area-group" style="margin-top:16px;">
      <h3 class="county-area-heading">Dedicated Jacksonville Pages</h3>
      <div class="county-area-grid">
{jax_cards}
      </div>
    </div>
    <div class="card" style="margin-top:18px;padding:20px 22px;">
      <h3 class="county-area-heading" style="margin-top:0;">Also serving neighborhoods across Jacksonville</h3>
      <p style="margin:10px 0 0;">HydroSeal also serves Atlantic Beach, Neptune Beach, Bartram Park, Deerwood, eTown, Glen Kernan, Ortega, Pablo Creek Reserve, Queens Harbour, Riverside/Avondale, Tamaya and other selected Jacksonville communities through the closest dedicated page above.</p>
    </div>
  </div>
</section>'''
s = replace_once(s, r'<!-- COUNTY LINKS -->\s*<section class="section" id="county-links-duval">.*?</section>', jax_section, 'Jacksonville county links')
jax_path.write_text(s, encoding='utf-8')

stj_path = ROOT / 'service-areas/st-johns-county/index.html'
s = stj_path.read_text(encoding='utf-8')
stj_cards = '\n\n'.join([
    card('/service-areas/st-johns-county/nocatee', 'Nocatee', 'Dedicated Nocatee driveway, patio and pool-deck paver sealing page.'),
    card('/service-areas/st-johns-county/ponte-vedra', 'Ponte Vedra', 'Dedicated Ponte Vedra paver and travertine sealing page.'),
    card('/service-areas/st-johns-county/ponte-vedra-beach', 'Ponte Vedra Beach', 'Coastal paver sealing page covering the beach corridor and nearby coastal communities.'),
    card('/service-areas/st-johns-county/julington-creek', 'Julington Creek', 'Dedicated Julington Creek page with established Google visibility.'),
    card('/service-areas/st-johns-county/fruit-cove', 'Fruit Cove', 'Dedicated Fruit Cove paver restoration and sealing page.'),
    card('/service-areas/st-johns-county/durbin-crossing', 'Durbin Crossing', 'Dedicated Durbin Crossing driveway and patio sealing page.'),
    card('/service-areas/st-johns-county/trailmark', 'TrailMark', 'Dedicated TrailMark page restored to preserve prior Google visibility.'),
])
stj_section = f'''<!-- COUNTY LINKS -->
    <section class="section" id="county-links">
      <div class="container">
        <h2 class="section-title">Core St. Johns County Paver Sealing Areas</h2>
        <p class="section-sub">These are HydroSeal's dedicated St. Johns County location pages. Nearby master-planned communities are covered inside the closest core market page.</p>
        <div class="county-area-group" style="margin-top:16px;">
          <h3 class="county-area-heading">Dedicated St. Johns County Pages</h3>
          <div class="county-area-grid">
{stj_cards}
          </div>
        </div>
        <div class="card" style="margin-top:18px;padding:20px 22px;">
          <h3 class="county-area-heading" style="margin-top:0;">Also serving communities throughout St. Johns County</h3>
          <p style="margin:10px 0 0;">Beachwalk, Del Webb Ponte Vedra, Marsh Landing, Murabella, Palencia, Palm Valley, RiverTown, Sawgrass, Shearwater, SilverLeaf and World Golf Village are served through the closest dedicated location page above.</p>
        </div>
      </div>
    </section>'''
s = replace_once(s, r'<!-- COUNTY LINKS -->\s*<section class="section" id="county-links">.*?</section>', stj_section, 'St Johns county links')
stj_path.write_text(s, encoding='utf-8')

clay_path = ROOT / 'service-areas/clay-county/index.html'
s = clay_path.read_text(encoding='utf-8')
clay_cards = '\n\n'.join([
    card('/service-areas/clay-county/fleming-island', 'Fleming Island', 'Dedicated Fleming Island page for moisture, irrigation and waterfront-adjacent conditions.'),
    card('/service-areas/clay-county/oakleaf-plantation', 'Oakleaf Plantation', 'Dedicated Oakleaf page for busy driveways, joint washout and community hardscapes.'),
    card('/service-areas/clay-county/orange-park', 'Orange Park', 'Dedicated Orange Park page for established homes, shade and organic staining.'),
    card('/service-areas/clay-county/middleburg', 'Middleburg', 'Dedicated Middleburg page with existing Google Search visibility.'),
])
clay_section = f'''<!-- COUNTY LINKS (focused core pages) -->
  <section class="section" id="county-links-clay">
    <div class="container">
      <h2 class="section-title">Core Clay County Paver Sealing Areas</h2>
      <p class="section-sub">These are HydroSeal's dedicated Clay County location pages. Green Cove Springs and nearby communities are covered through the Clay County hub rather than a separate thin page.</p>
      <div class="clay-tier-grid">
{clay_cards}
      </div>
      <div class="card" style="margin-top:18px;padding:20px 22px;">
        <h3 style="margin-top:0;">Also serving Green Cove Springs and surrounding Clay County</h3>
        <p style="margin:10px 0 0;">Green Cove Springs remains part of HydroSeal's Clay County service coverage and is represented by this county hub.</p>
      </div>
    </div>
  </section>'''
s = replace_once(s, r'<!-- COUNTY LINKS \(soft orange → white gradient cards\) -->\s*<section class="section" id="county-links-clay">.*?</section>', clay_section, 'Clay county links')
clay_path.write_text(s, encoding='utf-8')

# 2) Rebuild the main service-area hub around the 18 dedicated market URLs (plus the hub itself).
main_path = ROOT / 'service-areas/index.html'
s = main_path.read_text(encoding='utf-8')
s = s.replace('.community-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:32px}', '.community-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin-top:32px}')
# Add Yulee as a top market card if not already present there.
if '<h3>Yulee &amp; Wildlight</h3>' not in s.split('Popular local pages', 1)[0]:
    marker = '        </div>\n      </div>\n    </section>\n\n    <section class="service-hub-section alt">\n      <div class="service-hub-wrap">\n        <p class="service-hub-kicker">Popular local pages</p>'
    yulee_card = '''          <a class="county-card" href="/service-areas/yulee">
            <div class="county-card__media"><img src="/assets/hero/hydroseal-driveway.webp" alt="Yulee and Wildlight paver sealing service area" loading="lazy" decoding="async" /></div>
            <div class="county-card__body">
              <h3>Yulee &amp; Wildlight</h3>
              <p>Dedicated Nassau County coverage for Yulee and Wildlight driveways, patios, pool decks and walkways.</p>
              <span class="county-card__link">Explore Yulee &amp; Wildlight →</span>
            </div>
          </a>
'''
    replacement = yulee_card + '        </div>\n      </div>\n    </section>\n\n    <section class="service-hub-section alt">\n      <div class="service-hub-wrap">\n        <p class="service-hub-kicker">Popular local pages</p>'
    if marker not in s:
        raise SystemExit('Main service hub county-card insertion marker not found')
    s = s.replace(marker, replacement, 1)

main_groups = '''    <section class="service-hub-section alt">
      <div class="service-hub-wrap">
        <p class="service-hub-kicker">Dedicated local pages</p>
        <h2>Go directly to a HydroSeal core service area</h2>
        <p>These are the location pages HydroSeal is actively building and maintaining. Smaller neighborhoods are covered inside the closest core page instead of being split across dozens of overlapping URLs.</p>
        <div class="community-grid">
          <div class="community-group">
            <h3>Jacksonville</h3>
            <a href="/service-areas/jacksonville">Jacksonville</a>
            <a href="/service-areas/jacksonville/jacksonville-beach">Jacksonville Beach</a>
            <a href="/service-areas/jacksonville/mandarin">Mandarin</a>
            <a href="/service-areas/jacksonville/southside">Southside</a>
          </div>
          <div class="community-group">
            <h3>St. Johns County</h3>
            <a href="/service-areas/st-johns-county">St. Johns County</a>
            <a href="/service-areas/st-johns-county/durbin-crossing">Durbin Crossing</a>
            <a href="/service-areas/st-johns-county/fruit-cove">Fruit Cove</a>
            <a href="/service-areas/st-johns-county/julington-creek">Julington Creek</a>
            <a href="/service-areas/st-johns-county/nocatee">Nocatee</a>
            <a href="/service-areas/st-johns-county/ponte-vedra">Ponte Vedra</a>
            <a href="/service-areas/st-johns-county/ponte-vedra-beach">Ponte Vedra Beach</a>
            <a href="/service-areas/st-johns-county/trailmark">TrailMark</a>
          </div>
          <div class="community-group">
            <h3>Clay County</h3>
            <a href="/service-areas/clay-county">Clay County</a>
            <a href="/service-areas/clay-county/fleming-island">Fleming Island</a>
            <a href="/service-areas/clay-county/middleburg">Middleburg</a>
            <a href="/service-areas/clay-county/oakleaf-plantation">Oakleaf Plantation</a>
            <a href="/service-areas/clay-county/orange-park">Orange Park</a>
          </div>
          <div class="community-group">
            <h3>Nassau County</h3>
            <a href="/service-areas/yulee">Yulee &amp; Wildlight</a>
          </div>
        </div>
      </div>
    </section>'''
s = replace_once(s, r'<section class="service-hub-section alt">\s*<div class="service-hub-wrap">\s*<p class="service-hub-kicker">Popular local pages</p>.*?</section>', main_groups, 'Main service hub popular links')
s = re.sub(r'\s*<!-- hs-core-location-hub:start -->.*?<!-- hs-core-location-hub:end -->\s*', '\n', s, count=1, flags=re.S)
s = s.replace('St. Johns County, Clay County and nearby areas.', 'St. Johns County, Clay County, Yulee and nearby areas.')
# Collection schema: add Yulee as a fourth primary service market.
needle = '{"@type":"ListItem","position":3,"name":"Clay County","url":"https://hydrosealpavers.com/service-areas/clay-county"}'
if needle in s and '"position":4,"name":"Yulee' not in s:
    s = s.replace(needle, needle + ',\n          {"@type":"ListItem","position":4,"name":"Yulee & Wildlight","url":"https://hydrosealpavers.com/service-areas/yulee"}', 1)
main_path.write_text(s, encoding='utf-8')

# 3) Standardize the nearby-location column on every surviving location page.
for filename, cluster in SURVIVING_FILES.items():
    p = ROOT / filename
    text = p.read_text(encoding='utf-8')
    current = PATH_BY_FILE[filename]
    rows = link_list(cluster, current)
    pattern = r'(<div class="related-links-column">\s*<h3>Nearby Areas We Serve</h3>\s*<ul>).*?(</ul>)'
    repl = r'\1\n' + rows + r'\n            \2'
    text, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count == 0:
        # TrailMark and Yulee use simpler layouts; add a clean core-links box.
        heading = 'Nearby St. Johns County Service Areas' if cluster is STJ else ('Nearby Northeast Florida Service Areas' if cluster is NASSAU else 'Nearby Core Service Areas')
        insert = nearby_section(STJ if cluster is STJ else (JAX[:1] + STJ[:1] + CLAY[:1] if cluster is NASSAU else cluster), current, heading)
        if '</main>' not in text:
            raise SystemExit(f'{filename}: no related-links block and no </main> marker')
        text = text.replace('</main>', insert + '\n</main>', 1)
    p.write_text(text, encoding='utf-8')

# 4) Add Yulee to Service Areas navigation/footer wherever those sitewide components appear.
def add_yulee_nav(text):
    # Modern mega menu (inline or partial).
    def modern(m):
        inner = m.group(2)
        if '/service-areas/yulee' not in inner:
            inner = inner.rstrip() + '\n          <a href="/service-areas/yulee">Yulee</a>\n        '
        return m.group(1) + inner + m.group(3)
    text = re.sub(r'(<div class="hs-modern-mega hs-modern-areas-menu">)(.*?)(</div>)', modern, text, flags=re.S)
    # Legacy dropdown used on sitemap and some older pages.
    def legacy(m):
        inner = m.group(2)
        if '/service-areas/yulee' not in inner:
            inner = inner.rstrip() + '\n                <a role="menuitem" href="/service-areas/yulee">Yulee</a>\n              '
        return m.group(1) + inner + m.group(3)
    text = re.sub(r'(<div class="dropdown" role="menu" aria-label="Service Areas">)(.*?)(</div>)', legacy, text, flags=re.S)
    # Footer Service Areas group.
    def footer(m):
        inner = m.group(2)
        if '/service-areas/yulee' not in inner:
            inner = inner.rstrip() + '<a href="/service-areas/yulee">Yulee</a>'
        return m.group(1) + inner + m.group(3)
    text = re.sub(r'(<div class="footer-title">Service Areas</div>\s*<div class="footer-links">)(.*?)(</div>)', footer, text, flags=re.S)
    return text

for p in ROOT.rglob('*.html'):
    text = p.read_text(encoding='utf-8')
    new = add_yulee_nav(text)
    if new != text:
        p.write_text(new, encoding='utf-8')
for rel in ['partials/header.html', 'partials/footer.html']:
    p = ROOT / rel
    text = p.read_text(encoding='utf-8')
    new = add_yulee_nav(text)
    if new != text:
        p.write_text(new, encoding='utf-8')

# 5) Rebuild the visible HTML sitemap service-area sections with only dedicated URLs.
sitemap = ROOT / 'sitemap.html'
s = sitemap.read_text(encoding='utf-8')
def sitemap_section(title, items):
    rows = '\n'.join(f'          <li><a href="{href}">{name}</a></li>' for name, href in items)
    return f'''      <section class="card" style="margin-top:14px;">
        <h2>{title}</h2>
        <ul style="margin:10px 0 0 18px; display:grid; gap:8px;">
{rows}
        </ul>
      </section>'''
for title, items in [('Clay County', CLAY), ('Jacksonville', JAX), ('St. Johns County', STJ)]:
    s = replace_once(s, rf'<section class="card" style="margin-top:14px;">\s*<h2>{re.escape(title)}</h2>.*?</section>', sitemap_section(title, items), f'HTML sitemap {title}')
if '<h2>Nassau County</h2>' not in s:
    stj_block = sitemap_section('St. Johns County', STJ)
    s = s.replace(stj_block, stj_block + '\n' + sitemap_section('Nassau County', NASSAU), 1)
s = add_yulee_nav(s)
sitemap.write_text(s, encoding='utf-8')

# 6) Verification: the dedicated architecture must be internally direct and unambiguous.
for filename, cluster in SURVIVING_FILES.items():
    text = (ROOT / filename).read_text(encoding='utf-8')
    # No links on surviving pages should point at retired location URLs.
    for retired in RETIRED_PATHS:
        if f'href="{retired}"' in text or f"href='{retired}'" in text:
            raise SystemExit(f'{filename}: still links retired path {retired}')
    # Nearby blocks should contain only actual core labels, not retired pseudo-pages.
    m = re.search(r'<h3>Nearby Areas We Serve</h3>\s*<ul>(.*?)</ul>', text, re.S)
    if m:
        nearby = m.group(1)
        for label in RETIRED_LABELS:
            if label in nearby and label not in ('Wildlight',):
                raise SystemExit(f'{filename}: retired label remains in nearby-links block: {label}')

# Hub card sections cannot advertise retired pseudo-pages.
for filename, section_id in [
    ('service-areas/jacksonville/index.html', 'county-links-duval'),
    ('service-areas/st-johns-county/index.html', 'county-links'),
    ('service-areas/clay-county/index.html', 'county-links-clay'),
]:
    text = (ROOT / filename).read_text(encoding='utf-8')
    m = re.search(rf'<section class="section" id="{section_id}">(.*?)</section>', text, re.S)
    if not m:
        raise SystemExit(f'{filename}: focused hub section missing')
    block = m.group(1)
    # Mentions are allowed in the explanatory coverage paragraph, but link cards must not use retired hrefs.
    for retired in RETIRED_PATHS:
        if f'href="{retired}"' in block:
            raise SystemExit(f'{filename}: retired href remains in hub cards: {retired}')

main = main_path.read_text(encoding='utf-8')
for _, href in CORE:
    if href not in main:
        raise SystemExit(f'Main service hub missing core URL: {href}')
if 'Popular local pages' in main or '<!-- hs-core-location-hub:start -->' in main:
    raise SystemExit('Main service hub still contains duplicate old location-link sections')

header = (ROOT / 'partials/header.html').read_text(encoding='utf-8')
footer = (ROOT / 'partials/footer.html').read_text(encoding='utf-8')
if '/service-areas/yulee' not in header or '/service-areas/yulee' not in footer:
    raise SystemExit('Yulee missing from shared Service Areas navigation')

visible_sitemap = sitemap.read_text(encoding='utf-8')
for _, href in CORE:
    if href not in visible_sitemap:
        raise SystemExit(f'HTML sitemap missing core URL: {href}')
for retired in RETIRED_PATHS:
    if f'href="{retired}"' in visible_sitemap:
        raise SystemExit(f'HTML sitemap still links retired path: {retired}')

xml = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
for _, href in CORE:
    absolute = 'https://hydrosealpavers.com' + href
    if absolute not in xml:
        raise SystemExit(f'XML sitemap missing core URL: {absolute}')

print('Core location links rebuilt across hubs, surviving pages, navigation, footer, and HTML sitemap.')

from pathlib import Path
import re

FILES = [
    Path('service-areas/index.html'),
    Path('service-areas/jacksonville/index.html'),
    Path('service-areas/jacksonville/jacksonville-beach.html'),
    Path('service-areas/jacksonville/mandarin.html'),
    Path('service-areas/jacksonville/southside.html'),
    Path('service-areas/st-johns-county/index.html'),
    Path('service-areas/st-johns-county/durbin-crossing.html'),
    Path('service-areas/st-johns-county/fruit-cove.html'),
    Path('service-areas/st-johns-county/julington-creek.html'),
    Path('service-areas/st-johns-county/nocatee.html'),
    Path('service-areas/st-johns-county/ponte-vedra.html'),
    Path('service-areas/st-johns-county/ponte-vedra-beach.html'),
    Path('service-areas/st-johns-county/trailmark.html'),
    Path('service-areas/clay-county/index.html'),
    Path('service-areas/clay-county/fleming-island.html'),
    Path('service-areas/clay-county/middleburg.html'),
    Path('service-areas/clay-county/oakleaf-plantation.html'),
    Path('service-areas/clay-county/orange-park.html'),
    Path('service-areas/yulee.html'),
]

RETIRED = [
    'Atlantic Beach', 'Bartram Park', 'Deerwood', 'eTown', 'Etown', 'Glen Kernan',
    'Neptune Beach', 'Ortega', 'Pablo Creek Reserve', 'Queens Harbour',
    'Riverside / Avondale', 'Riverside & Avondale', 'Riverside Avondale', 'Tamaya',
    'Beachwalk', 'Del Webb Ponte Vedra', 'Marsh Landing', 'Murabella', 'Palencia',
    'Palm Valley', 'RiverTown', 'Rivertown', 'Sawgrass', 'Shearwater', 'SilverLeaf',
    'Silverleaf', 'World Golf Village', 'Green Cove Springs', 'Wildlight',
]

# Only unwrap links whose visible anchor text names a retired pseudo-page.
# The location remains mentioned in the copy, but no longer sends a misleading
# exact-location anchor to a different core URL.
anchor_re = re.compile(r'<a\b[^>]*href=["\'][^"\']+["\'][^>]*>(.*?)</a>', re.I | re.S)

def visible_text(html):
    return re.sub(r'<[^>]+>', '', html).replace('&amp;', '&').strip()

for path in FILES:
    text = path.read_text(encoding='utf-8')
    def repl(match):
        inner = match.group(1)
        label = visible_text(inner)
        if any(retired.lower() in label.lower() for retired in RETIRED):
            return inner
        return match.group(0)
    new = anchor_re.sub(repl, text)
    if new != text:
        path.write_text(new, encoding='utf-8')

# Verify no surviving service-area page still uses a retired location name as linked anchor text.
for path in FILES:
    text = path.read_text(encoding='utf-8')
    for m in anchor_re.finditer(text):
        label = visible_text(m.group(1))
        for retired in RETIRED:
            if retired.lower() in label.lower():
                raise SystemExit(f'{path}: retired linked label remains: {label}')

print('Retired location names preserved as coverage text but removed from misleading internal anchors.')

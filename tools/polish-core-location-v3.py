from pathlib import Path
import json
import re

PAGES = {
    Path('service-areas/jacksonville/index.html'): {
        'url': 'https://hydrosealpavers.com/service-areas/jacksonville',
        'name': 'Jacksonville Paver Sealing | Driveways, Pool Decks & Patios | HydroSeal',
        'description': 'Jacksonville paver sealing for driveways, pool decks, patios and walkways with deep cleaning, ASTM C144 joint restoration and professional Trident sealing.',
        'replacements': {
            'HydroSeal also serves Ortega, Riverside/Avondale, Bartram Park, Queens Harbour and other selected Duval County neighborhoods through the Jacksonville hub rather than creating a separate thin page for every subdivision.': 'HydroSeal also serves Ortega, Riverside/Avondale, Bartram Park, Queens Harbour and other selected Duval County neighborhoods, with the restoration plan matched to the closest Jacksonville service area and the conditions at the property.',
        },
    },
    Path('service-areas/st-johns-county/index.html'): {
        'url': 'https://hydrosealpavers.com/service-areas/st-johns-county',
        'name': 'St. Johns County Paver Sealing | Nocatee, Ponte Vedra & More | HydroSeal',
        'description': 'Professional paver sealing across St. Johns County including Nocatee, Ponte Vedra, Julington Creek, Fruit Cove, Durbin Crossing and TrailMark.',
        'replacements': {
            'Seven markets we are actively building': 'Dedicated St. Johns County service areas',
            "Beachwalk, Del Webb Ponte Vedra, Marsh Landing, Murabella, Palencia, Palm Valley, RiverTown, Sawgrass, Shearwater, SilverLeaf and World Golf Village remain part of HydroSeal's St. Johns County coverage and are represented through the closest core market instead of separate thin pages.": "HydroSeal also serves Beachwalk, Del Webb Ponte Vedra, Marsh Landing, Murabella, Palencia, Palm Valley, RiverTown, Sawgrass, Shearwater, SilverLeaf and World Golf Village. We route those properties through the closest St. Johns County service area while evaluating the actual surface and exposure at the home.",
        },
    },
    Path('service-areas/clay-county/index.html'): {
        'url': 'https://hydrosealpavers.com/service-areas/clay-county',
        'name': 'Clay County Paver Sealing | Fleming Island, Orange Park & Oakleaf | HydroSeal',
        'description': 'Clay County paver sealing for Fleming Island, Orange Park, Oakleaf and Middleburg with restoration built around shade, moisture, joint loss and Florida storms.',
        'replacements': {
            'Larger properties and open exposure. Middleburg already has demonstrated Google Search visibility, so we are continuing to build into it.': 'Larger properties and open exposure can create strong UV wear, drainage-driven joint loss and a different maintenance pattern than shaded Clay County neighborhoods.',
            'Green Cove Springs stays inside the Clay County hub': 'Paver sealing in Green Cove Springs',
            "HydroSeal serves suitable Green Cove Springs projects, but we are concentrating that coverage here instead of maintaining another overlapping location page.": "HydroSeal serves suitable Green Cove Springs driveways, patios, walkways and pool areas. River-influenced humidity, tree cover and drainage conditions are evaluated as part of the cleaning and sealing plan.",
        },
    },
    Path('service-areas/yulee.html'): {
        'url': 'https://hydrosealpavers.com/service-areas/yulee',
        'name': 'Paver Sealing Yulee & Wildlight FL | Driveways, Patios & Pool Decks | HydroSeal',
        'description': 'Paver sealing in Yulee and Wildlight, Florida for driveways, patios, walkways and pool decks with professional cleaning, joint restoration and sealing.',
        'replacements': {
            'Wildlight is intentionally built into this Yulee page so Nassau County authority is concentrated on one useful market page instead of competing URLs.': 'Wildlight homes share many of the same Northeast Florida paver conditions as Yulee, including strong sun, newer hardscapes, irrigation exposure and large driveways that benefit from consistent maintenance.',
            'One Nassau County page on purpose': 'Yulee and Wildlight service coverage',
            'HydroSeal is consolidating Yulee and Wildlight into a single dedicated market page. That lets us build deeper local information, project examples and internal links into one URL instead of splitting authority between two overlapping pages.': 'HydroSeal serves both Yulee and Wildlight from this Nassau County service area. Homeowners can use the same local resource for driveway, patio, walkway and pool-deck sealing throughout these neighboring communities.',
            "Yes. Wildlight is part of HydroSeal's Yulee and Nassau County service coverage. We intentionally represent both markets on this single dedicated page.": "Yes. Wildlight is part of HydroSeal's Yulee and Nassau County service coverage for suitable paver driveways, patios, walkways and pool areas.",
        },
    },
}

SCRIPT_RE = re.compile(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)


def sync_webpage_schema(text, url, name, description):
    def repl(match):
        raw = match.group(1).strip()
        try:
            data = json.loads(raw)
        except Exception:
            return match.group(0)
        if data.get('@type') == 'WebPage' and data.get('url') == url:
            data['name'] = name
            data['description'] = description
            return '<script type="application/ld+json">' + json.dumps(data, separators=(',', ':')) + '</script>'
        return match.group(0)
    return SCRIPT_RE.sub(repl, text)


for path, cfg in PAGES.items():
    text = path.read_text(encoding='utf-8')
    for old, new in cfg['replacements'].items():
        if old not in text:
            raise SystemExit(f'{path}: missing expected copy: {old[:80]}')
        text = text.replace(old, new)
    text = sync_webpage_schema(text, cfg['url'], cfg['name'], cfg['description'])
    path.write_text(text, encoding='utf-8')

print('Polished customer-facing core location copy and synchronized WebPage schema.')

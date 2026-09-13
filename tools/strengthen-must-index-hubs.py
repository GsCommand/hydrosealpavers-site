#!/usr/bin/env python3
from pathlib import Path
import re

TODAY = "2026-09-13"

PAGES = {
    Path("service-areas/jacksonville/index.html"): {
        "marker": '<span class="loc-eyebrow">Choose the service</span>',
        "id": "jacksonville-local-prep",
        "block": '''\n  <section class="loc-section loc-section--soft" id="jacksonville-local-prep">\n    <div class="loc-shell">\n      <span class="loc-eyebrow">Jacksonville-specific preparation</span>\n      <h2>Jacksonville conditions that change how pavers should be prepared</h2>\n      <p>Jacksonville is not one uniform paver environment. Coastal exposure near the Beaches and Intracoastal, mature tree canopy in Mandarin, newer high-sun hardscapes across the Southside, irrigation runoff, low joints and older coatings can all change the preparation needed before sealer is applied. HydroSeal evaluates the actual surface instead of using one fixed cleaning-and-sealing routine for every property.</p>\n      <p><strong>Coastal and Intracoastal properties</strong> can see repeated wetting, windblown material and salt exposure, while shaded properties can hold moisture and organic buildup longer. Open driveways can dry quickly but take heavier UV and vehicle wear. Existing coatings, drainage and joint condition also determine whether the job needs routine sealing, <a href="/paver-resealing/">resealing or stripping</a>.</p>\n      <p>HydroSeal routes the work by surface: <a href="/paver-sealing/driveways">driveway paver sealing</a>, <a href="/paver-sealing/pool-decks">pool deck sealing</a>, <a href="/paver-sealing/travertine-sealing">travertine sealing</a> and <a href="/paver-sealing/sand-options">joint-sand restoration</a>. For more localized conditions, see <a href="/service-areas/jacksonville/mandarin">Mandarin</a>, <a href="/service-areas/jacksonville/southside">Southside</a> and <a href="/service-areas/jacksonville/jacksonville-beach">Jacksonville Beach</a>.</p>\n    </div>\n  </section>\n''',
    },
    Path("service-areas/st-johns-county/index.html"): {
        "marker": '<span class="loc-eyebrow">Dedicated St. Johns pages</span>',
        "id": "st-johns-local-prep",
        "block": '''\n  <section class="loc-section" id="st-johns-local-prep">\n    <div class="loc-shell">\n      <span class="loc-eyebrow">St. Johns County project conditions</span>\n      <h2>Why paver sealing needs change across St. Johns County</h2>\n      <p>St. Johns County includes coastal communities, master-planned neighborhoods, established tree-lined areas and inland properties with very different sun, irrigation, drainage and traffic patterns. HydroSeal bases preparation on the paver surface, joint condition, existing coating and moisture conditions at the property rather than treating the entire county as one identical service area.</p>\n      <p>Properties around <a href="/service-areas/st-johns-county/nocatee">Nocatee</a>, <a href="/service-areas/st-johns-county/ponte-vedra">Ponte Vedra</a> and <a href="/service-areas/st-johns-county/ponte-vedra-beach">Ponte Vedra Beach</a> may combine large driveways, pool decks, irrigation and coastal humidity. Farther inland, <a href="/service-areas/st-johns-county/fruit-cove">Fruit Cove</a>, <a href="/service-areas/st-johns-county/julington-creek">Julington Creek</a>, <a href="/service-areas/st-johns-county/durbin-crossing">Durbin Crossing</a> and <a href="/service-areas/st-johns-county/trailmark">TrailMark</a> can present different combinations of shade, runoff, open sun and joint wear.</p>\n      <p>Surface type matters as much as location. Compare HydroSeal's process for <a href="/paver-sealing/driveways">driveways</a>, <a href="/paver-sealing/pool-decks">pool decks</a>, <a href="/paver-sealing/travertine-sealing">travertine</a> and <a href="/paver-resealing/">paver resealing and failed-coating restoration</a>.</p>\n    </div>\n  </section>\n''',
    },
    Path("service-areas/clay-county/index.html"): {
        "marker": '<span class="loc-eyebrow">Core Clay County pages</span>',
        "id": "clay-local-prep",
        "block": '''\n  <section class="loc-section" id="clay-local-prep">\n    <div class="loc-shell">\n      <span class="loc-eyebrow">Clay County surface conditions</span>\n      <h2>Clay County pavers face different moisture, shade and wear patterns</h2>\n      <p>Clay County properties range from shaded established neighborhoods to newer open-sun hardscapes and larger driveways. That variation affects drying time, organic growth, joint-sand loss, stain exposure and how an existing coating should be evaluated before another sealer is applied. HydroSeal adjusts cleaning, joint restoration and sealing to the condition of the surface rather than using one county-wide formula.</p>\n      <p><a href="/service-areas/clay-county/fleming-island">Fleming Island</a> properties can combine tree cover, irrigation and pool-deck moisture; <a href="/service-areas/clay-county/orange-park">Orange Park</a> includes many established hardscapes; <a href="/service-areas/clay-county/oakleaf-plantation">Oakleaf Plantation</a> includes newer paver driveways and patios; and <a href="/service-areas/clay-county/middleburg">Middleburg</a> properties can have broad, highly exposed driveway surfaces. Each needs the surface and joints checked before sealing decisions are made.</p>\n      <p>HydroSeal's core service paths include <a href="/paver-sealing/driveways">driveway paver sealing</a>, <a href="/paver-sealing/pool-decks">pool deck sealing</a>, <a href="/paver-sealing/travertine-sealing">travertine sealing</a>, <a href="/paver-sealing/sand-options">joint-sand restoration</a> and <a href="/paver-resealing/">paver resealing or stripping when an older coating has failed</a>.</p>\n    </div>\n  </section>\n''',
    },
}

changed = []
for path, spec in PAGES.items():
    text = path.read_text(encoding="utf-8")
    if f'id="{spec["id"]}"' in text:
        continue
    marker_index = text.find(spec["marker"])
    if marker_index < 0:
        raise SystemExit(f"Marker not found in {path}: {spec['marker']}")
    section_start = text.rfind("<section", 0, marker_index)
    if section_start < 0:
        raise SystemExit(f"Section start not found in {path}")
    text = text[:section_start] + spec["block"] + "\n" + text[section_start:]
    path.write_text(text, encoding="utf-8")
    changed.append(str(path))

sitemap = Path("sitemap.xml")
xml = sitemap.read_text(encoding="utf-8")
original_xml = xml
for url in (
    "https://hydrosealpavers.com/service-areas/jacksonville",
    "https://hydrosealpavers.com/service-areas/st-johns-county",
    "https://hydrosealpavers.com/service-areas/clay-county",
):
    xml = re.sub(
        rf'(<url><loc>{re.escape(url)}</loc><lastmod>)[^<]+(</lastmod></url>)',
        rf'\g<1>{TODAY}\2',
        xml,
    )
if xml != original_xml:
    sitemap.write_text(xml, encoding="utf-8")
    changed.append("sitemap.xml")

print("Updated:")
for item in changed:
    print(f"- {item}")

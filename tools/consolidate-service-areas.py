from pathlib import Path
import json
import re

BASE = "https://hydrosealpavers.com"
TODAY = "2026-09-03"

# Preserve the URLs that already showed Google visibility, plus the strategic
# markets HydroSeal wants to build around. Smaller overlapping communities are
# consolidated into the closest stronger market rather than left as thin pages.
REDIRECTS = {
    # Jacksonville / Duval
    "/service-areas/jacksonville/atlantic-beach": "/service-areas/jacksonville/jacksonville-beach",
    "/service-areas/jacksonville/bartram-park": "/service-areas/jacksonville",
    "/service-areas/jacksonville/deerwood": "/service-areas/jacksonville/southside",
    "/service-areas/jacksonville/etown": "/service-areas/jacksonville/southside",
    "/service-areas/jacksonville/glen-kernan": "/service-areas/jacksonville/southside",
    "/service-areas/jacksonville/neptune-beach": "/service-areas/jacksonville/jacksonville-beach",
    "/service-areas/jacksonville/ortega": "/service-areas/jacksonville",
    "/service-areas/jacksonville/pablo-creek-reserve": "/service-areas/jacksonville/southside",
    "/service-areas/jacksonville/queens-harbour": "/service-areas/jacksonville",
    "/service-areas/jacksonville/riverside-avondale": "/service-areas/jacksonville",
    "/service-areas/jacksonville/tamaya": "/service-areas/jacksonville/southside",

    # St. Johns County
    "/service-areas/st-johns-county/beachwalk": "/service-areas/st-johns-county",
    "/service-areas/st-johns-county/del-webb-ponte-vedra": "/service-areas/st-johns-county/nocatee",
    "/service-areas/st-johns-county/marsh-landing": "/service-areas/st-johns-county/ponte-vedra-beach",
    "/service-areas/st-johns-county/murabella": "/service-areas/st-johns-county",
    "/service-areas/st-johns-county/palencia": "/service-areas/st-johns-county",
    "/service-areas/st-johns-county/palm-valley": "/service-areas/st-johns-county/ponte-vedra",
    "/service-areas/st-johns-county/rivertown": "/service-areas/st-johns-county",
    "/service-areas/st-johns-county/sawgrass": "/service-areas/st-johns-county/ponte-vedra-beach",
    "/service-areas/st-johns-county/shearwater": "/service-areas/st-johns-county",
    "/service-areas/st-johns-county/silverleaf": "/service-areas/st-johns-county",
    "/service-areas/st-johns-county/world-golf-village": "/service-areas/st-johns-county",

    # Clay County
    "/service-areas/clay-county/green-cove-springs": "/service-areas/clay-county",

    # Nassau County
    "/service-areas/wildlight": "/service-areas/yulee",
}

CORE = [
    "/service-areas",
    "/service-areas/jacksonville",
    "/service-areas/jacksonville/jacksonville-beach",
    "/service-areas/jacksonville/mandarin",
    "/service-areas/jacksonville/southside",
    "/service-areas/st-johns-county",
    "/service-areas/st-johns-county/durbin-crossing",
    "/service-areas/st-johns-county/fruit-cove",
    "/service-areas/st-johns-county/julington-creek",
    "/service-areas/st-johns-county/nocatee",
    "/service-areas/st-johns-county/ponte-vedra",
    "/service-areas/st-johns-county/ponte-vedra-beach",
    # This URL previously earned Google impressions at an average position near 4.
    # Restore it rather than sacrificing an already-proven URL.
    "/service-areas/st-johns-county/trailmark",
    "/service-areas/clay-county",
    "/service-areas/clay-county/fleming-island",
    "/service-areas/clay-county/middleburg",
    "/service-areas/clay-county/oakleaf-plantation",
    "/service-areas/clay-county/orange-park",
    "/service-areas/yulee",
]

ABS_CORE = {BASE + p for p in CORE}

ABSORBED = {
    "/service-areas/jacksonville": ["Bartram Park", "Ortega", "Queens Harbour", "Riverside–Avondale"],
    "/service-areas/jacksonville/jacksonville-beach": ["Atlantic Beach", "Neptune Beach"],
    "/service-areas/jacksonville/southside": ["Deerwood", "eTown", "Glen Kernan", "Pablo Creek Reserve", "Tamaya"],
    "/service-areas/st-johns-county": ["Beachwalk", "Murabella", "Palencia", "Rivertown", "Shearwater", "SilverLeaf", "World Golf Village"],
    "/service-areas/st-johns-county/nocatee": ["Del Webb Ponte Vedra"],
    "/service-areas/st-johns-county/ponte-vedra": ["Palm Valley"],
    "/service-areas/st-johns-county/ponte-vedra-beach": ["Marsh Landing", "Sawgrass"],
    "/service-areas/clay-county": ["Green Cove Springs"],
    "/service-areas/yulee": ["Wildlight"],
}

LABELS = {
    "/service-areas/jacksonville": "Jacksonville",
    "/service-areas/jacksonville/jacksonville-beach": "Jacksonville Beach",
    "/service-areas/jacksonville/southside": "Jacksonville Southside",
    "/service-areas/st-johns-county": "St. Johns County",
    "/service-areas/st-johns-county/nocatee": "Nocatee",
    "/service-areas/st-johns-county/ponte-vedra": "Ponte Vedra",
    "/service-areas/st-johns-county/ponte-vedra-beach": "Ponte Vedra Beach",
    "/service-areas/clay-county": "Clay County",
    "/service-areas/yulee": "Yulee & Wildlight",
}


def page_file(url_path: str) -> Path:
    rel = url_path.strip("/")
    direct = Path(rel + ".html")
    index = Path(rel) / "index.html"
    if index.exists():
        return index
    return direct


def update_vercel():
    path = Path("vercel.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    redirects = data.setdefault("redirects", [])
    sources = set(REDIRECTS)
    redirects = [r for r in redirects if r.get("source") not in sources]
    focused = [
        {"source": source, "destination": BASE + destination, "permanent": True}
        for source, destination in REDIRECTS.items()
    ]
    # Put these before host/catch-all rules so old location URLs transfer in one hop.
    data["redirects"] = focused + redirects
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def update_sitemap():
    path = Path("sitemap.xml")
    lines = path.read_text(encoding="utf-8").splitlines()
    output = []
    for line in lines:
        match = re.search(r"<loc>(https://hydrosealpavers\.com/service-areas[^<]*)</loc>", line)
        if not match:
            output.append(line)
            continue
        loc = match.group(1).rstrip("/")
        if loc not in ABS_CORE:
            continue
        line = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{TODAY}</lastmod>", line)
        output.append(line)

    trailmark = BASE + "/service-areas/st-johns-county/trailmark"
    if not any(trailmark in line for line in output):
        entry = f"  <url><loc>{trailmark}</loc><lastmod>{TODAY}</lastmod></url>"
        insert_at = next((i for i, line in enumerate(output) if "</urlset>" in line), len(output))
        output.insert(insert_at, entry)

    output[2] = "<!-- focused service-area architecture refreshed 2026-09-03 -->"
    path.write_text("\n".join(output) + "\n", encoding="utf-8")


def update_internal_links():
    for path in Path(".").rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        original = text
        for source, destination in REDIRECTS.items():
            # Internal links should point straight to the surviving URL rather than
            # relying on a redirect. Absolute URLs in schema/canonicals are also
            # consolidated where they reference a retired location.
            text = text.replace(f'href="{source}"', f'href="{destination}"')
            text = text.replace(f"href='{source}'", f"href='{destination}'")
            text = text.replace(BASE + source, BASE + destination)
        if text != original:
            path.write_text(text, encoding="utf-8")


def coverage_section(url_path: str, communities):
    label = LABELS[url_path]
    chips = "".join(
        f'<span style="display:inline-block;margin:4px;padding:8px 12px;border-radius:999px;background:#eef7fb;color:#0b2d4a;font-weight:800;">{name}</span>'
        for name in communities
    )
    return f'''\n<!-- hs-location-consolidation:start -->
<section class="section hs-location-coverage" aria-labelledby="nearby-communities-heading">
  <div class="container">
    <div class="card" style="border:1px solid rgba(15,110,168,.18);">
      <p style="margin:0 0 6px;color:#0f6ea8;font-size:12px;font-weight:900;letter-spacing:1.4px;text-transform:uppercase;">Local coverage</p>
      <h2 id="nearby-communities-heading" style="margin:0 0 10px;">Paver Sealing in {label} and Nearby Communities</h2>
      <p class="muted" style="max-width:900px;">HydroSeal serves homeowners throughout {label} as well as nearby communities that share the same Northeast Florida heat, rainfall, irrigation, joint-sand and surface-wear challenges. We evaluate the actual condition of the pavers first, then tailor cleaning, re-sanding and sealing to the surface instead of treating every property the same.</p>
      <div style="margin-top:14px;">{chips}</div>
      <p class="muted" style="margin:16px 0 0;max-width:900px;">Common projects include <a href="/paver-sealing/driveways"><strong>driveway paver sealing</strong></a>, <a href="/paver-sealing/pool-decks"><strong>pool deck sealing</strong></a>, patios and walkways, joint-sand restoration, and <a href="/paver-sealing/travertine-sealing"><strong>travertine sealing</strong></a>. Call <a href="tel:+19045375000"><strong>904-537-5000</strong></a> or <a href="/get-a-quote"><strong>request a quote online</strong></a>.</p>
    </div>
  </div>
</section>
<!-- hs-location-consolidation:end -->\n'''


def inject_coverage():
    marker = re.compile(r"\n?<!-- hs-location-consolidation:start -->.*?<!-- hs-location-consolidation:end -->\n?", re.S)
    for url_path, communities in ABSORBED.items():
        path = page_file(url_path)
        if not path.exists():
            raise SystemExit(f"Missing target page: {path}")
        text = path.read_text(encoding="utf-8")
        text = marker.sub("\n", text)
        section = coverage_section(url_path, communities)
        if "</main>" not in text:
            raise SystemExit(f"No </main> in {path}")
        text = text.replace("</main>", section + "\n</main>", 1)

        if url_path == "/service-areas/yulee":
            text = re.sub(r"<title>.*?</title>", "<title>Paver Sealing Yulee &amp; Wildlight FL | HydroSeal</title>", text, count=1, flags=re.S)
            text = re.sub(
                r'<meta name="description" content="[^"]*"\s*/?>',
                '<meta name="description" content="Professional paver sealing in Yulee and Wildlight, FL for driveways, patios, pool decks and walkways. Cleaning, re-sanding and breathable sealing by HydroSeal." />',
                text,
                count=1,
            )
            text = text.replace("<h1 style=\"margin:8px 0 0;\">Paver Sealing in Yulee, FL</h1>", "<h1 style=\"margin:8px 0 0;\">Paver Sealing in Yulee &amp; Wildlight, FL</h1>")
            text = text.replace("Get Your Yulee Paver Sealing Quote Today", "Get Your Yulee &amp; Wildlight Paver Sealing Quote Today")
        path.write_text(text, encoding="utf-8")


def inject_core_hub():
    path = Path("service-areas/index.html")
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"\n?<!-- hs-core-location-hub:start -->.*?<!-- hs-core-location-hub:end -->\n?", re.S)
    text = pattern.sub("\n", text)
    groups = [
        ("Jacksonville", [
            ("Jacksonville", "/service-areas/jacksonville"),
            ("Mandarin", "/service-areas/jacksonville/mandarin"),
            ("Southside", "/service-areas/jacksonville/southside"),
            ("Jacksonville Beach", "/service-areas/jacksonville/jacksonville-beach"),
        ]),
        ("St. Johns County", [
            ("St. Johns County", "/service-areas/st-johns-county"),
            ("Julington Creek", "/service-areas/st-johns-county/julington-creek"),
            ("Fruit Cove", "/service-areas/st-johns-county/fruit-cove"),
            ("Durbin Crossing", "/service-areas/st-johns-county/durbin-crossing"),
            ("Nocatee", "/service-areas/st-johns-county/nocatee"),
            ("Ponte Vedra", "/service-areas/st-johns-county/ponte-vedra"),
            ("Ponte Vedra Beach", "/service-areas/st-johns-county/ponte-vedra-beach"),
            ("TrailMark", "/service-areas/st-johns-county/trailmark"),
        ]),
        ("Clay & Nassau", [
            ("Clay County", "/service-areas/clay-county"),
            ("Fleming Island", "/service-areas/clay-county/fleming-island"),
            ("Middleburg", "/service-areas/clay-county/middleburg"),
            ("Oakleaf", "/service-areas/clay-county/oakleaf-plantation"),
            ("Orange Park", "/service-areas/clay-county/orange-park"),
            ("Yulee & Wildlight", "/service-areas/yulee"),
        ]),
    ]
    cards = []
    for heading, links in groups:
        anchors = "".join(f'<a href="{url}" style="display:block;padding:9px 0;border-bottom:1px solid #edf1f4;color:#0f6ea8;font-weight:850;text-decoration:none;">{name}</a>' for name, url in links)
        cards.append(f'<div class="community-group"><h3>{heading}</h3>{anchors}</div>')
    block = f'''\n<!-- hs-core-location-hub:start -->
<section class="service-hub-section alt" aria-labelledby="focused-coverage-heading">
  <div class="service-hub-wrap">
    <p class="service-hub-kicker">Focused local coverage</p>
    <div class="service-hub-intro">
      <h2 id="focused-coverage-heading">Our Primary Northeast Florida Paver Sealing Markets</h2>
      <p>HydroSeal focuses its dedicated location pages on the markets where homeowners most often need driveway, pool deck, patio and walkway restoration. Smaller neighborhoods are covered within the closest primary market so each page can provide deeper, more useful local information.</p>
    </div>
    <div class="community-grid">{''.join(cards)}</div>
  </div>
</section>
<!-- hs-core-location-hub:end -->\n'''
    text = text.replace("</main>", block + "\n</main>", 1)
    path.write_text(text, encoding="utf-8")


def update_html_sitemap():
    path = Path("sitemap.html")
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for source in REDIRECTS:
        # Remove retired landing-page entries from the human sitemap instead of
        # sending users through redirects.
        pattern = re.compile(rf"\s*<li><a href=([\"']){re.escape(source)}\1[^>]*>.*?</a></li>\s*", re.S)
        text = pattern.sub("\n", text)
    if "/service-areas/st-johns-county/trailmark" not in text:
        needle = '<li><a href="/service-areas/st-johns-county/julington-creek">Julington Creek</a></li>'
        addition = needle + '\n          <li><a href="/service-areas/st-johns-county/trailmark">TrailMark</a></li>'
        if needle in text:
            text = text.replace(needle, addition, 1)
    path.write_text(text, encoding="utf-8")


def create_trailmark():
    path = Path("service-areas/st-johns-county/trailmark.html")
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Paver Sealing TrailMark St. Augustine FL | HydroSeal</title>
  <meta name="description" content="Professional paver sealing in TrailMark, St. Johns County for driveways, patios, pool areas and walkways. Cleaning, re-sanding and breathable sealing by HydroSeal." />
  <meta name="robots" content="index,follow,max-image-preview:large" />
  <link rel="canonical" href="{BASE}/service-areas/st-johns-county/trailmark" />
  <link rel="stylesheet" href="/styles.css?v=20260809-service-areas" />
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","url":"{BASE}/service-areas/st-johns-county/trailmark","name":"Paver Sealing TrailMark St. Augustine FL | HydroSeal"}}</script>
</head>
<body>
  <div data-include="/partials/header.html"></div>
  <div data-include="/partials/trustbar.html"></div>
  <nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><a href="/">Home</a><span>&gt;</span><a href="/service-areas">Service Areas</a><span>&gt;</span><a href="/service-areas/st-johns-county">St. Johns County</a><span>&gt;</span><span>TrailMark</span></div></nav>
  <main>
    <section class="section"><div class="container">
      <p style="color:#0f6ea8;font-weight:900;letter-spacing:1.2px;text-transform:uppercase;">St. Johns County paver care</p>
      <h1>Paver Sealing in TrailMark, FL</h1>
      <p class="muted" style="max-width:900px;">HydroSeal provides professional paver sealing for TrailMark homeowners with paver driveways, patios, pool areas and walkways that need cleaning, fresh joint sand and protection from Northeast Florida sun, rain and daily wear.</p>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px;"><a class="btn btn-primary" href="/get-a-quote">Request a Quote</a><a class="btn btn-ghost" href="tel:+19045375000">Call 904-537-5000</a></div>
    </div></section>
    <section class="section"><div class="container"><div class="card">
      <h2>Built for TrailMark driveways and outdoor living areas</h2>
      <p class="muted">Pavers around newer St. Johns County homes still deal with UV exposure, irrigation, organic growth, joint-sand loss and tire traffic. Our process starts with the condition of the surface—not a one-size-fits-all coating. We clean thoroughly, address visible staining where practical, restore joint sand when needed and apply a breathable professional sealer for a cleaner, more uniform finish.</p>
      <p class="muted"><strong>Driveways:</strong> restore color, stabilize joints and make routine cleaning easier. <strong>Pool decks and patios:</strong> improve appearance while accounting for moisture exposure and frequent foot traffic. <strong>Walkways:</strong> refresh faded pavers and loose joints around entries and side paths.</p>
    </div></div></section>
    <section class="section"><div class="container"><div class="card">
      <h2>HydroSeal's paver sealing process</h2>
      <ol class="muted"><li>Evaluate existing sealer, stains, drainage and joint condition.</li><li>Deep-clean and prepare the paver surface.</li><li>Re-sand joints when needed with kiln-dried ASTM C144 sand.</li><li>Apply professional breathable paver sealer with controlled coverage.</li><li>Provide cure-time and maintenance guidance before the surface returns to normal use.</li></ol>
      <p class="muted">HydroSeal is Trident Master Certified and backs qualifying paver-sealing work with a two-year workmanship/adhesion warranty. No deposit is required; payment is due when the job is complete.</p>
    </div></div></section>
    <section class="section"><div class="container"><div class="card">
      <h2>Serving TrailMark and nearby St. Johns County</h2>
      <p class="muted">TrailMark is part of our focused St. Johns County service area. We also maintain dedicated pages for <a href="/service-areas/st-johns-county/julington-creek">Julington Creek</a>, <a href="/service-areas/st-johns-county/fruit-cove">Fruit Cove</a>, <a href="/service-areas/st-johns-county/nocatee">Nocatee</a>, <a href="/service-areas/st-johns-county/ponte-vedra">Ponte Vedra</a> and <a href="/service-areas/st-johns-county/ponte-vedra-beach">Ponte Vedra Beach</a>.</p>
      <p><a class="btn btn-primary" href="/get-a-quote">Get a TrailMark Paver Sealing Quote</a></p>
    </div></div></section>
  </main>
  <div data-include="/partials/footer.html"></div>
  <script src="/assets/js/include.js" defer></script>
  <script src="/assets/js/router.js" defer></script>
  <script src="/assets/js/nav.js" defer></script>
  <script src="/assets/js/analytics.js" defer></script>
  <script defer src="/assets/js/third-party-loader.js"></script>
</body>
</html>'''
    path.write_text(html, encoding="utf-8")


def main():
    create_trailmark()
    update_vercel()
    update_sitemap()
    update_internal_links()
    inject_coverage()
    inject_core_hub()
    update_html_sitemap()
    print(f"Focused service-area architecture: {len(CORE)} core URLs; {len(REDIRECTS)} retired URLs redirected.")


if __name__ == "__main__":
    main()

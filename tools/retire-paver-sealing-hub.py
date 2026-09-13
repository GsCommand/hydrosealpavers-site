from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
changed = []


def write_if_changed(path: Path, text: str):
    old = path.read_text(encoding="utf-8")
    if old != text:
        path.write_text(text, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))


# 1) Server-side permanent redirects: retire the generic /paver-sealing hub to the homepage.
vercel_path = ROOT / "vercel.json"
data = json.loads(vercel_path.read_text(encoding="utf-8"))
redirects = data.setdefault("redirects", [])
new_redirects = [
    {"source": "/paver-sealing", "destination": "/", "permanent": True},
    {"source": "/paver-sealing/", "destination": "/", "permanent": True},
]
existing_sources = {r.get("source") for r in redirects}
prepend = [r for r in new_redirects if r["source"] not in existing_sources]
if prepend:
    data["redirects"] = prepend + redirects
    write_if_changed(vercel_path, json.dumps(data, indent=2) + "\n")

# 2) Remove the retired hub from the XML sitemap.
sitemap_xml = ROOT / "sitemap.xml"
xml = sitemap_xml.read_text(encoding="utf-8")
xml = re.sub(
    r'^\s*<url><loc>https://hydrosealpavers\.com/paver-sealing</loc><lastmod>[^<]+</lastmod></url>\s*\n?',
    '',
    xml,
    flags=re.MULTILINE,
)
write_if_changed(sitemap_xml, xml)

# 3) Remove the retired hub from the human-readable sitemap.
sitemap_html = ROOT / "sitemap.html"
html = sitemap_html.read_text(encoding="utf-8")
html = html.replace('            <li><a href="/paver-sealing">Paver Sealing</a></li>\n', '')
write_if_changed(sitemap_html, html)

# 4) Remove the obsolete 404 quick-link to the retired hub.
notfound = ROOT / "404.html"
html = notfound.read_text(encoding="utf-8")
html = html.replace('              <a href="/paver-sealing">Paver Sealing</a>\n', '')
write_if_changed(notfound, html)

# 5) Replace the Jacksonville page's generic hub button with the homepage, which is now the main paver-sealing page.
jax = ROOT / "service-areas/jacksonville/index.html"
html = jax.read_text(encoding="utf-8")
html = html.replace(
    'href="/paver-sealing">View All Paver Sealing Services</a>',
    'href="/">View HydroSeal Paver Sealing</a>',
)
write_if_changed(jax, html)

# 6) Point the stripping/resealing article at the dedicated resealing page instead of the retired generic hub.
article = ROOT / "learning-center/problems/cleaning-resealing-or-stripping/index.html"
html = article.read_text(encoding="utf-8")
html = html.replace(
    '<a href="/paver-sealing">View paver sealing services</a>',
    '<a href="/paver-resealing">View paver resealing services</a>',
)
write_if_changed(article, html)

# 7) Remove the retired hub as a visible and structured breadcrumb parent from child service pages.
sand = ROOT / "paver-sealing/sand-options.html"
html = sand.read_text(encoding="utf-8")
html = html.replace(
    '<nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><a href="/">Home</a><span aria-hidden="true">&gt;</span><a href="/paver-sealing">Paver Sealing</a><span aria-hidden="true">&gt;</span><span aria-current="page">Sand Options</span></div></nav>',
    '<nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><a href="/">Home</a><span aria-hidden="true">&gt;</span><span aria-current="page">Sand Options</span></div></nav>',
)
html = html.replace(
    '      {"@type":"ListItem","position":2,"name":"Paver Sealing","item":"https://hydrosealpavers.com/paver-sealing"},\n      {"@type":"ListItem","position":3,"name":"Sand Options","item":"https://hydrosealpavers.com/paver-sealing/sand-options"}',
    '      {"@type":"ListItem","position":2,"name":"Sand Options","item":"https://hydrosealpavers.com/paver-sealing/sand-options"}',
)
write_if_changed(sand, html)

# Compact JSON-LD breadcrumbs on driveway and pool-deck service pages.
for rel, label, url in [
    ("paver-sealing/driveways.html", "Driveways", "https://hydrosealpavers.com/paver-sealing/driveways"),
    ("paver-sealing/pool-decks.html", "Pool Decks", "https://hydrosealpavers.com/paver-sealing/pool-decks"),
]:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    old = (
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://hydrosealpavers.com/"},'
        '{"@type":"ListItem","position":2,"name":"Paver Sealing","item":"https://hydrosealpavers.com/paver-sealing"},'
        f'{{"@type":"ListItem","position":3,"name":"{label}","item":"{url}"}}]}}'
    )
    new = (
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://hydrosealpavers.com/"},'
        f'{{"@type":"ListItem","position":2,"name":"{label}","item":"{url}"}}]}}'
    )
    html = html.replace(old, new)
    write_if_changed(path, html)

# Multiline breadcrumb on patios/walkways.
patios = ROOT / "paver-sealing/patios-walkways.html"
html = patios.read_text(encoding="utf-8")
html = re.sub(
    r'\{\s*"@type":\s*"ListItem",\s*"position":\s*2,\s*"name":\s*"Paver Sealing",\s*"item":\s*"https://hydrosealpavers\.com/paver-sealing"\s*\},\s*',
    '',
    html,
    count=1,
)
html = html.replace('"position": 3,\n      "name": "Patios & Walkways"', '"position": 2,\n      "name": "Patios & Walkways"', 1)
write_if_changed(patios, html)

# 8) Remove the retired source page. Child URLs under /paver-sealing/ remain untouched.
hub = ROOT / "paver-sealing/index.html"
if hub.exists():
    hub.unlink()
    changed.append(str(hub.relative_to(ROOT)))

print("Changed files:")
for path in changed:
    print(f"- {path}")

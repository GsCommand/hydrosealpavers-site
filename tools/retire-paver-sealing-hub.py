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

# 7) Remove the retired hub as a visible breadcrumb parent from Sand Options.
sand = ROOT / "paver-sealing/sand-options.html"
html = sand.read_text(encoding="utf-8")
html = html.replace(
    '<nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><a href="/">Home</a><span aria-hidden="true">&gt;</span><a href="/paver-sealing">Paver Sealing</a><span aria-hidden="true">&gt;</span><span aria-current="page">Sand Options</span></div></nav>',
    '<nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><a href="/">Home</a><span aria-hidden="true">&gt;</span><span aria-current="page">Sand Options</span></div></nav>',
)
write_if_changed(sand, html)

# 8) Remove the retired hub from structured breadcrumbs on all child service pages.
child_pages = [
    ROOT / "paver-sealing/driveways.html",
    ROOT / "paver-sealing/pool-decks.html",
    ROOT / "paver-sealing/patios-walkways.html",
    ROOT / "paver-sealing/sand-options.html",
    ROOT / "paver-sealing/travertine-sealing.html",
]
parent_item = re.compile(
    r'\{\s*"@type"\s*:\s*"ListItem"\s*,\s*"position"\s*:\s*2\s*,\s*"name"\s*:\s*"Paver Sealing"\s*,\s*"item"\s*:\s*"https://hydrosealpavers\.com/paver-sealing"\s*\}\s*,?\s*',
    flags=re.DOTALL,
)
for path in child_pages:
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8")
    new_html, count = parent_item.subn('', html, count=1)
    if count:
        new_html = re.sub(r'("position"\s*:\s*)3', r'\g<1>2', new_html, count=1)
    write_if_changed(path, new_html)

# 9) Any remaining general internal link to the retired hub now points to the homepage.
# Specific links above are handled first so contextual pages can point to a narrower service when appropriate.
for path in ROOT.rglob("*.html"):
    html = path.read_text(encoding="utf-8", errors="ignore")
    if 'href="/paver-sealing"' in html:
        html = html.replace('href="/paver-sealing"', 'href="/"')
        write_if_changed(path, html)

# 10) Remove the retired source page. Child URLs under /paver-sealing/ remain untouched.
hub = ROOT / "paver-sealing/index.html"
if hub.exists():
    hub.unlink()
    changed.append(str(hub.relative_to(ROOT)))

# 11) Validation: no direct internal href or structured breadcrumb should still point at the retired hub.
remaining_href = []
remaining_breadcrumb_parent = []
for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if 'href="/paver-sealing"' in text:
        remaining_href.append(str(path.relative_to(ROOT)))
    if '"item":"https://hydrosealpavers.com/paver-sealing"' in text or '"item": "https://hydrosealpavers.com/paver-sealing"' in text:
        remaining_breadcrumb_parent.append(str(path.relative_to(ROOT)))

if remaining_href:
    raise SystemExit("Retired /paver-sealing href remains in: " + ", ".join(remaining_href))
if remaining_breadcrumb_parent:
    raise SystemExit("Retired /paver-sealing breadcrumb remains in: " + ", ".join(remaining_breadcrumb_parent))

print("Changed files:")
for path in changed:
    print(f"- {path}")

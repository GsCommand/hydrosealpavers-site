#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BEST = "/learning-center/local/best-time-of-year-to-seal-pavers-in-florida"
SEALING_DUP = "/learning-center/sealing/best-time-of-year-to-seal-pavers-in-florida"

# 1. Redirect rules: preserve the cited local URL and consolidate only the duplicate.
vercel_path = ROOT / "vercel.json"
data = json.loads(vercel_path.read_text(encoding="utf-8"))
redirects = []
for item in data.get("redirects", []):
    source = item.get("source")
    if source in {BEST, SEALING_DUP, "/learning-center/local/:path*"}:
        continue
    redirects.append(item)
insert_at = next((i for i, item in enumerate(redirects) if item.get("source") == "/learning-center/sealing/diy-vs-professional-paver-sealing"), 4)
redirects.insert(insert_at, {"source": SEALING_DUP, "destination": BEST, "permanent": True})
data["redirects"] = redirects
vercel_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

# 2. Sitemap: add the exact cited URL if missing.
sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
full = "https://hydrosealpavers.com" + BEST
if full not in text:
    entry = f"  <url><loc>{full}</loc><lastmod>2026-08-01</lastmod></url>\n"
    text = text.replace("</urlset>", entry + "</urlset>")
    sitemap.write_text(text, encoding="utf-8")

# 3. Learning Center: add the guide card and update visible counts.
index = ROOT / "learning-center" / "index.html"
text = index.read_text(encoding="utf-8")
text = text.replace("Browse 21 practical guides", "Browse 22 practical guides")
text = text.replace("Search and browse 21 practical Florida paver guides.", "Search and browse 22 practical Florida paver guides.")
text = text.replace("Twenty-one practical Florida paver guides", "Twenty-two practical Florida paver guides")
text = text.replace('"numberOfItems":21', '"numberOfItems":22')
text = text.replace('<div><strong>21</strong><span>Detailed guides</span></div>', '<div><strong>22</strong><span>Detailed guides</span></div>')
text = text.replace("Showing all 21 guides.", "Showing all 22 guides.")
if BEST not in text:
    marker = '<article class="lc-card" data-category="sealing"><p class="lc-card__category">Paver Sealing</p><h2><a href="/learning-center/sealing/how-long-does-paver-sealing-last-in-florida">'
    card = '<article class="lc-card" data-category="sealing"><p class="lc-card__category">Florida Weather</p><h2><a href="' + BEST + '">Best Time of Year to Seal Pavers in Florida</a></h2><p>Learn how rain windows, surface moisture, humidity, temperature, drying, and cure time determine a safe sealing schedule.</p><a class="lc-card__link" href="' + BEST + '">Read guide →</a></article>\n      '
    text = text.replace(marker, card + marker)
index.write_text(text, encoding="utf-8")

# 4. llms.txt: expose the cited page as a primary maintained resource.
llms = ROOT / "llms.txt"
text = llms.read_text(encoding="utf-8")
if full not in text:
    text += f"\n- Best time to seal pavers in Florida: {full}\n"
    llms.write_text(text, encoding="utf-8")

# 5. Verify all >3 citation pages have a source file and are not exact redirect sources.
protected = {
    "/learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida": "learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida/index.html",
    BEST: "learning-center/local/best-time-of-year-to-seal-pavers-in-florida/index.html",
    "/landing": "landing.html",
    "/service-areas/st-johns-county/ponte-vedra-beach": "service-areas/st-johns-county/ponte-vedra-beach.html",
    "/learning-center/sealing/water-based-vs-solvent-based-paver-sealer": "learning-center/sealing/water-based-vs-solvent-based-paver-sealer/index.html",
    "/learning-center/sealing/how-long-does-paver-sealing-last-in-florida": "learning-center/sealing/how-long-does-paver-sealing-last-in-florida/index.html",
    "/learning-center/maintenance/paver-maintenance-checklist-for-florida-homeowners": "learning-center/maintenance/paver-maintenance-checklist-for-florida-homeowners/index.html",
    "/": "index.html",
    "/learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot": "learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot/index.html",
    "/learning-center/sealing/wet-look-vs-natural-look-paver-sealer": "learning-center/sealing/wet-look-vs-natural-look-paver-sealer/index.html",
}
redirect_sources = {item.get("source") for item in data["redirects"]}
missing = []
redirected = []
for url, rel in protected.items():
    if not (ROOT / rel).exists():
        missing.append((url, rel))
    if url in redirect_sources:
        redirected.append(url)
if missing or redirected:
    raise SystemExit(f"Preservation audit failed. Missing={missing}; redirected={redirected}")
print("All ten Bing pages above three citations are preserved at their exact URLs.")

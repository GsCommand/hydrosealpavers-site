#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
NEW = "/learning-center/surfaces/astm-c144-sand-vs-polymeric-sand-for-paver-sealing"
CITED = "/learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida"
SEARCH_DUP = "/learning-center/search/best-sand-for-pavers-in-jacksonville"
FADING = "/learning-center/problems/why-pavers-fade-over-time"

# Replace internal references in text-based site files.
allowed = {".html", ".xml", ".txt", ".md", ".py"}
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in allowed:
        continue
    if ".git" in path.parts or path.name == Path(__file__).name:
        continue
    text = path.read_text(encoding="utf-8")
    updated = text.replace(NEW, CITED)
    if updated != text:
        path.write_text(updated, encoding="utf-8")

# Reverse the sand redirect and remove the redirect from the restored fading page.
vercel_path = ROOT / "vercel.json"
data = json.loads(vercel_path.read_text(encoding="utf-8"))
redirects = []
for item in data.get("redirects", []):
    source = item.get("source")
    if source in {CITED, NEW, SEARCH_DUP, FADING}:
        continue
    redirects.append(item)

insert_at = next((i for i, item in enumerate(redirects) if item.get("source") == "/learning-center/search/:path*"), len(redirects))
redirects[insert_at:insert_at] = [
    {"source": NEW, "destination": CITED, "permanent": True},
    {"source": SEARCH_DUP, "destination": CITED, "permanent": True},
]
data["redirects"] = redirects
vercel_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

# Add the restored fading article to the XML sitemap if needed.
sitemap_path = ROOT / "sitemap.xml"
sitemap = sitemap_path.read_text(encoding="utf-8")
full_fading = "https://hydrosealpavers.com" + FADING
if full_fading not in sitemap:
    entry = f"  <url><loc>{full_fading}</loc><lastmod>2026-08-01</lastmod></url>\n"
    sitemap = sitemap.replace("</urlset>", entry + "</urlset>")
    sitemap_path.write_text(sitemap, encoding="utf-8")

# Add a visible Learning Center card for the restored cited page.
index_path = ROOT / "learning-center/index.html"
index = index_path.read_text(encoding="utf-8")
if FADING not in index:
    marker = '<article class="lc-card" data-category="problems"><p class="lc-card__category">Paver Problems</p><h2><a href="/learning-center/problems/why-are-my-pavers-turning-white-in-florida">'
    card = '<article class="lc-card" data-category="problems"><p class="lc-card__category">Paver Problems</p><h2><a href="/learning-center/problems/why-pavers-fade-over-time">Why Pavers Fade Over Time in Florida</a></h2><p>Separate UV exposure, traffic wear, contamination, worn sealer, and permanent surface aging.</p><a class="lc-card__link" href="/learning-center/problems/why-pavers-fade-over-time">Diagnose the problem →</a></article>\n      '
    index = index.replace(marker, card + marker)
    index = index.replace("Browse 20 practical guides", "Browse 21 practical guides")
    index = index.replace("Search and browse 20 practical Florida paver guides.", "Search and browse 21 practical Florida paver guides.")
    index = index.replace("numberOfItems\":20", "numberOfItems\":21")
    index = index.replace("<strong>20</strong><span>Detailed guides</span>", "<strong>21</strong><span>Detailed guides</span>")
    index = index.replace("Showing all 20 guides.", "Showing all 21 guides.")
    index = index.replace("visible === 20", "visible === 21")
    index_path.write_text(index, encoding="utf-8")

print("Promoted Bing-cited sand URL and restored the cited fading guide.")

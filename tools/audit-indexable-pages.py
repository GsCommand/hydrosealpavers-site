from pathlib import Path
from html import unescape
import json, re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://hydrosealpavers.com"

# User-approved audit scope: established sealing/service-area pages only.
# Paver Cleaning and Paver Repair are intentionally excluded while they are still being developed.

def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")

def route_to_file(route):
    route = route.rstrip("/") or "/"
    if route == "/":
        return ROOT / "index.html"
    rel = route.lstrip("/")
    for candidate in (ROOT / (rel + ".html"), ROOT / rel / "index.html"):
        if candidate.exists():
            return candidate
    return None

def first(pattern, text):
    m = re.search(pattern, text, flags=re.I | re.S)
    if not m:
        return ""
    value = re.sub(r"<[^>]+>", " ", m.group(1))
    return re.sub(r"\s+", " ", unescape(value)).strip()

def attr_meta(name, text):
    # Handles either attribute order for standard meta tags.
    patterns = [
        rf'<meta\b[^>]*\bname=["\']{re.escape(name)}["\'][^>]*\bcontent=["\']([^"\']*)["\'][^>]*>',
        rf'<meta\b[^>]*\bcontent=["\']([^"\']*)["\'][^>]*\bname=["\']{re.escape(name)}["\'][^>]*>',
    ]
    for p in patterns:
        m = re.search(p, text, flags=re.I)
        if m:
            return unescape(m.group(1)).strip()
    return ""

def canonical(text):
    patterns = [
        r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)["\'][^>]*>',
        r'<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']canonical["\'][^>]*>',
    ]
    for p in patterns:
        m = re.search(p, text, flags=re.I)
        if m:
            return m.group(1).strip().rstrip("/") or SITE
    return ""

def visible_words(text):
    text = re.sub(r'<script\b.*?</script>', ' ', text, flags=re.I | re.S)
    text = re.sub(r'<style\b.*?</style>', ' ', text, flags=re.I | re.S)
    text = re.sub(r'<header\b.*?</header>', ' ', text, flags=re.I | re.S)
    text = re.sub(r'<footer\b.*?</footer>', ' ', text, flags=re.I | re.S)
    text = re.sub(r'<nav\b.*?</nav>', ' ', text, flags=re.I | re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text).lower()
    return re.findall(r"[a-z0-9]+(?:['-][a-z0-9]+)?", text)

def shingles(words, n=5):
    if len(words) < n:
        return set()
    return {tuple(words[i:i+n]) for i in range(len(words)-n+1)}

# Sitemap URLs are the current intended indexable architecture.
sitemap = read(ROOT / "sitemap.xml")
urls = re.findall(r'<loc>(https://hydrosealpavers\.com[^<]+)</loc>', sitemap)
routes = [urlparse(u).path.rstrip("/") or "/" for u in urls]

scope = []
for route in routes:
    if route in {"/paver-cleaning", "/paver-repair"}:
        continue
    if route.startswith("/paver-sealing/") or route in {"/paver-resealing", "/paver-efflorescence-removal", "/paver-sealing-cost-calculator"} or route == "/service-areas" or route.startswith("/service-areas/"):
        scope.append(route)

vercel = json.loads(read(ROOT / "vercel.json"))
redirects = {r.get("source"): r.get("destination") for r in vercel.get("redirects", []) if r.get("source")}

# Unique internal source files linking to each route. Exclude sitemap/404/partials so the count reflects body/content architecture more than boilerplate.
html_files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
source_cache = {}
for p in html_files:
    rel = str(p.relative_to(ROOT))
    if rel in {"sitemap.html", "404.html"} or rel.startswith("partials/"):
        continue
    source_cache[rel] = read(p)

records = []
for route in scope:
    p = route_to_file(route)
    expected = (SITE + route).rstrip("/") or SITE
    if p is None:
        records.append({"route": route, "file": "MISSING", "error": "NO_SOURCE_FILE"})
        continue
    text = read(p)
    can = canonical(text)
    robots = attr_meta("robots", text)
    title = first(r'<title>(.*?)</title>', text)
    h1 = first(r'<h1\b[^>]*>(.*?)</h1>', text)
    words = visible_words(text)
    incoming = []
    needle1 = f'href="{route}"'
    needle2 = f"href='{route}'"
    needle3 = f'href="{route}/"'
    needle4 = f"href='{route}/'"
    for rel, src in source_cache.items():
        if rel == str(p.relative_to(ROOT)):
            continue
        if any(n in src for n in (needle1, needle2, needle3, needle4)):
            incoming.append(rel)
    records.append({
        "route": route,
        "file": str(p.relative_to(ROOT)),
        "title": title,
        "h1": h1,
        "robots": robots,
        "canonical": can,
        "self_canonical": can == expected,
        "index_allowed": "noindex" not in robots.lower(),
        "word_count": len(words),
        "incoming_unique_files": len(incoming),
        "incoming_examples": incoming[:6],
        "shingles": shingles(words),
    })

# Similarity among active pages; 5-word shingles discount shared nav/footer boilerplate.
for a in records:
    if "shingles" not in a:
        continue
    best = (0.0, "")
    for b in records:
        if a is b or "shingles" not in b:
            continue
        sa, sb = a["shingles"], b["shingles"]
        if not sa or not sb:
            continue
        score = len(sa & sb) / len(sa | sb)
        if score > best[0]:
            best = (score, b["route"])
    a["max_similarity"] = round(best[0], 3)
    a["most_similar_to"] = best[1]
    del a["shingles"]

print("=== HYDROSEAL CURRENT INDEXABLE SERVICE/LOCATION AUDIT ===")
print(f"Scoped sitemap URLs: {len(records)}")
print("Paver Cleaning and Paver Repair intentionally excluded from this audit.\n")

for r in records:
    if r.get("error"):
        print(f"ERROR | {r['route']} | {r['error']}")
        continue
    flags = []
    if not r["self_canonical"]: flags.append("CANONICAL_MISMATCH")
    if not r["index_allowed"]: flags.append("NOINDEX")
    if r["incoming_unique_files"] == 0: flags.append("NO_BODY_INLINKS")
    if r.get("max_similarity", 0) >= 0.45: flags.append("HIGH_SIMILARITY")
    print(" | ".join([
        r["route"],
        f"words={r['word_count']}",
        f"inlinks={r['incoming_unique_files']}",
        f"sim={r.get('max_similarity',0):.3f}->{r.get('most_similar_to','')}",
        f"canonical={'SELF' if r['self_canonical'] else r['canonical'] or 'MISSING'}",
        "flags=" + (",".join(flags) if flags else "OK"),
        f"TITLE={r['title']}",
        f"H1={r['h1']}",
    ]))

print("\n=== SITEMAP / REDIRECT CONFLICTS ===")
conflicts = []
for route in scope:
    if route in redirects:
        conflicts.append((route, redirects[route]))
if conflicts:
    for src, dest in conflicts:
        print(f"SITEMAP URL REDIRECTS | {src} -> {dest}")
else:
    print("None")

print("\n=== RETIRED LOCATION SOURCES (redirected, therefore consolidated) ===")
for src, dest in redirects.items():
    if src.startswith('/service-areas/') and src not in scope and ':path' not in src and src not in {'/service-areas/'}:
        print(f"{src} -> {dest}")

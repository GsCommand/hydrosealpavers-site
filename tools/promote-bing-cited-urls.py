#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
NEW = "/learning-center/surfaces/astm-c144-sand-vs-polymeric-sand-for-paver-sealing"
CITED = "/learning-center/surfaces/what-is-the-best-sand-for-paver-joints-in-florida"
SEARCH_DUP = "/learning-center/search/best-sand-for-pavers-in-jacksonville"

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

# Reverse the redirect so the not-yet-indexed URL consolidates into Bing's cited URL.
vercel_path = ROOT / "vercel.json"
data = json.loads(vercel_path.read_text(encoding="utf-8"))
redirects = []
for item in data.get("redirects", []):
    source = item.get("source")
    if source in {CITED, NEW, SEARCH_DUP}:
        continue
    redirects.append(item)

# Put specific citation-preserving routes before wildcard Learning Center redirects.
insert_at = next((i for i, item in enumerate(redirects) if item.get("source") == "/learning-center/search/:path*"), len(redirects))
redirects[insert_at:insert_at] = [
    {"source": NEW, "destination": CITED, "permanent": True},
    {"source": SEARCH_DUP, "destination": CITED, "permanent": True},
]
data["redirects"] = redirects
vercel_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

print("Promoted Bing-cited sand URL across site files and redirects.")

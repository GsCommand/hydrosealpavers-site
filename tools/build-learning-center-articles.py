#!/usr/bin/env python3
"""Consolidate HydroSeal's Learning Center into 20 text-first blog posts."""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path("learning-center")
SITE = "https://hydrosealpavers.com"
TODAY = "2026-07-30"

KEEP = [
    "sealing/how-long-does-paver-sealing-last-in-florida",
    "sealing/how-often-should-pavers-be-sealed-in-florida",
    "sealing/how-to-choose-the-right-paver-sealer-for-your-home",
    "sealing/water-based-vs-solvent-based-paver-sealer",
    "sealing/wet-look-vs-natural-look-paver-sealer",
    "sealing/why-cheap-paver-sealing-jobs-fail",
    "cleaning/how-to-clean-pavers-without-damaging-them",
    "cleaning/can-pressure-washing-damage-pavers",
    "cleaning/how-to-remove-algae-and-mildew-from-pavers",
    "surfaces/astm-c144-sand-vs-polymeric-sand-for-paver-sealing",
    "surfaces/driveway-paver-sealing-cost-per-square-foot",
    "surfaces/best-sealer-for-pool-decks-slip-safety-and-durability",
    "problems/what-causes-efflorescence-on-pavers",
    "problems/why-are-my-pavers-turning-white-in-florida",
    "problems/why-is-my-paver-sealer-peeling",
    "problems/why-are-my-pavers-slippery-after-sealing",
    "problems/why-is-sand-coming-out-of-my-pavers",
    "travertine/should-you-seal-travertine-pool-decks-in-florida",
    "travertine/how-to-clean-travertine-without-damage",
    "maintenance/paver-maintenance-checklist-for-florida-homeowners",
]
KEEP_SET = set(KEEP)
LABELS = {
    "sealing": "Paver Sealing",
    "cleaning": "Cleaning",
    "surfaces": "Sand, Cost & Pool Decks",
    "problems": "Paver Problems",
    "travertine": "Travertine",
    "maintenance": "Maintenance",
}


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", value)).strip()


def first(pattern: str, source: str, default: str = "") -> str:
    match = re.search(pattern, source, re.I | re.S)
    return clean_text(match.group(1)) if match else default


def extract_body(source: str) -> str:
    match = re.search(r'<div\b[^>]*class="[^"]*learning-article__body[^"]*"[^>]*>(.*?)</div>\s*<section\b[^>]*class="[^"]*learning-article__cta', source, re.I | re.S)
    if match:
        body = match.group(1)
    else:
        article = re.search(r"<article\b[^>]*>(.*?)</article>", source, re.I | re.S)
        body = article.group(1) if article else "<p>This article is being rebuilt.</p>"
    body = re.sub(r"<figure\b.*?</figure>", "", body, flags=re.I | re.S)
    body = re.sub(r"<picture\b.*?</picture>", "", body, flags=re.I | re.S)
    body = re.sub(r"<img\b[^>]*>", "", body, flags=re.I)
    body = re.sub(r"<svg\b.*?</svg>", "", body, flags=re.I | re.S)
    body = re.sub(r'<section\b[^>]*class="[^"]*(?:learning-article__related|learning-article__topics|lc-soft-cta)[^"]*"[^>]*>.*?</section>', "", body, flags=re.I | re.S)
    body = re.sub(r"<h1\b[^>]*>.*?</h1>", "", body, flags=re.I | re.S)
    return body.strip()


def article_data(slug: str) -> dict[str, str]:
    path = ROOT / slug / "index.html"
    source = path.read_text(encoding="utf-8")
    title = first(r"<h1[^>]*>(.*?)</h1>", source) or first(r"<title>(.*?)\s*\|", source)
    intro = first(r'<p[^>]*class="[^"]*(?:learning-article__intro|lc-subhead|dek)[^"]*"[^>]*>(.*?)</p>', source)
    if not intro:
        intro = first(r'<meta name="description" content="([^"]+)"', source)
    return {"slug": slug, "title": title, "intro": intro, "body": extract_body(source), "category": slug.split("/")[0]}


def article_html(item: dict[str, str], related: list[dict[str, str]]) -> str:
    route = "/learning-center/" + item["slug"]
    canonical = SITE + route
    title = html.escape(item["title"])
    intro = html.escape(item["intro"], quote=True)
    related_links = "".join(f'<li><a href="/learning-center/{x["slug"]}">{html.escape(x["title"])}</a></li>' for x in related)
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": canonical + "#article", "url": canonical, "headline": item["title"], "description": item["intro"], "dateModified": TODAY, "inLanguage": "en-US", "articleSection": LABELS[item["category"]], "author": {"@type": "Organization", "@id": SITE + "/#business", "name": "HydroSeal"}, "publisher": {"@id": SITE + "/#business"}, "mainEntityOfPage": {"@id": canonical + "#webpage"}},
            {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": item["title"], "isPartOf": {"@id": SITE + "/#website"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Learning Center", "item": SITE + "/learning-center"},
                {"@type": "ListItem", "position": 3, "name": item["title"], "item": canonical},
            ]},
        ],
    }
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | HydroSeal</title>
<meta name="description" content="{intro}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/styles.css?v=20260312-1">
<link rel="stylesheet" href="/assets/css/learning-center.css?v=20260730-1">
<script type="application/ld+json">{json.dumps(schema, separators=(",", ":"))}</script>
</head>
<body class="page-learning-center lc-article-page">
<header data-include="/includes/header.html"></header>
<main id="page" data-page>
<article class="blog-post">
<nav class="blog-breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span>›</span><a href="/learning-center">Learning Center</a><span>›</span><span aria-current="page">{title}</span></nav>
<header class="blog-post__header">
<p class="blog-post__category">{html.escape(LABELS[item["category"]])}</p>
<h1>{title}</h1>
<p class="blog-post__dek">{html.escape(item["intro"])}</p>
<p class="blog-post__meta">Updated July 30, 2026 · HydroSeal field guidance</p>
</header>
<div class="blog-post__content">{item["body"]}</div>
<section class="blog-post__related"><h2>Related articles</h2><ul>{related_links}</ul></section>
<section class="blog-post__cta"><h2>Need help with your pavers?</h2><p>Send HydroSeal a few photos for practical guidance and a project quote.</p><p><a href="sms:+19045375000">Text 904.537.5000</a> · <a href="/get-a-quote">Request a quote</a></p></section>
</article>
</main>
<footer data-include="/includes/footer.html"></footer>
<script defer src="/assets/js/nav.js"></script>
</body>
</html>\n'''


def directory_html(items: list[dict[str, str]]) -> str:
    links = "".join(f'''<article class="blog-index__item"><p>{html.escape(LABELS[x["category"]])}</p><h2><a href="/learning-center/{x["slug"]}">{html.escape(x["title"])}</a></h2><p>{html.escape(x["intro"])}</p></article>''' for x in items)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HydroSeal Learning Center | Paver Sealing Guides</title><meta name="description" content="Twenty practical HydroSeal articles about paver sealing, cleaning, joint sand, pool decks, travertine, maintenance, and common Florida paver problems."><meta name="robots" content="index,follow"><link rel="canonical" href="{SITE}/learning-center"><link rel="stylesheet" href="/styles.css?v=20260312-1"><link rel="stylesheet" href="/assets/css/learning-center.css?v=20260730-1"></head><body class="page-learning-center"><header data-include="/includes/header.html"></header><main id="page" data-page><section class="blog-index"><header class="blog-index__header"><p>HydroSeal Resources</p><h1>Learning Center</h1><p>Twenty straightforward guides for homeowners comparing paver cleaning, joint sand, sealing, repairs, pool deck care, and travertine maintenance in Northeast Florida.</p></header><div class="blog-index__list">{links}</div></section></main><footer data-include="/includes/footer.html"></footer><script defer src="/assets/js/nav.js"></script></body></html>\n'''


def choose_target(route: str) -> str:
    value = route.lower()
    rules = [
        (("efflorescence",), "problems/what-causes-efflorescence-on-pavers"),
        (("turning-white", "peeling-or-turning-white"), "problems/why-are-my-pavers-turning-white-in-florida"),
        (("peeling",), "problems/why-is-my-paver-sealer-peeling"),
        (("slippery",), "problems/why-are-my-pavers-slippery-after-sealing"),
        (("sand", "weed"), "problems/why-is-sand-coming-out-of-my-pavers"),
        (("travertine", "stone"), "travertine/should-you-seal-travertine-pool-decks-in-florida"),
        (("pool-deck",), "surfaces/best-sealer-for-pool-decks-slip-safety-and-durability"),
        (("cost", "price", "pricing"), "surfaces/driveway-paver-sealing-cost-per-square-foot"),
        (("pressure-wash", "clean-paver", "algae", "mildew", "bleach", "stain"), "cleaning/how-to-clean-pavers-without-damaging-them"),
        (("maintain", "maintenance", "seasonal", "re-sand"), "maintenance/paver-maintenance-checklist-for-florida-homeowners"),
        (("water-based", "solvent-based"), "sealing/water-based-vs-solvent-based-paver-sealer"),
        (("wet-look", "natural-look"), "sealing/wet-look-vs-natural-look-paver-sealer"),
        (("how-long", "how-often", "reseal", "best-time"), "sealing/how-long-does-paver-sealing-last-in-florida"),
    ]
    for needles, target in rules:
        if any(x in value for x in needles):
            return target
    return "sealing/how-to-choose-the-right-paver-sealer-for-your-home"


def update_redirects(all_routes: set[str]) -> None:
    path = Path("vercel.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    redirects = [x for x in data.get("redirects", []) if not str(x.get("source", "")).startswith("/learning-center/")]
    for route in sorted(all_routes - KEEP_SET):
        redirects.append({"source": "/learning-center/" + route, "destination": "/learning-center/" + choose_target(route), "permanent": True})
    data["redirects"] = redirects
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    old_index = (ROOT / "index.html").read_text(encoding="utf-8")
    all_routes = set(re.findall(r'href="/learning-center/([^"#?]+)"', old_index))
    all_routes = {x.rstrip("/") for x in all_routes if x.count("/") >= 1}
    items = [article_data(slug) for slug in KEEP]
    for index, item in enumerate(items):
        related = [items[(index + n) % len(items)] for n in (1, 2, 3)]
        (ROOT / item["slug"] / "index.html").write_text(article_html(item, related), encoding="utf-8")
    (ROOT / "index.html").write_text(directory_html(items), encoding="utf-8")
    for route in sorted(all_routes - KEEP_SET):
        target = ROOT / route
        if target.is_dir():
            shutil.rmtree(target)
    for category in ROOT.iterdir():
        if category.is_dir() and (category / "index.html").exists():
            (category / "index.html").unlink()
        if category.is_dir() and not any(category.iterdir()):
            category.rmdir()
    update_redirects(all_routes)
    print(f"Kept {len(items)} articles; retired {len(all_routes - KEEP_SET)} routes.")


if __name__ == "__main__":
    main()

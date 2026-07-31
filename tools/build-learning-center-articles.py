#!/usr/bin/env python3
"""Validate the finished HydroSeal Learning Center without rewriting article files.

This command is intentionally non-destructive. It fails when a retained article is
missing, thin, internally inconsistent, linked to a retired route, or contains weak
placeholder content. Redirects for merged and retired routes are maintained in
vercel.json and must not be replaced by deleting URLs without destinations.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path("learning-center")
SITE = "https://hydrosealpavers.com"
MIN_WORDS = 550

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
KEEP_ROUTES = {f"/learning-center/{slug}" for slug in KEEP}

PLACEHOLDERS = (
    "this article is being rebuilt",
    "this guide outlines",
    "content coming soon",
    "lorem ipsum",
)


def text_only(value: str) -> str:
    value = re.sub(r"<(script|style)\b.*?</\1>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def first(pattern: str, source: str) -> str:
    match = re.search(pattern, source, flags=re.I | re.S)
    return text_only(match.group(1)) if match else ""


def all_internal_learning_links(source: str) -> set[str]:
    links: set[str] = set()
    for href in re.findall(r'href=["\']([^"\']+)["\']', source, flags=re.I):
        parsed = urlparse(href)
        path = parsed.path.rstrip("/") or "/"
        if path.startswith("/learning-center/"):
            links.add(path)
    return links


def visible_faq_questions(source: str) -> set[str]:
    faq_match = re.search(r'<section\b[^>]*(?:id=["\']faq["\']|class=["\'][^"\']*faq[^"\']*)[^>]*>(.*?)</section>', source, flags=re.I | re.S)
    scope = faq_match.group(1) if faq_match else source
    return {text_only(q) for q in re.findall(r"<h3\b[^>]*>(.*?)</h3>", scope, flags=re.I | re.S)}


def schema_faq_questions(source: str) -> set[str]:
    questions: set[str] = set()
    for raw in re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', source, flags=re.I | re.S):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        stack = [data]
        while stack:
            item = stack.pop()
            if isinstance(item, dict):
                if item.get("@type") == "FAQPage":
                    for entity in item.get("mainEntity", []):
                        if isinstance(entity, dict) and entity.get("name"):
                            questions.add(str(entity["name"]).strip())
                stack.extend(item.values())
            elif isinstance(item, list):
                stack.extend(item)
    return questions


def validate_article(slug: str) -> tuple[list[str], str]:
    path = ROOT / slug / "index.html"
    errors: list[str] = []
    if not path.exists():
        return [f"missing retained article: {path}"], ""

    source = path.read_text(encoding="utf-8")
    lower = source.lower()
    route = f"/learning-center/{slug}"
    canonical = SITE + route

    title = first(r"<title>(.*?)</title>", source)
    h1 = first(r"<h1\b[^>]*>(.*?)</h1>", source)
    breadcrumb = first(r'<span\b[^>]*aria-current=["\']page["\'][^>]*>(.*?)</span>', source)
    body_match = re.search(r'<div\b[^>]*class=["\'][^"\']*blog-post__content[^"\']*["\'][^>]*>(.*?)</div>\s*<section\b[^>]*class=["\'][^"\']*blog-post__related', source, flags=re.I | re.S)
    body_html = body_match.group(1) if body_match else ""
    words = re.findall(r"\b[\w’'-]+\b", text_only(body_html))

    if not h1:
        errors.append("missing H1")
    if not title:
        errors.append("missing title")
    elif h1 and not title.startswith(h1):
        errors.append(f"title/H1 drift: title={title!r}, h1={h1!r}")
    if breadcrumb and h1 and breadcrumb != h1:
        errors.append(f"breadcrumb/H1 drift: breadcrumb={breadcrumb!r}, h1={h1!r}")
    if f'rel="canonical" href="{canonical}"' not in source and f"rel='canonical' href='{canonical}'" not in source:
        errors.append("missing or incorrect canonical")
    if "datepublished" not in lower or "datemodified" not in lower:
        errors.append("missing publication or modification date in structured data")
    if "<h2" not in lower:
        errors.append("missing H2 sections")
    if "quick answer" not in lower:
        errors.append("missing direct Quick answer section")
    if len(words) < MIN_WORDS:
        errors.append(f"thin body: {len(words)} words; minimum is {MIN_WORDS}")
    for phrase in PLACEHOLDERS:
        if phrase in lower:
            errors.append(f"placeholder phrase detected: {phrase!r}")
    if '/includes/header.html' in source or '/includes/footer.html' in source:
        errors.append("uses obsolete /includes/ partial path")
    if '/partials/header.html' not in source or '/partials/footer.html' not in source:
        errors.append("missing shared /partials/ header or footer")
    if '/assets/js/include.js' not in source:
        errors.append("missing include loader")

    broken = sorted(all_internal_learning_links(source) - KEEP_ROUTES)
    if broken:
        errors.append("links to retired or unknown Learning Center routes: " + ", ".join(broken))

    visible_faq = visible_faq_questions(source)
    schema_faq = schema_faq_questions(source)
    if schema_faq and visible_faq != schema_faq:
        errors.append(
            "FAQ schema does not exactly match visible FAQ questions: "
            f"visible={sorted(visible_faq)!r}; schema={sorted(schema_faq)!r}"
        )

    return errors, first(r'<p\b[^>]*class=["\'][^"\']*blog-post__dek[^"\']*["\'][^>]*>(.*?)</p>', source)


def validate_index() -> list[str]:
    path = ROOT / "index.html"
    if not path.exists():
        return ["missing Learning Center index"]
    source = path.read_text(encoding="utf-8")
    links = all_internal_learning_links(source)
    errors: list[str] = []
    missing = sorted(KEEP_ROUTES - links)
    extra = sorted(links - KEEP_ROUTES)
    if missing:
        errors.append("index is missing retained articles: " + ", ".join(missing))
    if extra:
        errors.append("index links to retired or unknown articles: " + ", ".join(extra))
    return errors


def main() -> int:
    failures: list[str] = []
    intros: Counter[str] = Counter()

    for slug in KEEP:
        errors, intro = validate_article(slug)
        if intro:
            intros[intro.casefold()] += 1
        failures.extend(f"{slug}: {error}" for error in errors)

    failures.extend(f"learning-center/index.html: {error}" for error in validate_index())

    duplicates = [intro for intro, count in intros.items() if count > 1 and intro]
    if duplicates:
        failures.append(f"duplicate article introductions detected: {len(duplicates)}")

    if failures:
        print("Learning Center validation failed:\n", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Learning Center validation passed: {len(KEEP)} retained articles and one index.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

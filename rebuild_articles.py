#!/usr/bin/env python3
"""Rebuild FAQ blocks for learning-center article pages.

Policy:
- Keep 3-4 FAQ items by default (trim to strongest 4 when more exist)
- Allow 5 only when the FAQ container includes data-faq-allow-5="true"
- Regenerate FAQPage JSON-LD from visible FAQ items only
- Extract FAQ text from direct faq items only so CTA/sidebar content is ignored
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

FAQ_ITEM_PATTERN = re.compile(
    r"<(?:article|details)[^>]*?(?:lc-faq-item|faq-item)[^>]*>(.*?)</(?:article|details)>",
    re.IGNORECASE | re.DOTALL,
)
H3_Q_PATTERN = re.compile(r"<h3[^>]*>(.*?)</h3>", re.IGNORECASE | re.DOTALL)
SUMMARY_Q_PATTERN = re.compile(r"<summary[^>]*>(.*?)</summary>", re.IGNORECASE | re.DOTALL)
P_A_PATTERN = re.compile(r"<p[^>]*>(.*?)</p>", re.IGNORECASE | re.DOTALL)
FAQ_SECTION_PATTERN = re.compile(
    r"(<section[^>]*>)(.*?<h2[^>]*>\s*Frequently\s+asked\s+questions\s*</h2>.*?)(</section>)",
    re.IGNORECASE | re.DOTALL,
)
FAQ_JSONLD_PATTERN = re.compile(
    r"<script type=\"application/ld\+json\">\s*\{\s*\"@context\"\s*:\s*\"https://schema.org\"\s*,\s*\"@type\"\s*:\s*\"FAQPage\".*?</script>",
    re.IGNORECASE | re.DOTALL,
)
TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")


@dataclass
class FAQItem:
    question: str
    answer: str
    html: str


def clean_text(value: str) -> str:
    no_tags = TAG_PATTERN.sub("", value)
    return SPACE_PATTERN.sub(" ", no_tags).strip()


def extract_faq_items(section_html: str) -> list[FAQItem]:
    items: list[FAQItem] = []
    for match in FAQ_ITEM_PATTERN.finditer(section_html):
        block = match.group(0)
        inner = match.group(1)
        q_match = H3_Q_PATTERN.search(inner) or SUMMARY_Q_PATTERN.search(inner)
        a_match = P_A_PATTERN.search(inner)
        if not q_match or not a_match:
            continue
        q = clean_text(q_match.group(1))
        a = clean_text(a_match.group(1))
        if q and a:
            items.append(FAQItem(question=q, answer=a, html=block))
    return items


def score_question(question: str) -> int:
    q = question.lower()
    high_intent_tokens = [
        "cost",
        "price",
        "how often",
        "strip",
        "sealer",
        "florida",
        "humidity",
        "timing",
        "driveway",
    ]
    return sum(1 for token in high_intent_tokens if token in q)


def choose_items(items: list[FAQItem], allow_five: bool) -> list[FAQItem]:
    limit = 5 if allow_five else 4
    if len(items) <= limit:
        return items
    scored = sorted(enumerate(items), key=lambda x: (score_question(x[1].question), -x[0]), reverse=True)
    chosen_indexes = sorted(i for i, _ in scored[:limit])
    return [items[i] for i in chosen_indexes]


def build_faq_jsonld(items: Iterable[FAQItem]) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": {"@type": "Answer", "text": item.answer},
            }
            for item in items
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "</script>"


def rebuild_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    match = FAQ_SECTION_PATTERN.search(html)
    if not match:
        match = re.search(
            r"(<section[^>]*id=\"faq\"[^>]*>)(.*?)(</section>)",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
    if not match:
        return False

    section_open, section_body, section_close = match.groups()
    faq_items = extract_faq_items(section_body)
    if not faq_items:
        return False

    allow_five = 'data-faq-allow-5="true"' in section_open.lower() or 'data-faq-allow-5="true"' in section_body.lower()
    final_items = choose_items(faq_items, allow_five=allow_five)

    # Preserve the existing wrapper and heading; replace only faq-item blocks.
    rebuilt_body = section_body
    rebuilt_body = FAQ_ITEM_PATTERN.sub("", rebuilt_body)
    insertion = "".join(item.html for item in final_items)
    if "lc-faq-list" in section_body:
        rebuilt_body = re.sub(r"(<div[^>]*lc-faq-list[^>]*>)", r"\1" + insertion, rebuilt_body, count=1, flags=re.IGNORECASE)
    else:
        rebuilt_body = rebuilt_body + insertion

    new_section = section_open + rebuilt_body + section_close
    html = html[: match.start()] + new_section + html[match.end() :]

    faq_json = build_faq_jsonld(final_items)
    if FAQ_JSONLD_PATTERN.search(html):
        html = FAQ_JSONLD_PATTERN.sub(faq_json, html, count=1)
    else:
        head_close = html.lower().find("</head>")
        if head_close != -1:
            html = html[:head_close] + faq_json + html[head_close:]

    path.write_text(html, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild learning-center article FAQ blocks.")
    parser.add_argument("paths", nargs="*", help="Specific article files. Defaults to all learning-center article index pages.")
    args = parser.parse_args()

    targets = [Path(p) for p in args.paths] if args.paths else list(Path("learning-center").glob("*/*/index.html"))

    changed = 0
    for target in targets:
        if rebuild_file(target):
            changed += 1
            print(f"updated {target}")

    print(f"done: {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

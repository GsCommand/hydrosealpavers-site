#!/usr/bin/env python3
"""Build the shared, static Learning Center article template.

Article copy remains in each route's existing HTML file.  This builder is the
single source for the surrounding editorial layout, metadata, related-guide
selection, CTA, breadcrumbs, and category navigation.  It deliberately keeps
the site dependency-free so the static site can be deployed as-is.
"""
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path("learning-center")
SITE = "https://hydrosealpavers.com"
CATEGORIES = {
    "sealing": "Paver Sealing Basics", "cleaning": "Cleaning", "maintenance": "Maintenance",
    "problems": "Sealer Problems", "surfaces": "Pool Decks & Surfaces",
    "travertine": "Travertine", "warranty": "Choosing a Contractor", "local": "Local Florida Conditions",
    "search": "Learning Center Guides",
}
TOPICS = [("sealing", "Paver Sealing Basics"), ("cleaning", "Cleaning"), ("maintenance", "Maintenance"),
          ("problems", "Sealer Problems"), ("surfaces", "Pool Decks & Surfaces"), ("travertine", "Travertine"),
          ("local", "Local Florida Conditions")]

@dataclass
class Guide:
    path: Path
    route: str
    category: str
    title: str
    intro: str
    hero: str | None
    body: str
    header: str
    footer: str

def clean(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", value)).strip()

def tag_block(source: str, tag: str, start: int = 0) -> tuple[str, int, int] | None:
    match = re.search(rf"<{tag}\b[^>]*>", source[start:], re.I)
    if not match: return None
    opening = start + match.start(); pos = start + match.end(); depth = 1
    tokens = re.compile(rf"</?{tag}\b[^>]*>", re.I)
    while (token := tokens.search(source, pos)):
        depth += -1 if token.group().startswith("</") else 1
        pos = token.end()
        if depth == 0: return source[opening:pos], opening, pos
    return None

def content_of(block: str) -> str:
    return re.sub(r"^<[^>]+>|</[^>]+>$", "", block.strip(), flags=re.S)

def first(pattern: str, source: str) -> str:
    m = re.search(pattern, source, re.I | re.S)
    return clean(m.group(1)) if m else ""

def image(source: str) -> str | None:
    m = re.search(r"(?:--lc-hero-image|--learning-center-hero-image)\s*:\s*url\(['\"]?([^'\")]+)", source, re.I)
    if m: return m.group(1)
    m = re.search(r'<figure[^>]*learning-article__hero[^>]*>\s*<img[^>]*src="([^"]+)', source, re.I)
    if m: return m.group(1)
    m = re.search(r'<meta property="og:image" content="https?://hydrosealpavers\.com([^"?]+)', source, re.I)
    return m.group(1) if m else None

def remove_ctas(body: str) -> str:
    # The old sidebar and CTA are intentionally not retained in the shared layout.
    body = re.sub(r"<section\b[^>]*\blc-soft-cta\b[^>]*>.*?</section>", "", body, flags=re.I | re.S)
    body = re.sub(r"<section\b[^>]*(?:\bhelp\b|\bcta\b)[^>]*>.*?</section>", "", body, flags=re.I | re.S)
    body = re.sub(r"[Tt]his placeholder article[^.]*\.", "This guide focuses on the practical checks homeowners can make before choosing a treatment.", body)
    body = re.sub(r"This placeholder section will be expanded with examples and local guidance\.", "For surface-specific guidance, request an inspection before choosing a treatment.", body)
    return body.strip()

def remove_section_class(body: str, class_name: str) -> str:
    """Remove a complete section even when it contains nested article cards."""
    while (match := re.search(rf'<section\b[^>]*\b{re.escape(class_name)}\b[^>]*>', body, re.I)):
        block = tag_block(body, "section", match.start())
        if not block: break
        body = body[:block[1]] + body[block[2]:]
    return body

class ArticleBodyNormalizer(HTMLParser):
    """Keep article copy while removing legacy layout-only wrappers."""
    UNWRAP_CLASSES = {
        "container", "lc-detail-section", "lc-detail-stack", "lc-prose-layout", "lc-prose",
        "lc-section-heading", "lc-section-heading--left", "section-heading", "lc-faq-list",
    }
    SECTION_CLASSES = {"lc-prose-section", "lc-article-section", "lc-faq-item", "lc-takeaways-card", "lc-process-box"}
    KEEP_CLASSES = {"lc-table-wrap", "table-wrap", "lc-compare-table", "lc-list-check"}
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.output: list[str] = []
        self.stack: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = set(dict(attrs).get("class", "").split())
        if tag == "aside":
            tag = "section"
            classes = set()
        if classes & self.UNWRAP_CLASSES:
            self.stack.append((tag, None))
            return
        output_tag = "section" if classes & self.SECTION_CLASSES else tag
        kept_attrs = [(key, value) for key, value in attrs if key != "class" or value in self.KEEP_CLASSES]
        self.output.append("<" + output_tag + "".join(
            f' {key}' if value is None else f' {key}="{html.escape(value, quote=True)}"'
            for key, value in kept_attrs
        ) + ">")
        if tag not in self.VOID_TAGS:
            self.stack.append((tag, output_tag))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return
        _, output_tag = self.stack.pop()
        if output_tag:
            self.output.append(f"</{output_tag}>")

    def handle_data(self, data: str) -> None:
        self.output.append(data)

    def handle_entityref(self, name: str) -> None:
        self.output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.output.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.output.append(f"<!--{data}-->")

def normalize_article_body(body: str) -> str:
    """Convert old card-and-sidebar article markup into a single prose flow."""
    body = remove_section_class(body, "lc-detail-hero")
    # Related-reading blocks from old templates duplicate the shared related-guides section.
    while True:
        related_section = None
        for match in re.finditer(r'<section\b[^>]*\blc-detail-section\b[^>]*>', body, re.I):
            block = tag_block(body, "section", match.start())
            if block and "lc-related-grid" in block[0]:
                related_section = block
                break
        if not related_section:
            break
        body = body[:related_section[1]] + body[related_section[2]:]
    parser = ArticleBodyNormalizer()
    parser.feed(body)
    parser.close()
    return "".join(parser.output).strip()

def read_guide(path: Path) -> Guide:
    source = path.read_text(encoding="utf-8")
    category = path.parts[1]
    title = first(r"<h1[^>]*>(.*?)</h1>", source) or first(r"<title>(.*?)\|", source)
    intro = first(r'<p[^>]*class="[^"]*(?:lc-subhead|dek|learning-center-dek|learning-article__intro)[^"]*"[^>]*>(.*?)</p>', source)
    if not intro:
        intro = first(r"<article\b[^>]*>\s*(?:<section[^>]*>)?\s*<p[^>]*>(.*?)</p>", source)
    if "placeholder" in intro.lower():
        intro = "This guide outlines the practical checks and next steps homeowners can use when evaluating this paver concern."
    main = tag_block(source, "main")
    article = tag_block(main[0], "article") if main else None
    existing_body = re.search(r'<div\b[^>]*\blearning-article__body\b[^>]*>', source, re.I)
    body_block = tag_block(source, "div", existing_body.start()) if existing_body else None
    body = remove_ctas(content_of(body_block[0]) if body_block else (content_of(article[0]) if article else "<p>Guide content is being reviewed.</p>"))
    # Pages generated by this tool can safely be used as the next build input.
    body = re.sub(r'<header class="learning-article__header">.*?</header>', "", body, flags=re.I | re.S)
    body = remove_section_class(body, "learning-article__related")
    body = remove_section_class(body, "learning-article__topics")
    body = re.sub(r'<h1\b[^>]*>.*?</h1>', '', body, flags=re.I | re.S)
    body = re.sub(r'placeholder', 'general', body, flags=re.I)
    body = normalize_article_body(body)
    header = source[source.lower().find("<body"): source.lower().find("<main")]
    header = re.sub(r'<nav class="breadcrumb"[^>]*>.*?</nav>', '', header, flags=re.I | re.S)
    footer_match = tag_block(source, "footer")
    footer = footer_match[0] if footer_match else '<footer data-include="/includes/footer.html"></footer>'
    route = "/" + str(path.parent).replace("\\", "/")
    return Guide(path, route, category, title, intro, image(source), body, header, footer)

def related(g: Guide, all_guides: list[Guide]) -> list[Guide]:
    same = [x for x in all_guides if x.route != g.route and x.category == g.category]
    rest = [x for x in all_guides if x.route != g.route and x.category != g.category]
    return (same + rest)[:3]

def breadcrumb_schema(g: Guide) -> dict:
    category_url = f"{SITE}/learning-center/{g.category}"
    return {"@context":"https://schema.org", "@type":"BreadcrumbList", "itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE + "/"},
        {"@type":"ListItem","position":2,"name":"Learning Center","item":SITE + "/learning-center"},
        {"@type":"ListItem","position":3,"name":CATEGORIES[g.category],"item":category_url},
        {"@type":"ListItem","position":4,"name":g.title,"item":SITE + g.route}]}

def build(g: Guide, all_guides: list[Guide]) -> str:
    hero = ""
    if g.hero:
        hero = f'<figure class="learning-article__hero"><img src="{html.escape(g.hero)}" alt="{html.escape(g.title)}" width="1600" height="900" decoding="async"><figcaption>HydroSeal Learning Center</figcaption></figure>'
    cards = "".join(f'''<article class="learning-article-card">{'<img src="' + html.escape(x.hero) + '" alt="" width="800" height="450" loading="lazy" decoding="async">' if x.hero else ''}<div><span>{html.escape(CATEGORIES[x.category])}</span><h3>{html.escape(x.title)}</h3><p>{html.escape(x.intro)}</p><a href="{x.route}">Read Guide<span class="sr-only">: {html.escape(x.title)}</span></a></div></article>''' for x in related(g, all_guides))
    topics = "".join(f'<a href="/learning-center/{slug}">{label}</a>' for slug, label in TOPICS)
    category = CATEGORIES[g.category]
    article_schema = {"@context":"https://schema.org", "@type":"Article", "mainEntityOfPage":SITE + g.route,
        "headline":g.title, "description":g.intro, "publisher":{"@type":"Organization","name":"HydroSeal","logo":{"@type":"ImageObject","url":SITE + "/assets/hero/Hydrosealpaversealing.png"}}}
    if g.hero: article_schema["image"] = [SITE + g.hero]
    head = g.path.read_text(encoding="utf-8")
    head = re.sub(r'placeholder', 'general', head, flags=re.I)
    head = re.sub(r'<script type="application/ld\+json">[^<]*"@type"\s*:\s*"(?:Article|BlogPosting|BreadcrumbList)"[^<]*</script>', '', head, flags=re.I)
    head = re.sub(r'(<meta name="description" content=")[^"]*(")', rf'\1{html.escape(g.intro, quote=True)}\2', head, count=1, flags=re.I)
    schemas = '<script type="application/ld+json">' + json.dumps(article_schema, separators=(",", ":")) + '</script><script type="application/ld+json">' + json.dumps(breadcrumb_schema(g), separators=(",", ":")) + '</script>'
    head = head.replace("</head>", schemas + "</head>")
    breadcrumbs = f'<nav class="learning-article__breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span><a href="/learning-center">Learning Center</a><span aria-hidden="true">›</span><a href="/learning-center/{g.category}">{html.escape(category)}</a><span aria-hidden="true">›</span><span aria-current="page">{html.escape(g.title)}</span></nav>'
    layout = f'''<main id="page" data-page><article class="learning-article" data-learning-article="true"><header class="learning-article__header"><div class="learning-article__column">{breadcrumbs}<span class="learning-article__category">{html.escape(category)}</span><h1>{html.escape(g.title)}</h1><p class="learning-article__intro">{html.escape(g.intro)}</p></div></header>{hero}<div class="learning-article__column learning-article__body">{g.body}</div><section class="learning-article__cta" aria-labelledby="article-cta-title"><div class="learning-article__column"><span>HydroSeal Pavers</span><h2 id="article-cta-title">Not sure what your pavers need?</h2><p>Share a few photos with HydroSeal for practical guidance on cleaning, joint sand, sealing, or failed-sealer correction.</p><div><a class="btn btn-primary" href="/get-a-quote">Text Photos for a Quote</a><a class="learning-article__call" href="tel:+19045375000">Call HydroSeal: 904.537.5000</a></div></div></section><section class="learning-article__related" aria-labelledby="related-guides"><div class="container"><h2 id="related-guides">Related guides</h2><div class="learning-article__related-grid">{cards}</div></div></section><section class="learning-article__topics" aria-labelledby="explore-topics"><div class="learning-article__column"><h2 id="explore-topics">Explore more Learning Center topics</h2><div>{topics}</div></div></section></article></main>'''
    output = head[:head.lower().find("<body")] + g.header + layout + g.footer + '\n<script defer src="/assets/js/nav.js"></script>\n<script defer src="/assets/js/learning-center-article.js"></script>\n</body>\n</html>\n'
    return re.sub(r"[ \t]+\n", "\n", output)

def main() -> None:
    guides = [read_guide(p) for p in sorted(ROOT.glob("*/*/index.html"))]
    for guide in guides: guide.path.write_text(build(guide, guides), encoding="utf-8")
    print(f"built {len(guides)} Learning Center articles")

if __name__ == "__main__": main()

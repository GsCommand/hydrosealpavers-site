#!/usr/bin/env python3
"""Validate HydroSeal Learning Center articles and directory links."""
from __future__ import annotations
import json,re,sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path("learning-center")
SITE="https://hydrosealpavers.com"
MIN_WORDS=550
KEEP=[
"problems/cleaning-resealing-or-stripping",
"sealing/is-paver-sealing-worth-it-in-florida",
"cost/how-much-does-it-cost-to-strip-and-reseal-pavers",
"sealing/what-should-professional-paver-sealing-include",
"sealing/diy-vs-professional-paver-sealing-in-florida",
"hiring/how-to-choose-a-paver-sealing-company-in-northeast-florida",
"local/best-time-of-year-to-seal-pavers-in-florida",
"sealing/how-long-does-paver-sealing-last-in-florida",
"sealing/how-often-should-pavers-be-sealed-in-florida",
"sealing/how-to-choose-the-right-paver-sealer-for-your-home",
"sealing/water-based-vs-solvent-based-paver-sealer",
"sealing/wet-look-vs-natural-look-paver-sealer",
"sealing/why-cheap-paver-sealing-jobs-fail",
"cleaning/how-to-clean-pavers-without-damaging-them",
"cleaning/can-pressure-washing-damage-pavers",
"cleaning/how-to-remove-algae-and-mildew-from-pavers",
"surfaces/what-is-the-best-sand-for-paver-joints-in-florida",
"surfaces/driveway-paver-sealing-cost-per-square-foot",
"surfaces/best-sealer-for-pool-decks-slip-safety-and-durability",
"problems/what-causes-efflorescence-on-pavers",
"problems/why-pavers-fade-over-time",
"problems/why-are-my-pavers-turning-white-in-florida",
"problems/why-is-my-paver-sealer-peeling",
"problems/why-are-my-pavers-slippery-after-sealing",
"problems/why-is-sand-coming-out-of-my-pavers",
"travertine/should-you-seal-travertine-pool-decks-in-florida",
"travertine/how-to-clean-travertine-without-damage",
"maintenance/paver-maintenance-checklist-for-florida-homeowners",
]
KEEP_ROUTES={f"/learning-center/{slug}" for slug in KEEP}
PLACEHOLDERS=("this article is being rebuilt","this guide outlines","content coming soon","lorem ipsum")
def text_only(value:str)->str:
 value=re.sub(r"<(script|style)\b.*?</\1>"," ",value,flags=re.I|re.S);value=re.sub(r"<[^>]+>"," ",value);return re.sub(r"\s+"," ",value).strip()
def first(pattern:str,source:str)->str:
 m=re.search(pattern,source,flags=re.I|re.S);return text_only(m.group(1)) if m else ""
def internal_links(source:str)->set[str]:
 links=set()
 for href in re.findall(r'href=["\']([^"\']+)["\']',source,flags=re.I):
  path=urlparse(href).path.rstrip("/") or "/"
  if path.startswith("/learning-center/"):links.add(path)
 return links
def visible_faq(source:str)->set[str]:
 m=re.search(r'<section\b[^>]*(?:id=["\']faq["\']|class=["\'][^"\']*faq[^"\']*)[^>]*>(.*?)</section>',source,flags=re.I|re.S);scope=m.group(1) if m else source
 return {text_only(q) for q in re.findall(r"<h3\b[^>]*>(.*?)</h3>",scope,flags=re.I|re.S)}
def schema_faq(source:str)->set[str]:
 out=set()
 for raw in re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',source,flags=re.I|re.S):
  try:data=json.loads(raw)
  except json.JSONDecodeError:continue
  stack=[data]
  while stack:
   item=stack.pop()
   if isinstance(item,dict):
    if item.get("@type")=="FAQPage":
     for entity in item.get("mainEntity",[]):
      if isinstance(entity,dict) and entity.get("name"):out.add(str(entity["name"]).strip())
    stack.extend(item.values())
   elif isinstance(item,list):stack.extend(item)
 return out
def validate_article(slug:str)->tuple[list[str],str]:
 path=ROOT/slug/"index.html";errors=[]
 if not path.exists():return [f"missing retained article: {path}"],""
 source=path.read_text(encoding="utf-8");lower=source.lower();route=f"/learning-center/{slug}";canonical=SITE+route
 title=first(r"<title>(.*?)</title>",source);h1=first(r"<h1\b[^>]*>(.*?)</h1>",source)
 body_match=re.search(r'<div\b[^>]*class=["\'][^"\']*blog-post__content[^"\']*["\'][^>]*>(.*?)</div>\s*<section\b[^>]*class=["\'][^"\']*blog-post__related',source,flags=re.I|re.S)
 words=re.findall(r"\b[\w’'-]+\b",text_only(body_match.group(1) if body_match else ""))
 if not h1:errors.append("missing H1")
 if not title:errors.append("missing title")
 elif h1 and not title.startswith(h1):errors.append(f"title/H1 drift: title={title!r}, h1={h1!r}")
 if f'rel="canonical" href="{canonical}"' not in source and f"rel='canonical' href='{canonical}'" not in source:errors.append("missing or incorrect canonical")
 if "datepublished" not in lower or "datemodified" not in lower:errors.append("missing publication or modification date in structured data")
 if "<h2" not in lower:errors.append("missing H2 sections")
 if "quick answer" not in lower:errors.append("missing direct Quick answer section")
 if len(words)<MIN_WORDS:errors.append(f"thin body: {len(words)} words; minimum is {MIN_WORDS}")
 for phrase in PLACEHOLDERS:
  if phrase in lower:errors.append(f"placeholder phrase detected: {phrase!r}")
 if '/partials/header.html' not in source or '/partials/footer.html' not in source:errors.append("missing shared header or footer")
 if '/assets/js/include.js' not in source:errors.append("missing include loader")
 broken=sorted(internal_links(source)-KEEP_ROUTES)
 if broken:errors.append("links to unknown Learning Center routes: "+", ".join(broken))
 visible,schema=visible_faq(source),schema_faq(source)
 if schema and visible!=schema:errors.append(f"FAQ schema mismatch: visible={sorted(visible)!r}; schema={sorted(schema)!r}")
 return errors,first(r'<p\b[^>]*class=["\'][^"\']*blog-post__dek[^"\']*["\'][^>]*>(.*?)</p>',source)
def main()->int:
 failures=[];intros=Counter()
 for slug in KEEP:
  errors,intro=validate_article(slug)
  if intro:intros[intro.casefold()]+=1
  failures.extend(f"{slug}: {e}" for e in errors)
 index=ROOT/"index.html"
 if not index.exists():failures.append("missing Learning Center index")
 else:
  links=internal_links(index.read_text(encoding="utf-8"));missing=sorted(KEEP_ROUTES-links);extra=sorted(links-KEEP_ROUTES)
  if missing:failures.append("index missing: "+", ".join(missing))
  if extra:failures.append("index unknown links: "+", ".join(extra))
 if any(c>1 for c in intros.values()):failures.append("duplicate article introductions detected")
 if failures:
  print("Learning Center validation failed:\n",file=sys.stderr)
  for failure in failures:print(f"- {failure}",file=sys.stderr)
  return 1
 print(f"Learning Center validation passed: {len(KEEP)} retained articles and one index.");return 0
if __name__=="__main__":raise SystemExit(main())

#!/usr/bin/env python3
from pathlib import Path

MAPPING = {
    '/learning-center/search/why-pressure-washing-alone-is-not-enough-for-pavers': '/learning-center/cleaning/can-pressure-washing-damage-pavers',
    '/learning-center/search/is-paver-sealing-worth-it-in-jacksonville': '/learning-center/sealing/how-long-does-paver-sealing-last-in-florida',
    '/learning-center/local/best-time-of-year-to-seal-pavers-in-florida': '/learning-center/sealing/how-often-should-pavers-be-sealed-in-florida',
    '/learning-center/search/how-much-does-paver-sealing-cost-in-jacksonville': '/learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot',
    '/learning-center/search/how-much-does-paver-sealing-cost-in-fleming-island': '/learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot',
    '/learning-center/search/how-much-does-paver-sealing-cost-in-nocatee': '/learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot',
    '/learning-center/search/how-much-does-paver-sealing-cost-in-ponte-vedra': '/learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot',
    '/learning-center/search/how-much-does-paver-sealing-cost-in-oakleaf-plantation': '/learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot',
    '/learning-center/search/one-day-vs-two-day-paver-sealing-in-florida': '/learning-center/sealing/how-often-should-pavers-be-sealed-in-florida',
    '/learning-center/search/what-is-the-best-paver-sealer-for-jacksonville': '/learning-center/sealing/how-to-choose-the-right-paver-sealer-for-your-home',
    '/learning-center/search/what-is-the-best-paver-sealer-for-pool-decks': '/learning-center/surfaces/best-sealer-for-pool-decks-slip-safety-and-durability',
    '/learning-center/search/what-is-the-best-sealer-for-travertine': '/learning-center/travertine/should-you-seal-travertine-pool-decks-in-florida',
    '/learning-center/search/astm-c144-sand-vs-polymeric-sand-for-paver-sealing': '/learning-center/surfaces/astm-c144-sand-vs-polymeric-sand-for-paver-sealing',
    '/learning-center/search/why-cheap-paver-sealing-jobs-fail': '/learning-center/sealing/why-cheap-paver-sealing-jobs-fail',
    '/learning-center/search/should-you-use-bleach-on-pavers-before-sealing': '/learning-center/cleaning/how-to-clean-pavers-without-damaging-them',
    '/learning-center/problems/why-is-my-paver-sealer-peeling-or-turning-white': '/learning-center/problems/why-is-my-paver-sealer-peeling',
    '/learning-center/problems/why-do-pavers-fail-faster-near-the-beach': '/learning-center/sealing/how-long-does-paver-sealing-last-in-florida',
    '/learning-center/local/why-pavers-fail-faster-near-the-beach': '/learning-center/sealing/how-long-does-paver-sealing-last-in-florida',
    '/learning-center/warranty/why-we-use-trident-products-only': '/learning-center/sealing/how-to-choose-the-right-paver-sealer-for-your-home',
    '/learning-center/warranty/why-hydroseal-uses-trident-products-only': '/learning-center/sealing/how-to-choose-the-right-paver-sealer-for-your-home',
}

changed = []
for path in Path('.').rglob('*.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    original = text
    for old, new in MAPPING.items():
        text = text.replace(old, new)
    # Replace retired category landing links with the final directory.
    for category in ('cleaning','local','maintenance','problems','sealing','search','surfaces','travertine','video-tutorials','warranty'):
        text = text.replace(f'/learning-center/{category}"', '/learning-center"')
        text = text.replace(f'/learning-center/{category}/"', '/learning-center"')
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(str(path))
print(f'Updated {len(changed)} files')

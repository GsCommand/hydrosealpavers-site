#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.git', 'node_modules'}
CHECK_ONLY = '--check' in sys.argv

MODERN_COLUMNS = (
    '<div class="hs-modern-column">'
    '<a href="/paver-sealing/driveways">Driveway Paver Sealing<small>Clean, resand, and protect</small></a>'
    '<a href="/paver-sealing/pool-decks">Pool Deck Sealing<small>Moisture-aware preparation</small></a>'
    '<a href="/paver-sealing/travertine-sealing">Travertine Sealing<small>Natural-stone specific care</small></a>'
    '<a href="/paver-resealing/">Paver Resealing<small>Restore weathered protection</small></a>'
    '</div>'
    '<div class="hs-modern-column">'
    '<a href="/paver-cleaning">Paver Cleaning<small>Surface-safe preparation and cleaning</small></a>'
    '<a href="/paver-repair">Paver Repair<small>Small repairs and paver re-leveling</small></a>'
    '<a href="/paver-sealing/sand-options">Joint Sand Options<small>ASTM C144 colors and selection</small></a>'
    '<a href="/paver-sealing-cost-calculator">Instant Pricing Calculator<small>Estimate standard sealing cost</small></a>'
    '</div>'
)

LEGACY_COLUMNS = (
    '<div class="mega-column">'
    '<a href="/paver-sealing/driveways">Driveway Paver Sealing<small>Clean, resand, and protect</small></a>'
    '<a href="/paver-sealing/pool-decks">Pool Deck Sealing<small>Moisture-aware preparation</small></a>'
    '<a href="/paver-sealing/travertine-sealing">Travertine Sealing<small>Natural-stone specific care</small></a>'
    '<a href="/paver-resealing/">Paver Resealing<small>Restore weathered protection</small></a>'
    '</div>'
    '<div class="mega-column">'
    '<a href="/paver-cleaning">Paver Cleaning<small>Surface-safe preparation and cleaning</small></a>'
    '<a href="/paver-repair">Paver Repair<small>Small repairs and paver re-leveling</small></a>'
    '<a href="/paver-sealing/sand-options">Joint Sand Options<small>ASTM C144 colors and selection</small></a>'
    '<a href="/paver-sealing-cost-calculator">Instant Pricing Calculator<small>Estimate standard sealing cost</small></a>'
    '</div>'
)

MODERN_RE = re.compile(
    r'(?P<open><button\b[^>]*class=["\'][^"\']*hs-modern-parent[^"\']*["\'][^>]*>\s*Paver Sealing\s*</button>\s*<div\b[^>]*class=["\']hs-modern-mega["\'][^>]*>)'
    r'\s*<div\b[^>]*class=["\']hs-modern-column["\'][^>]*>.*?</div>\s*'
    r'<div\b[^>]*class=["\']hs-modern-column["\'][^>]*>.*?</div>\s*'
    r'(?P<close></div>)',
    re.IGNORECASE | re.DOTALL,
)

LEGACY_RE = re.compile(
    r'(?P<open><button\b[^>]*class=["\'][^"\']*nav-parent[^"\']*["\'][^>]*>\s*Paver Sealing\s*</button>\s*<div\b[^>]*class=["\'][^"\']*mega[^"\']*paver-sealing-menu[^"\']*["\'][^>]*>)'
    r'\s*<div\b[^>]*class=["\']mega-column["\'][^>]*>.*?</div>\s*'
    r'<div\b[^>]*class=["\']mega-column["\'][^>]*>.*?</div>\s*'
    r'(?P<close></div>)',
    re.IGNORECASE | re.DOTALL,
)


def html_files():
    for path in ROOT.rglob('*.html'):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def replace_known_nav(text):
    modern = len(MODERN_RE.findall(text))
    legacy = len(LEGACY_RE.findall(text))
    if modern > 1 or legacy > 1 or (modern and legacy):
        raise RuntimeError('multiple Paver Sealing navigation blocks detected')
    if modern:
        return MODERN_RE.sub(lambda m: m.group('open') + MODERN_COLUMNS + m.group('close'), text, count=1), 'modern'
    if legacy:
        return LEGACY_RE.sub(lambda m: m.group('open') + LEGACY_COLUMNS + m.group('close'), text, count=1), 'legacy'
    return text, None


def main():
    total = direct = modern = legacy = includes = unchanged = 0
    changed = []
    no_header = []
    unrecognized = []
    failures = []

    files = sorted(html_files())
    for path in files:
        total += 1
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding='utf-8')
        has_header_include = bool(re.search(r'<header\b[^>]*data-include=["\']/partials/header\.html["\']', text, re.I))
        try:
            updated, kind = replace_known_nav(text)
        except RuntimeError as exc:
            failures.append(f'{rel}: {exc}')
            continue

        if kind:
            direct += 1
            modern += kind == 'modern'
            legacy += kind == 'legacy'
            menu_match = MODERN_RE.search(updated) if kind == 'modern' else LEGACY_RE.search(updated)
            menu = menu_match.group(0) if menu_match else ''
            required = [
                '/paver-sealing/driveways', '/paver-sealing/pool-decks', '/paver-sealing/travertine-sealing',
                '/paver-resealing/', '/paver-cleaning', '/paver-repair', '/paver-sealing/sand-options',
                '/paver-sealing-cost-calculator'
            ]
            if not all(f'href="{href}"' in menu for href in required):
                failures.append(f'{rel}: updated menu failed 4+4 link verification')
            if menu.count('<a ') != 8:
                failures.append(f'{rel}: Paver Sealing menu has {menu.count("<a ")} links instead of 8')
            if updated != text:
                changed.append(rel)
                if not CHECK_ONLY:
                    path.write_text(updated, encoding='utf-8')
            else:
                unchanged += 1
            continue

        if has_header_include:
            includes += 1
            continue

        # Flag any page that appears to have a site Paver Sealing nav but did not match a known safe pattern.
        if 'Paver Sealing' in text and ('nav-parent' in text or 'hs-modern-parent' in text or 'paver-sealing-menu' in text):
            unrecognized.append(rel)
        else:
            no_header.append(rel)

    partial = ROOT / 'partials/header.html'
    partial_text = partial.read_text(encoding='utf-8')
    partial_updated, partial_kind = replace_known_nav(partial_text)
    if partial_kind != 'modern':
        failures.append('partials/header.html: expected modern Paver Sealing menu not found')
    else:
        partial_menu = MODERN_RE.search(partial_updated)
        if not partial_menu or partial_menu.group(0).count('<a ') != 8:
            failures.append('partials/header.html: 4+4 verification failed')
        if partial_updated != partial_text:
            if 'partials/header.html' not in changed:
                changed.append('partials/header.html')
            if not CHECK_ONLY:
                partial.write_text(partial_updated, encoding='utf-8')

    # Every header-include page is covered by the verified shared partial.
    covered = direct + includes
    print(f'HTML files audited: {total}')
    print(f'Pages with hardcoded recognized nav: {direct} (modern={modern}, legacy={legacy})')
    print(f'Pages using /partials/header.html: {includes}')
    print(f'HTML pages covered by updated 4+4 nav: {covered}')
    print(f'Already exact/unchanged hardcoded navs: {unchanged}')
    print(f'Files requiring changes: {len(changed)}')
    for rel in changed:
        print(f'  CHANGE {rel}')
    print(f'HTML files without site header pattern: {len(no_header)}')
    for rel in no_header:
        print(f'  NO_HEADER {rel}')
    if unrecognized:
        print('Unrecognized navigation files:', file=sys.stderr)
        for rel in unrecognized:
            print(f'  {rel}', file=sys.stderr)
        failures.append(f'{len(unrecognized)} unrecognized navigation file(s)')
    if failures:
        print('Verification failures:', file=sys.stderr)
        for failure in failures:
            print(f'  {failure}', file=sys.stderr)
        raise SystemExit(1)

    if CHECK_ONLY and changed:
        print('Check mode: files still require normalization.', file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.git', 'node_modules'}
CHECK_ONLY = '--check' in sys.argv

ITEMS = [
    ('/paver-sealing/driveways', 'Driveway Paver Sealing', 'Clean, resand, and protect'),
    ('/paver-sealing/pool-decks', 'Pool Deck Sealing', 'Moisture-aware preparation'),
    ('/paver-sealing/travertine-sealing', 'Travertine Sealing', 'Natural-stone specific care'),
    ('/paver-resealing/', 'Paver Resealing', 'Restore weathered protection'),
    ('/paver-cleaning', 'Paver Cleaning', 'Surface-safe preparation and cleaning'),
    ('/paver-repair', 'Paver Repair', 'Small repairs and paver re-leveling'),
    ('/paver-sealing/sand-options', 'Joint Sand Options', 'ASTM C144 colors and selection'),
    ('/paver-sealing-cost-calculator', 'Instant Pricing Calculator', 'Estimate standard sealing cost'),
]

MODERN_COLUMNS = (
    '<div class="hs-modern-column">' + ''.join(
        f'<a href="{href}">{label}<small>{small}</small></a>' for href, label, small in ITEMS[:4]
    ) + '</div>'
    '<div class="hs-modern-column">' + ''.join(
        f'<a href="{href}">{label}<small>{small}</small></a>' for href, label, small in ITEMS[4:]
    ) + '</div>'
)

LEGACY_COLUMNS = (
    '<div class="mega-column">' + ''.join(
        f'<a href="{href}">{label}<small>{small}</small></a>' for href, label, small in ITEMS[:4]
    ) + '</div>'
    '<div class="mega-column">' + ''.join(
        f'<a href="{href}">{label}<small>{small}</small></a>' for href, label, small in ITEMS[4:]
    ) + '</div>'
)

SIMPLE_LINKS = ''.join(
    f'<a role="menuitem" href="{href}">{label}<small>{small}</small></a>' for href, label, small in ITEMS
)

MODERN_RE = re.compile(
    r'(?P<open><button\b[^>]*class=["\'][^"\']*hs-modern-parent[^"\']*["\'][^>]*>\s*Paver Sealing\s*</button>\s*'
    r'<div\b[^>]*class=["\'][^"\']*hs-modern-mega[^"\']*["\'][^>]*>)'
    r'\s*<div\b[^>]*class=["\'][^"\']*hs-modern-column[^"\']*["\'][^>]*>.*?</div>\s*'
    r'<div\b[^>]*class=["\'][^"\']*hs-modern-column[^"\']*["\'][^>]*>.*?</div>\s*'
    r'(?P<close></div>)',
    re.IGNORECASE | re.DOTALL,
)

LEGACY_RE = re.compile(
    r'(?P<open><button\b[^>]*class=["\'][^"\']*nav-parent[^"\']*["\'][^>]*>\s*Paver Sealing\s*</button>\s*'
    r'<div\b[^>]*class=["\'][^"\']*mega[^"\']*paver-sealing-menu[^"\']*["\'][^>]*>)'
    r'\s*<div\b[^>]*class=["\'][^"\']*mega-column[^"\']*["\'][^>]*>.*?</div>\s*'
    r'<div\b[^>]*class=["\'][^"\']*mega-column[^"\']*["\'][^>]*>.*?</div>\s*'
    r'(?P<close></div>)',
    re.IGNORECASE | re.DOTALL,
)

SIMPLE_RE = re.compile(
    r'(?P<button><button\b[^>]*class=["\'][^"\']*nav-parent[^"\']*["\'][^>]*>\s*Paver Sealing\s*</button>)\s*'
    r'<div\b(?P<attrs>[^>]*)class=["\'][^"\']*dropdown[^"\']*["\'](?P<attrs2>[^>]*)>.*?</div>',
    re.IGNORECASE | re.DOTALL,
)

STYLE_MARKER = '/* Sitewide Paver Sealing 4+4 dropdown */'
STYLE_BLOCK = r'''

/* Sitewide Paver Sealing 4+4 dropdown */
@media (min-width:981px){
  .dropdown.paver-sealing-menu{
    min-width:560px;
    grid-template-columns:repeat(2,minmax(250px,1fr));
    grid-template-rows:repeat(4,auto);
    grid-auto-flow:column;
    gap:4px 12px;
  }
  .nav-group:hover .dropdown.paver-sealing-menu,
  .nav-group:focus-within .dropdown.paver-sealing-menu,
  .nav-group.open .dropdown.paver-sealing-menu{display:grid}
}
.dropdown.paver-sealing-menu a{min-width:0}
.dropdown.paver-sealing-menu a small{display:block;margin-top:2px;font-size:11px;line-height:1.3;font-weight:600;opacity:.72}
@media (max-width:980px){
  .dropdown.paver-sealing-menu{grid-template-columns:1fr;grid-auto-flow:row;min-width:0;max-width:none}
  .nav-group.open .dropdown.paver-sealing-menu{display:block}
}
'''


def html_files():
    for path in ROOT.rglob('*.html'):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def simple_replacement(match):
    attrs = (match.group('attrs') + ' ' + match.group('attrs2')).strip()
    # Preserve non-class attributes from the existing dropdown, but normalize the class.
    attrs = re.sub(r'\s*class=["\'][^"\']*["\']', '', attrs, flags=re.I)
    attrs = re.sub(r'\s+', ' ', attrs).strip()
    extra = f' {attrs}' if attrs else ''
    return match.group('button') + f'<div class="dropdown paver-sealing-menu"{extra}>' + SIMPLE_LINKS + '</div>'


def replace_known_nav(text):
    counts = {
        'modern': len(MODERN_RE.findall(text)),
        'legacy': len(LEGACY_RE.findall(text)),
        'simple': len(SIMPLE_RE.findall(text)),
    }
    found = [kind for kind, count in counts.items() if count]
    if any(count > 1 for count in counts.values()) or len(found) > 1:
        raise RuntimeError(f'multiple Paver Sealing navigation blocks detected: {counts}')
    if counts['modern']:
        return MODERN_RE.sub(lambda m: m.group('open') + MODERN_COLUMNS + m.group('close'), text, count=1), 'modern'
    if counts['legacy']:
        return LEGACY_RE.sub(lambda m: m.group('open') + LEGACY_COLUMNS + m.group('close'), text, count=1), 'legacy'
    if counts['simple']:
        return SIMPLE_RE.sub(simple_replacement, text, count=1), 'simple'
    return text, None


def extract_menu(text, kind):
    pattern = {'modern': MODERN_RE, 'legacy': LEGACY_RE, 'simple': SIMPLE_RE}[kind]
    match = pattern.search(text)
    return match.group(0) if match else ''


def verify_menu(rel, menu, failures):
    for href, _label, _small in ITEMS:
        if f'href="{href}"' not in menu:
            failures.append(f'{rel}: missing {href} from Paver Sealing menu')
    if menu.count('<a ') != 8:
        failures.append(f'{rel}: Paver Sealing menu has {menu.count("<a ")} links instead of 8')
    # Enforce the requested order, which gives 4 left + 4 right for modern/legacy
    # and column-flow 4+4 for the simple dropdown CSS.
    positions = [menu.find(f'href="{href}"') for href, _label, _small in ITEMS]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        failures.append(f'{rel}: Paver Sealing menu is not in the requested 4+4 order')


def main():
    total = direct = modern = legacy = simple = includes = unchanged = 0
    changed = []
    no_header = []
    unrecognized = []
    failures = []

    files = sorted(html_files())
    for path in files:
        total += 1
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding='utf-8')
        has_header_include = bool(re.search(r'<[^>]+\bdata-include=["\']/partials/header\.html["\'][^>]*>', text, re.I))
        try:
            updated, kind = replace_known_nav(text)
        except RuntimeError as exc:
            failures.append(f'{rel}: {exc}')
            continue

        if kind:
            direct += 1
            modern += kind == 'modern'
            legacy += kind == 'legacy'
            simple += kind == 'simple'
            verify_menu(rel, extract_menu(updated, kind), failures)
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

        # Fail rather than silently skip a Paver Sealing navigation we do not recognize.
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
        verify_menu('partials/header.html', extract_menu(partial_updated, 'modern'), failures)
        if partial_updated != partial_text:
            if 'partials/header.html' not in changed:
                changed.append('partials/header.html')
            if not CHECK_ONLY:
                partial.write_text(partial_updated, encoding='utf-8')

    styles = ROOT / 'styles.css'
    style_text = styles.read_text(encoding='utf-8')
    if STYLE_MARKER not in style_text:
        if CHECK_ONLY:
            failures.append('styles.css: missing 4+4 rules for legacy/simple dropdown pages')
        else:
            styles.write_text(style_text.rstrip() + STYLE_BLOCK + '\n', encoding='utf-8')
            changed.append('styles.css')

    covered = direct + includes
    print(f'HTML files audited: {total}')
    print(f'Pages with hardcoded recognized nav: {direct} (modern={modern}, legacy={legacy}, simple={simple})')
    print(f'Pages using /partials/header.html: {includes}')
    print(f'HTML pages covered by updated 4+4 nav: {covered}')
    print(f'Already exact/unchanged hardcoded navs: {unchanged}')
    print(f'Files requiring changes: {len(changed)}')
    for rel in changed:
        print(f'  CHANGE {rel}')
    print(f'HTML files without a site header: {len(no_header)}')
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

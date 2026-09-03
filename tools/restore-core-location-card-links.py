from pathlib import Path
import re


def replace_once(text, pattern, repl, label):
    new, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 replacement, got {count}')
    return new

# Main Service Areas hub: restore all four primary market cards as actual links.
p = Path('service-areas/index.html')
s = p.read_text(encoding='utf-8')
county_grid = '''        <div class="county-grid">
          <a class="county-card" href="/service-areas/jacksonville">
            <div class="county-card__media"><img src="/assets/hero/paversealing-jacksonville.webp" alt="Jacksonville paver sealing service area" loading="lazy" decoding="async" /></div>
            <div class="county-card__body">
              <h3>Jacksonville &amp; Duval County</h3>
              <p>Coverage across Jacksonville, Jacksonville Beach, Mandarin and Southside, with smaller Duval neighborhoods covered inside the closest core page.</p>
              <span class="county-card__link">Explore Jacksonville coverage →</span>
            </div>
          </a>

          <a class="county-card" href="/service-areas/st-johns-county">
            <div class="county-card__media"><img src="/assets/hero/paversealing-stjohns.png" alt="St. Johns County paver sealing service area" loading="lazy" decoding="async" /></div>
            <div class="county-card__body">
              <h3>St. Johns County</h3>
              <p>Dedicated coverage for Nocatee, Ponte Vedra, Ponte Vedra Beach, Julington Creek, Fruit Cove, Durbin Crossing and TrailMark.</p>
              <span class="county-card__link">Explore St. Johns County →</span>
            </div>
          </a>

          <a class="county-card" href="/service-areas/clay-county">
            <div class="county-card__media"><img src="/assets/hero/paver-sealing-jacksonville-driveway.webp" alt="Clay County paver driveway sealing" loading="lazy" decoding="async" /></div>
            <div class="county-card__body">
              <h3>Clay County</h3>
              <p>Dedicated coverage for Fleming Island, Orange Park, Oakleaf Plantation and Middleburg, with Green Cove Springs covered by the county hub.</p>
              <span class="county-card__link">Explore Clay County coverage →</span>
            </div>
          </a>

          <a class="county-card" href="/service-areas/yulee">
            <div class="county-card__media"><img src="/assets/hero/hydroseal-driveway.webp" alt="Yulee and Wildlight paver sealing service area" loading="lazy" decoding="async" /></div>
            <div class="county-card__body">
              <h3>Yulee &amp; Wildlight</h3>
              <p>Dedicated Nassau County coverage for Yulee and Wildlight driveways, patios, pool decks and walkways.</p>
              <span class="county-card__link">Explore Yulee &amp; Wildlight →</span>
            </div>
          </a>
        </div>'''
s = replace_once(s, r'        <div class="county-grid">.*?        </div>\n      </div>\n    </section>', county_grid + '\n      </div>\n    </section>', 'main county grid')

# Restore the Nassau core link if it was unwrapped by the retired-neighborhood cleanup.
s = re.sub(
    r'(<div class="community-group">\s*<h3>Nassau County</h3>)\s*(?:<a[^>]*href="/service-areas/yulee"[^>]*>)?Yulee &amp; Wildlight(?:</a>)?\s*(</div>)',
    r'\1\n            <a href="/service-areas/yulee">Yulee &amp; Wildlight</a>\n          \2',
    s,
    count=1,
    flags=re.S,
)
p.write_text(s, encoding='utf-8')

# Jacksonville hub: restore the 3 dedicated child cards. Coverage communities remain plain text below.
p = Path('service-areas/jacksonville/index.html')
s = p.read_text(encoding='utf-8')
jax_grid = '''      <div class="county-area-grid">
        <a class="card service-card featured-card" href="/service-areas/jacksonville/jacksonville-beach">
          <h3>Jacksonville Beach</h3>
          <p>Core Beaches page for Jacksonville Beach, with Atlantic Beach and Neptune Beach covered inside the same market.</p>
          <strong>View Jacksonville Beach <span class="arrow" aria-hidden="true">→</span></strong>
        </a>

        <a class="card service-card featured-card" href="/service-areas/jacksonville/mandarin">
          <h3>Mandarin</h3>
          <p>Dedicated Mandarin page for shaded driveways, patios, walkways and pool-deck pavers.</p>
          <strong>View Mandarin <span class="arrow" aria-hidden="true">→</span></strong>
        </a>

        <a class="card service-card featured-card" href="/service-areas/jacksonville/southside">
          <h3>Southside</h3>
          <p>Core Southside page serving Deerwood, eTown, Glen Kernan, Pablo Creek Reserve, Tamaya and nearby communities.</p>
          <strong>View Southside <span class="arrow" aria-hidden="true">→</span></strong>
        </a>
      </div>'''
s = replace_once(s, r'      <div class="county-area-grid">.*?      </div>\n    </div>\n    <div class="card"', jax_grid + '\n    </div>\n    <div class="card"', 'Jacksonville core card grid')
p.write_text(s, encoding='utf-8')

# Verify the exact card links across all core hubs.
checks = {
    'service-areas/index.html': [
        'class="county-card" href="/service-areas/jacksonville"',
        'class="county-card" href="/service-areas/st-johns-county"',
        'class="county-card" href="/service-areas/clay-county"',
        'class="county-card" href="/service-areas/yulee"',
        '<a href="/service-areas/yulee">Yulee &amp; Wildlight</a>',
    ],
    'service-areas/jacksonville/index.html': [
        'href="/service-areas/jacksonville/jacksonville-beach"',
        'href="/service-areas/jacksonville/mandarin"',
        'href="/service-areas/jacksonville/southside"',
    ],
    'service-areas/st-johns-county/index.html': [
        'href="/service-areas/st-johns-county/nocatee"',
        'href="/service-areas/st-johns-county/ponte-vedra"',
        'href="/service-areas/st-johns-county/ponte-vedra-beach"',
        'href="/service-areas/st-johns-county/julington-creek"',
        'href="/service-areas/st-johns-county/fruit-cove"',
        'href="/service-areas/st-johns-county/durbin-crossing"',
        'href="/service-areas/st-johns-county/trailmark"',
    ],
    'service-areas/clay-county/index.html': [
        'href="/service-areas/clay-county/fleming-island"',
        'href="/service-areas/clay-county/oakleaf-plantation"',
        'href="/service-areas/clay-county/orange-park"',
        'href="/service-areas/clay-county/middleburg"',
    ],
}
for filename, needles in checks.items():
    text = Path(filename).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'{filename}: missing required core card/link: {needle}')

print('Core service-area card links restored and verified.')

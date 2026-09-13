from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed = []


def replace_once(rel, old, new):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Expected text not found in {rel}: {old[:120]}")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    changed.append(rel)

# 1) Strong weather/cure guide -> resealing/restoration service.
replace_once(
    "learning-center/sealing/rain-after-paver-sealing/index.html",
    '<section><h2>What should homeowners do?</h2><p>Keep vehicles, sprinklers and unnecessary traffic off the surface. Allow conditions to dry. Photograph affected areas and contact the installer. Avoid adding cleaners, solvents or more sealer without knowing the coating chemistry.</p></section>',
    '<section><h2>What should homeowners do?</h2><p>Keep vehicles, sprinklers and unnecessary traffic off the surface. Allow conditions to dry. Photograph affected areas and contact the installer. Avoid adding cleaners, solvents or more sealer without knowing the coating chemistry. If the existing coating is already cloudy, peeling, or otherwise failing, review HydroSeal’s <a href="/paver-resealing">paver resealing and restoration service</a> before another coat is considered.</p></section>'
)

# 2) Strong traction guide -> pool-deck money page.
replace_once(
    "learning-center/problems/why-are-my-pavers-slippery-after-sealing/index.html",
    '<p>A semi-gloss wet-look finish is not automatically unsafe, but surface texture, film thickness, additive choice, cleaning, drainage, and maintenance all affect wet traction.</p>',
    '<p>A semi-gloss wet-look finish is not automatically unsafe, but surface texture, film thickness, additive choice, cleaning, drainage, and maintenance all affect wet traction. For surface-specific preparation and traction planning, see HydroSeal’s <a href="/paver-sealing/pool-decks">pool deck paver sealing service</a>.</p>'
)

# 3) Pool-deck sealer guide -> pool-deck money page.
replace_once(
    "learning-center/surfaces/best-sealer-for-pool-decks-slip-safety-and-durability/index.html",
    '<p>Pool decks in <a href="/service-areas/st-johns-county/nocatee">Nocatee</a>, <a href="/service-areas/st-johns-county/ponte-vedra">Ponte Vedra</a>, <a href="/service-areas/jacksonville/jacksonville-beach">Jacksonville Beach</a>, and other Northeast Florida communities may face strong sun, coastal salt, irrigation, screen-enclosure shade, and frequent wet-dry cycles. These conditions make breathability, traction, and cure timing more important than headline gloss.</p>',
    '<p>Pool decks in <a href="/service-areas/st-johns-county/nocatee">Nocatee</a>, <a href="/service-areas/st-johns-county/ponte-vedra">Ponte Vedra</a>, <a href="/service-areas/jacksonville/jacksonville-beach">Jacksonville Beach</a>, and other Northeast Florida communities may face strong sun, coastal salt, irrigation, screen-enclosure shade, and frequent wet-dry cycles. These conditions make breathability, traction, and cure timing more important than headline gloss. For the local service scope, see <a href="/paver-sealing/pool-decks">Pool Deck Paver Sealing in Jacksonville</a>.</p>'
)

# 4) White-sealer troubleshooting -> efflorescence and resealing services.
replace_once(
    "learning-center/problems/why-are-my-pavers-turning-white-in-florida/index.html",
    '<section><h2>What HydroSeal does</h2><p>HydroSeal evaluates the pattern, texture, coating condition, low areas, irrigation coverage, drainage, moisture history, and previous products before recommending treatment. Improvement is often possible, but complete removal and non-recurrence cannot be guaranteed without understanding the cause.</p></section>',
    '<section><h2>What HydroSeal does</h2><p>HydroSeal evaluates the pattern, texture, coating condition, low areas, irrigation coverage, drainage, moisture history, and previous products before recommending treatment. Improvement is often possible, but complete removal and non-recurrence cannot be guaranteed without understanding the cause. When testing points to mineral deposits, see our <a href="/paver-efflorescence-removal">paver efflorescence removal service</a>. When the problem is inside a failed coating, review <a href="/paver-resealing">paver resealing and restoration</a>.</p></section>'
)

# 5) Efflorescence guide -> dedicated efflorescence service.
replace_once(
    "learning-center/problems/what-causes-efflorescence-on-pavers/index.html",
    '<p>HydroSeal provides condition-based evaluation for selected properties across <a href="/service-areas/jacksonville">Jacksonville</a>, <a href="/service-areas/st-johns-county/nocatee">Nocatee</a>, <a href="/service-areas/st-johns-county/ponte-vedra">Ponte Vedra</a>, and nearby Northeast Florida communities. Treatment can improve appearance, but full removal and permanent prevention cannot always be guaranteed.</p>',
    '<p>HydroSeal provides condition-based evaluation for selected properties across <a href="/service-areas/jacksonville">Jacksonville</a>, <a href="/service-areas/st-johns-county/nocatee">Nocatee</a>, <a href="/service-areas/st-johns-county/ponte-vedra">Ponte Vedra</a>, and nearby Northeast Florida communities. Treatment can improve appearance, but full removal and permanent prevention cannot always be guaranteed. For contractor service details, see <a href="/paver-efflorescence-removal">Paver Efflorescence Removal in Jacksonville</a>.</p>'
)

# 6) Strip/reseal cost guide -> dedicated resealing service.
replace_once(
    "learning-center/cost/how-much-does-it-cost-to-strip-and-reseal-pavers/index.html",
    '<p>Do not assume every faded driveway needs complete removal. If the existing coating is still bonded and chemically compatible, a professional may recommend cleaning, preparation, joint-sand restoration, and a controlled recoat. That is why the first decision should be <a href="/learning-center/problems/cleaning-resealing-or-stripping">cleaning, resealing, or stripping</a>—not automatically choosing the most aggressive option.</p>',
    '<p>Do not assume every faded driveway needs complete removal. If the existing coating is still bonded and chemically compatible, a professional may recommend cleaning, preparation, joint-sand restoration, and a controlled recoat. That is why the first decision should be <a href="/learning-center/problems/cleaning-resealing-or-stripping">cleaning, resealing, or stripping</a>—not automatically choosing the most aggressive option. For the contractor service scope, see <a href="/paver-resealing">Paver Resealing &amp; Restoration</a>.</p>'
)

# 7) Hiring guide -> the three surviving county/city service hubs.
replace_once(
    "learning-center/hiring/how-to-choose-a-paver-sealing-company-in-northeast-florida/index.html",
    '<h2>Local experience matters, but proximity is not enough</h2><p>Jacksonville, Nocatee, Ponte Vedra, Palm Valley, the Beaches, and Clay County share heat and rain, but properties differ in irrigation, shade, drainage, salt exposure, pool chemicals, traffic, and paver type. A contractor should explain the conditions at your property rather than relying on a generic “Florida-proof” process.</p>',
    '<h2>Local experience matters, but proximity is not enough</h2><p><a href="/service-areas/jacksonville">Jacksonville</a>, <a href="/service-areas/st-johns-county">St. Johns County</a>, and <a href="/service-areas/clay-county">Clay County</a> share heat and rain, but properties differ in irrigation, shade, drainage, salt exposure, pool chemicals, traffic, and paver type. A contractor should explain the conditions at your property rather than relying on a generic “Florida-proof” process.</p>'
)

# 8) Resealing lifespan guide -> dedicated resealing service.
replace_once(
    "learning-center/sealing/how-long-does-paver-sealing-last-in-florida/index.html",
    '<section><h2>Signs it may be time to reseal</h2><ul><li>Uneven color loss or exposed wear lanes</li><li>Water absorption increasing across previously protected areas</li><li>Joint sand washing out or becoming unstable</li><li>Coating thinning without peeling or whitening</li><li>Stains becoming harder to clean</li><li>Pool-deck or driveway areas wearing differently from sheltered sections</li></ul></section>',
    '<section><h2>Signs it may be time to reseal</h2><ul><li>Uneven color loss or exposed wear lanes</li><li>Water absorption increasing across previously protected areas</li><li>Joint sand washing out or becoming unstable</li><li>Coating thinning without peeling or whitening</li><li>Stains becoming harder to clean</li><li>Pool-deck or driveway areas wearing differently from sheltered sections</li></ul><p>If the existing coating is wearing but remains stable, start with HydroSeal’s <a href="/paver-resealing">paver resealing service</a> to understand the inspection and preparation scope.</p></section>'
)

# 9) High-impression driveway cost guide -> driveway service + calculator.
replace_once(
    "learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot/index.html",
    '<section><h2>The basic cost formula</h2><p><strong>Measured paver area × applicable project rate + restoration or repair scope = estimated project cost.</strong></p><p>The applicable rate changes with surface type and condition. A straightforward clean, joint-sand restoration, and seal project is different from failed-coating removal, heavy stain treatment, sunken-paver repair, or natural-stone work.</p></section>',
    '<section><h2>The basic cost formula</h2><p><strong>Measured paver area × applicable project rate + restoration or repair scope = estimated project cost.</strong></p><p>The applicable rate changes with surface type and condition. A straightforward clean, joint-sand restoration, and seal project is different from failed-coating removal, heavy stain treatment, sunken-paver repair, or natural-stone work. See <a href="/paver-sealing/driveways">Driveway Paver Sealing in Jacksonville</a> for the service scope, or use the <a href="/paver-sealing-cost-calculator">paver sealing cost calculator</a> for a quick planning estimate.</p></section>'
)

# 10) Remove a link hop: Palm Valley is already consolidated into Ponte Vedra.
replace_once(
    "learning-center/travertine/how-to-clean-travertine-without-damage/index.html",
    '<a href="/service-areas/st-johns-county/palm-valley">Palm Valley</a>',
    '<a href="/service-areas/st-johns-county/ponte-vedra">Ponte Vedra</a>'
)

# Validation: no homepage title/H1 or service-page title/H1 edits are part of this sprint.
for forbidden in [
    ROOT / "index.html",
    ROOT / "service-areas/jacksonville/index.html",
    ROOT / "paver-sealing/driveways.html",
    ROOT / "paver-sealing/pool-decks.html",
    ROOT / "paver-sealing/travertine-sealing.html",
    ROOT / "paver-resealing/index.html",
]:
    if str(forbidden.relative_to(ROOT)) in changed:
        raise SystemExit(f"Unexpected money-page content edit: {forbidden}")

required = {
    "learning-center/sealing/rain-after-paver-sealing/index.html": '/paver-resealing',
    "learning-center/problems/why-are-my-pavers-slippery-after-sealing/index.html": '/paver-sealing/pool-decks',
    "learning-center/surfaces/best-sealer-for-pool-decks-slip-safety-and-durability/index.html": '/paver-sealing/pool-decks',
    "learning-center/problems/why-are-my-pavers-turning-white-in-florida/index.html": '/paver-efflorescence-removal',
    "learning-center/problems/what-causes-efflorescence-on-pavers/index.html": '/paver-efflorescence-removal',
    "learning-center/cost/how-much-does-it-cost-to-strip-and-reseal-pavers/index.html": '/paver-resealing',
    "learning-center/hiring/how-to-choose-a-paver-sealing-company-in-northeast-florida/index.html": '/service-areas/jacksonville',
    "learning-center/sealing/how-long-does-paver-sealing-last-in-florida/index.html": '/paver-resealing',
    "learning-center/surfaces/driveway-paver-sealing-cost-per-square-foot/index.html": '/paver-sealing/driveways',
    "learning-center/travertine/how-to-clean-travertine-without-damage/index.html": '/service-areas/st-johns-county/ponte-vedra',
}
for rel, href in required.items():
    if f'href="{href}"' not in (ROOT / rel).read_text(encoding="utf-8"):
        raise SystemExit(f"Required link missing after edit: {rel} -> {href}")

print("Changed files:")
for rel in changed:
    print(f"- {rel}")
print(f"Total changed content files: {len(changed)}")

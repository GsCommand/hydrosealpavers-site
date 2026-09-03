from pathlib import Path
import json
import re

CSS_LINK = '<link rel="stylesheet" href="/assets/css/core-location-v3.css?v=20260903" />'


def faq_schema(url, questions):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in questions
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":")) + '</script>'


def remove_faq_schema(text):
    pattern = re.compile(r'<script\s+type="application/ld\+json"[^>]*>.*?</script>', re.S | re.I)
    kept = []
    pos = 0
    for match in pattern.finditer(text):
        kept.append(text[pos:match.start()])
        block = match.group(0)
        if '"FAQPage"' not in block and '"@type": "FAQPage"' not in block:
            kept.append(block)
        pos = match.end()
    kept.append(text[pos:])
    return ''.join(kept)


def set_meta(text, title, description):
    text = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', text, count=1, flags=re.S | re.I)
    text = re.sub(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>', f'<meta name="description" content="{description}" />', text, count=1, flags=re.I)
    text = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>', f'<meta property="og:title" content="{title}" />', text, count=1, flags=re.I)
    text = re.sub(r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>', f'<meta property="og:description" content="{description}" />', text, count=1, flags=re.I)
    text = re.sub(r'<meta\s+name="twitter:title"\s+content="[^"]*"\s*/?>', f'<meta name="twitter:title" content="{title}" />', text, count=1, flags=re.I)
    text = re.sub(r'<meta\s+name="twitter:description"\s+content="[^"]*"\s*/?>', f'<meta name="twitter:description" content="{description}" />', text, count=1, flags=re.I)
    return text


def rebuild(path, title, description, main_html, questions):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    text = set_meta(text, title, description)
    text = remove_faq_schema(text)
    if CSS_LINK not in text:
        text = text.replace('</head>', f'  {CSS_LINK}\n  {faq_schema("https://hydrosealpavers.com/" + path.replace("index.html", "").replace(".html", "").rstrip("/"), questions)}\n</head>', 1)
    else:
        text = text.replace('</head>', f'  {faq_schema("https://hydrosealpavers.com/" + path.replace("index.html", "").replace(".html", "").rstrip("/"), questions)}\n</head>', 1)
    pattern = re.compile(r'<main\s+id="page"\s+data-page[^>]*>.*?</main>', re.S | re.I)
    text, count = pattern.subn(main_html, text, count=1)
    if count != 1:
        raise SystemExit(f'{path}: expected one main replacement, got {count}')
    p.write_text(text, encoding='utf-8')


TRUST = '''
<section class="loc-trust hs-reminder-badges" aria-label="HydroSeal service standards">
  <div class="loc-shell loc-trust-grid">
    <div>Licensed &amp; Insured</div>
    <div>Trident Master Certified</div>
    <div>ASTM C144 Joint Sand</div>
    <div>2-Year Workmanship Warranty</div>
  </div>
</section>
'''

JAX_MAIN = r'''
<main id="page" data-page class="loc-page loc-jax">
  <section class="loc-jax-hero">
    <img src="/assets/hero/paversealing-jacksonville.webp" alt="Professionally sealed paver driveway in Jacksonville Florida" width="1600" height="900" loading="eager" decoding="async" fetchpriority="high" />
    <div class="loc-shell loc-jax-hero__inner">
      <div class="loc-jax-hero__panel">
        <span class="loc-eyebrow" style="color:#7dd7f3;">Jacksonville &amp; Duval County</span>
        <h1>Jacksonville Paver Sealing Built for Florida Exposure</h1>
        <p>HydroSeal restores and seals paver driveways, pool decks, patios and walkways across Jacksonville. The process changes with the property: beach-side salt air, Southside sun exposure, Mandarin tree canopy, irrigation runoff and older joint systems all create different prep requirements.</p>
        <div class="loc-btn-row"><a class="loc-btn loc-btn--blue" href="/get-a-quote">Request a Quote</a><a class="loc-btn loc-btn--white" href="tel:+19045375000">Call 904.537.5000</a></div>
      </div>
    </div>
  </section>

  <div class="loc-shell loc-jax-proof">
    <div class="loc-jax-proof__grid">
      <div><strong>Deep Cleaning</strong><span>Surface prep before sealing</span></div>
      <div><strong>Joint Restoration</strong><span>ASTM C144 kiln-dried sand</span></div>
      <div><strong>Breathable Sealing</strong><span>Controlled Trident application</span></div>
      <div><strong>Local Warranty</strong><span>2-year workmanship coverage</span></div>
    </div>
  </div>

  <section class="loc-section">
    <div class="loc-shell loc-jax-matrix">
      <div class="loc-jax-matrix__intro">
        <span class="loc-eyebrow">Why Jacksonville is different</span>
        <h2>One city. Four very different paver environments.</h2>
        <p class="loc-lede">Jacksonville is too large to treat every hardscape the same. The right prep depends on where the property sits, how water moves across it, how much shade it receives and whether the surface is a driveway, pool deck or natural stone.</p>
        <div class="loc-btn-row"><a class="loc-btn loc-btn--outline" href="/paver-sealing">View All Paver Sealing Services</a></div>
      </div>
      <div class="loc-jax-matrix__grid">
        <article class="loc-card"><b>The Beaches</b><h3>Salt air + strong sun</h3><p>Jacksonville Beach, Atlantic Beach and Neptune Beach surfaces see intense UV, wind-driven moisture and coastal exposure. Fading and joint loss can show up faster on open driveways and pool surrounds.</p></article>
        <article class="loc-card"><b>Mandarin</b><h3>Shade + mature tree canopy</h3><p>Older neighborhoods often hold moisture longer. Organic buildup, leaf tannins and darkened joints become the prep problem before the sealer ever comes out.</p></article>
        <article class="loc-card"><b>Southside</b><h3>Large driveways + daily traffic</h3><p>Deerwood, eTown, Glen Kernan, Pablo Creek Reserve and Tamaya commonly combine large visible hardscapes with frequent vehicle use, irrigation and full-sun exposure.</p></article>
        <article class="loc-card"><b>Older Jacksonville</b><h3>Drainage + mixed surface age</h3><p>Ortega, Riverside/Avondale, Bartram Park and established neighborhoods can have older pavers, repairs, tree roots, drainage changes and mixed previous coatings that require more evaluation.</p></article>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell">
      <span class="loc-eyebrow">Dedicated Jacksonville pages</span>
      <h2>Start with the market closest to your property</h2>
      <div class="loc-jax-markets">
        <a class="loc-card loc-card-link" href="/service-areas/jacksonville/jacksonville-beach"><img src="/assets/hero/jacksonville-pool-paver-sealing.jpg" alt="Jacksonville Beach paver and pool deck sealing" loading="lazy" width="900" height="600" /><div class="copy"><h3>Jacksonville Beach</h3><p>Our core Beaches page for Jacksonville Beach with Atlantic Beach and Neptune Beach covered inside the same coastal market.</p></div></a>
        <a class="loc-card loc-card-link" href="/service-areas/jacksonville/mandarin"><img src="/assets/hero/brickpaver-driveway.jpeg" alt="Mandarin Jacksonville paver driveway sealing" loading="lazy" width="900" height="600" /><div class="copy"><h3>Mandarin</h3><p>Local guidance for shaded driveways, tree-covered patios, pool decks and older Jacksonville paver installations.</p></div></a>
        <a class="loc-card loc-card-link" href="/service-areas/jacksonville/southside"><img src="/assets/hero/paver-sealing-jacksonville-driveway.webp" alt="Southside Jacksonville paver sealing" loading="lazy" width="900" height="600" /><div class="copy"><h3>Southside</h3><p>The primary page for Southside communities including Deerwood, eTown, Glen Kernan, Pablo Creek Reserve and Tamaya.</p></div></a>
      </div>
      <p class="loc-lede" style="margin-top:22px;">HydroSeal also serves Ortega, Riverside/Avondale, Bartram Park, Queens Harbour and other selected Duval County neighborhoods through the Jacksonville hub rather than creating a separate thin page for every subdivision.</p>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell">
      <span class="loc-eyebrow">Choose the service</span>
      <h2>Jacksonville paver restoration by surface type</h2>
      <div class="loc-jax-services">
        <a class="loc-card" href="/paver-sealing/driveways"><span>Driveways</span><h3>Clean, re-sand &amp; seal</h3><p>Built around tire traffic, oil exposure, runoff, joint loss and the curb-appeal impact of a large front driveway.</p></a>
        <a class="loc-card" href="/paver-sealing/pool-decks"><span>Pool Decks</span><h3>Moisture-aware preparation</h3><p>Pool areas need careful cleaning, dry-time control and an application plan that respects walking surfaces and water exposure.</p></a>
        <a class="loc-card" href="/paver-sealing/patios-walkways"><span>Patios &amp; Walkways</span><h3>Shade and organics matter</h3><p>Leaf tannins, mildew, tree cover and irrigation create very different restoration needs than an open-sun driveway.</p></a>
        <a class="loc-card" href="/paver-sealing/travertine-sealing"><span>Natural Stone</span><h3>Travertine-specific sealing</h3><p>Travertine is evaluated separately from concrete pavers because porosity, moisture and finish expectations are different.</p></a>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell">
      <span class="loc-eyebrow">The HydroSeal process</span>
      <h2>What happens before the final coat</h2>
      <div class="loc-jax-process">
        <article><span class="n">01</span><h3>Inspect</h3><p>We look at prior sealer, joint depth, drainage, staining, repairs and the way the property actually gets used.</p></article>
        <article><span class="n">02</span><h3>Deep clean</h3><p>Organic buildup, dirt and problem areas are treated so contamination is not trapped under fresh sealer.</p></article>
        <article><span class="n">03</span><h3>Restore joints</h3><p>Where needed, loose material is removed and joints are reset with ASTM C144 kiln-dried sand.</p></article>
        <article><span class="n">04</span><h3>Seal evenly</h3><p>Trident sealer is applied in controlled passes after the surface is properly prepared and dry enough to accept it.</p></article>
      </div>
      <div class="loc-btn-row"><a class="loc-btn loc-btn--outline" href="/paver-cleaning">Paver Cleaning</a><a class="loc-btn loc-btn--outline" href="/paver-repair">Paver Repair</a><a class="loc-btn loc-btn--outline" href="/paver-resealing">Paver Resealing</a><a class="loc-btn loc-btn--outline" href="/paver-sealing/sand-options">Joint Sand Options</a></div>
    </div>
  </section>

  <section class="loc-section"><div class="loc-shell"><div class="elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26" data-elfsight-app-lazy></div></div></section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell">
      <span class="loc-eyebrow">Jacksonville questions</span><h2>What homeowners usually ask before sealing</h2>
      <div class="loc-faq">
        <details><summary>How often should pavers be sealed in Jacksonville?</summary><div class="answer">There is no single calendar date that fits every Jacksonville property. Full-sun driveways, coastal exposure, heavy traffic and aggressive runoff can wear protection faster than shaded patios. We recommend resealing from actual surface condition rather than applying another coat simply because a certain number of years has passed.</div></details>
        <details><summary>Why does joint sand disappear so quickly on some Jacksonville driveways?</summary><div class="answer">Heavy rain, irrigation overspray, sloped driveways and repeated washing can move joint sand out of the system. Once joints are visibly low, restoring the joints before sealing is more important than simply adding another coat over the surface.</div></details>
        <details><summary>Can algae or mildew be sealed over?</summary><div class="answer">No. Organic growth and contamination should be treated and removed before sealing. Trapping dark growth or residue beneath fresh sealer creates an uneven result and can contribute to premature failure.</div></details>
        <details><summary>Do you seal both driveways and pool decks in Jacksonville?</summary><div class="answer">Yes. HydroSeal works on suitable paver driveways, pool decks, patios and walkways, and also evaluates select travertine surfaces. The prep and product approach changes with the surface and exposure.</div></details>
      </div>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell loc-related">
      <div class="loc-card"><h3>Jacksonville Areas</h3><ul><li><a href="/service-areas/jacksonville/jacksonville-beach">Jacksonville Beach</a></li><li><a href="/service-areas/jacksonville/mandarin">Mandarin</a></li><li><a href="/service-areas/jacksonville/southside">Southside</a></li><li><a href="/service-areas/st-johns-county">St. Johns County</a></li></ul></div>
      <div class="loc-card"><h3>Paver Services</h3><ul><li><a href="/paver-sealing/driveways">Driveway Sealing</a></li><li><a href="/paver-sealing/pool-decks">Pool Deck Sealing</a></li><li><a href="/paver-sealing/travertine-sealing">Travertine Sealing</a></li><li><a href="/paver-sealing-cost-calculator">Pricing Calculator</a></li></ul></div>
      <div class="loc-card"><h3>Planning Guides</h3><ul><li><a href="/learning-center/sealing/what-should-professional-paver-sealing-include">What Professional Sealing Includes</a></li><li><a href="/learning-center/problems/why-is-sand-coming-out-of-my-pavers">Why Joint Sand Comes Out</a></li><li><a href="/learning-center/sealing/how-long-does-paver-sealing-last-in-florida">How Long Sealing Lasts</a></li></ul></div>
    </div>
  </section>

  ''' + TRUST + r'''
  <section class="loc-final"><div class="loc-shell loc-final-inner"><div><span class="loc-eyebrow" style="color:#7dd7f3;">Jacksonville estimates</span><h2>Find out what your pavers actually need.</h2><p>Send the address and a few photos. We can determine whether the surface needs cleaning, fresh joint sand, resealing, repair or a full restoration scope.</p></div><div class="loc-btn-row"><a class="loc-btn loc-btn--blue" href="/get-a-quote">Request a Quote</a><a class="loc-btn loc-btn--white" href="tel:+19045375000">Call HydroSeal</a></div></div></section>
</main>
'''

STJ_MAIN = r'''
<main id="page" data-page class="loc-page loc-stj">
  <section class="loc-stj-hero">
    <div class="loc-shell loc-stj-hero__grid">
      <div class="loc-stj-hero__copy">
        <span class="loc-eyebrow">St. Johns County, Florida</span>
        <h1>Paver Sealing Across St. Johns County</h1>
        <p class="loc-lede">From coastal Ponte Vedra to Nocatee, Julington Creek and the western growth corridor, St. Johns County pavers age differently from neighborhood to neighborhood. HydroSeal adjusts cleaning, joint restoration and sealing around sun exposure, irrigation, humidity, pool environments and the condition of the existing surface.</p>
        <div class="loc-btn-row"><a class="loc-btn loc-btn--navy" href="/get-a-quote">Get a Local Quote</a><a class="loc-btn loc-btn--outline" href="tel:+19045375000">904.537.5000</a></div>
      </div>
      <div class="loc-stj-hero__media"><img src="/assets/hero/st-johns-paver-sealing-nocatee-driveway.webp" alt="Paver driveway sealing in St Johns County Florida" loading="eager" width="1200" height="800" fetchpriority="high" /><div class="loc-stj-hero__note">Driveways • pool decks • patios • walkways • select travertine</div></div>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell">
      <span class="loc-eyebrow">Three local conditions</span><h2>The county changes as you move east to west</h2>
      <div class="loc-stj-corridors">
        <article class="loc-card"><h3>Coastal corridor</h3><p>Ponte Vedra and Ponte Vedra Beach bring more humidity, salt-air exposure, strong sun and pool-deck work. Surfaces often need careful moisture evaluation before sealing.</p></article>
        <article class="loc-card"><h3>Northern communities</h3><p>Nocatee, Durbin Crossing, Fruit Cove and Julington Creek mix newer driveways with established tree canopy, irrigation and larger outdoor-living areas.</p></article>
        <article class="loc-card"><h3>Western growth</h3><p>TrailMark and surrounding growth corridors often have newer paver installations where early joint loss, fading and maintenance timing matter more than heavy coating removal.</p></article>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell">
      <span class="loc-eyebrow">Dedicated St. Johns pages</span><h2>Seven markets we are actively building</h2>
      <div class="loc-stj-areas">
        <a class="loc-card" href="/service-areas/st-johns-county/nocatee"><h3>Nocatee</h3><small>Driveways + pool areas</small></a>
        <a class="loc-card" href="/service-areas/st-johns-county/ponte-vedra"><h3>Ponte Vedra</h3><small>Pavers + travertine</small></a>
        <a class="loc-card" href="/service-areas/st-johns-county/ponte-vedra-beach"><h3>Ponte Vedra Beach</h3><small>Coastal exposure</small></a>
        <a class="loc-card" href="/service-areas/st-johns-county/julington-creek"><h3>Julington Creek</h3><small>Established visibility</small></a>
        <a class="loc-card" href="/service-areas/st-johns-county/fruit-cove"><h3>Fruit Cove</h3><small>Shade + restoration</small></a>
        <a class="loc-card" href="/service-areas/st-johns-county/durbin-crossing"><h3>Durbin Crossing</h3><small>Driveways + patios</small></a>
        <a class="loc-card" href="/service-areas/st-johns-county/trailmark"><h3>TrailMark</h3><small>Western St. Johns</small></a>
      </div>
      <p class="loc-lede" style="margin-top:22px;">Beachwalk, Del Webb Ponte Vedra, Marsh Landing, Murabella, Palencia, Palm Valley, RiverTown, Sawgrass, Shearwater, SilverLeaf and World Golf Village remain part of HydroSeal's St. Johns County coverage and are represented through the closest core market instead of separate thin pages.</p>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell loc-stj-surface">
      <div class="loc-stj-surface__photo"><img src="/assets/hero/hydroseal-travertine-pool-deck-square.webp" alt="Pool deck and natural stone sealing in St Johns County" loading="lazy" width="900" height="900" /></div>
      <div>
        <span class="loc-eyebrow">What we inspect first</span><h2>The surface decides the process.</h2>
        <div class="loc-stj-checks">
          <article><h3>Driveway exposure</h3><p>We look for UV fade, tire traffic, irrigation marks, joint loss, sloped runoff and any old sealer that may affect bonding.</p></article>
          <article><h3>Pool deck moisture</h3><p>Pool surrounds need a different drying and application plan because shade, splash-out and constant moisture can change both prep and cure expectations.</p></article>
          <article><h3>Travertine porosity</h3><p>Natural stone is not treated like concrete pavers. We evaluate absorption, previous products and finish goals before selecting the sealing system.</p></article>
          <article><h3>Joint condition</h3><p>Low, loose or contaminated joints are corrected before sealing when joint restoration is part of the scope.</p></article>
        </div>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell">
      <span class="loc-eyebrow">Service cluster</span><h2>Use the page that matches your surface</h2>
      <div class="loc-related">
        <div class="loc-card"><h3>Hardscape Services</h3><ul><li><a href="/paver-sealing/driveways">Driveway Paver Sealing</a></li><li><a href="/paver-sealing/pool-decks">Pool Deck Sealing</a></li><li><a href="/paver-sealing/patios-walkways">Patio &amp; Walkway Sealing</a></li><li><a href="/paver-sealing/travertine-sealing">Travertine Sealing</a></li></ul></div>
        <div class="loc-card"><h3>Restoration Services</h3><ul><li><a href="/paver-cleaning">Paver Cleaning</a></li><li><a href="/paver-repair">Paver Repair</a></li><li><a href="/paver-resealing">Paver Resealing</a></li><li><a href="/paver-sealing/sand-options">Joint Sand Options</a></li></ul></div>
        <div class="loc-card"><h3>Before You Hire</h3><ul><li><a href="/paver-sealing-cost-calculator">Paver Sealing Cost Calculator</a></li><li><a href="/learning-center/hiring/how-to-choose-a-paver-sealing-company-in-northeast-florida">How to Choose a Company</a></li><li><a href="/learning-center/sealing/what-should-professional-paver-sealing-include">What Sealing Should Include</a></li></ul></div>
      </div>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell">
      <span class="loc-eyebrow">Our workflow</span><h2>A prep-first process for St. Johns County</h2>
      <div class="loc-stj-process">
        <article class="loc-card"><h3>Evaluate the coating and surface</h3><p>We identify whether the surface is unsealed, simply weathered, previously coated or showing a failure that needs a different restoration path.</p></article>
        <article class="loc-card"><h3>Clean for the actual problem</h3><p>Organic growth, irrigation staining, rust, leaf tannins and embedded grime do not all respond to the same cleaning method.</p></article>
        <article class="loc-card"><h3>Rebuild the joints where needed</h3><p>Joint sand is restored after cleaning when the scope calls for it so the surface is stabilized before the sealer is applied.</p></article>
        <article class="loc-card"><h3>Apply the correct sealing system</h3><p>Concrete pavers and natural stone receive different product decisions. Application is controlled for even appearance and appropriate cure time.</p></article>
      </div>
    </div>
  </section>

  <section class="loc-section"><div class="loc-shell"><div class="elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26" data-elfsight-app-lazy></div></div></section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell">
      <span class="loc-eyebrow">St. Johns County FAQ</span><h2>Questions we hear from local homeowners</h2>
      <div class="loc-faq">
        <details><summary>How much does paver sealing cost in St. Johns County?</summary><div class="answer">Pricing depends on square footage, surface condition, access, staining, joint condition, prior coatings and whether the project includes concrete pavers or natural stone. HydroSeal evaluates the actual scope before recommending a final price.</div></details>
        <details><summary>Do Nocatee and Ponte Vedra properties need the same sealing process?</summary><div class="answer">Not necessarily. Coastal humidity, salt exposure, pool environments, shade, drainage and surface material can change the prep and sealing plan even when two homes are only a few miles apart.</div></details>
        <details><summary>Can you seal travertine pool decks in St. Johns County?</summary><div class="answer">HydroSeal evaluates and seals select travertine surfaces. Travertine is handled differently from concrete pavers because stone porosity, moisture and finish expectations require a separate product and prep decision.</div></details>
        <details><summary>Why hire a professional paver sealing company instead of adding another coat?</summary><div class="answer">The condition below the new sealer matters more than the new coat itself. Cleaning, joint stability, moisture, old product compatibility and surface preparation determine whether a new sealing system has a good foundation.</div></details>
      </div>
    </div>
  </section>
  ''' + TRUST + r'''
  <section class="loc-final"><div class="loc-shell loc-final-inner"><div><span class="loc-eyebrow" style="color:#7dd7f3;">St. Johns County service</span><h2>Get the right scope before the surface gets worse.</h2><p>Send the property address and photos of the driveway, pool deck, patio or travertine. HydroSeal can help identify the correct restoration path.</p></div><div class="loc-btn-row"><a class="loc-btn loc-btn--blue" href="/get-a-quote">Request a Quote</a><a class="loc-btn loc-btn--white" href="tel:+19045375000">Call HydroSeal</a></div></div></section>
</main>
'''

CLAY_MAIN = r'''
<main id="page" data-page class="loc-page loc-clay">
  <section class="loc-clay-hero">
    <div class="loc-shell loc-clay-hero__grid">
      <div><span class="loc-eyebrow" style="color:#f2c77f;">Clay County restoration field guide</span><h1>Paver Sealing for Clay County Homes</h1><p>Fleming Island, Orange Park, Oakleaf, Middleburg and Green Cove Springs deal with a different mix of shade, tree canopy, irrigation, storm runoff and slower dry-out than the open coastal market. HydroSeal builds the restoration plan around those conditions instead of treating Clay County like a copy of Jacksonville.</p><div class="loc-btn-row"><a class="loc-btn loc-btn--blue" href="/get-a-quote">Request a Quote</a><a class="loc-btn loc-btn--white" href="tel:+19045375000">Call 904.537.5000</a></div></div>
      <div class="loc-clay-hero__photo"><img src="/assets/hero/paversealing-clay-county.png" alt="Clay County Florida paver sealing" loading="eager" decoding="async" width="1200" height="800" fetchpriority="high" /></div>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell loc-clay-guide">
      <aside class="loc-clay-guide__rail"><span class="loc-eyebrow">Before we seal</span><h3>Clay County checklist</h3><ul><li>Is the surface staying damp under tree cover?</li><li>Are joints visibly low after rain?</li><li>Is irrigation creating rust or mineral staining?</li><li>Is there an old sealer still on the pavers?</li><li>Do edge pavers or repaired sections sit unevenly?</li><li>Is the project a driveway, patio, pool deck or stone?</li></ul><div class="loc-btn-row"><a class="loc-btn loc-btn--outline" href="/paver-cleaning">Cleaning</a><a class="loc-btn loc-btn--outline" href="/paver-repair">Repair</a></div></aside>
      <div class="loc-clay-guide__stack">
        <article class="loc-card"><span class="tag">Condition 01</span><h3>Tree canopy keeps pavers wet longer</h3><p>Shade is not automatically bad, but surfaces that stay damp support algae, mildew and darker organic buildup. The answer is not to seal over it. The surface has to be cleaned and allowed to reach the right condition before sealing.</p></article>
        <article class="loc-card"><span class="tag">Condition 02</span><h3>Storm water moves joint sand</h3><p>Florida downpours and irrigation concentrate water along driveway edges, slopes and drainage paths. When joints lose material, re-sanding becomes part of the restoration—not an optional cosmetic step.</p></article>
        <article class="loc-card"><span class="tag">Condition 03</span><h3>Older neighborhoods can have mixed coatings</h3><p>Some Clay County surfaces have been sealed more than once, repaired in sections or exposed to different products over time. We evaluate compatibility before adding a fresh coating.</p></article>
        <article class="loc-card"><span class="tag">Condition 04</span><h3>Pool decks need their own moisture plan</h3><p>Pool surrounds combine shade, splash-out, screen enclosures and foot traffic. They are not treated as a smaller driveway. Prep, product choice and cure expectations are adjusted to the environment.</p></article>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell"><span class="loc-eyebrow">Core Clay County pages</span><h2>Four dedicated markets, one strong county hub</h2>
      <div class="loc-clay-areas">
        <a class="loc-card loc-card-link" href="/service-areas/clay-county/fleming-island"><h3>Fleming Island</h3><p>Waterfront-adjacent humidity, irrigation, established communities and large visible driveways.</p></a>
        <a class="loc-card loc-card-link" href="/service-areas/clay-county/orange-park"><h3>Orange Park</h3><p>Older tree-lined properties where shade, organic staining and mixed surface age can drive prep.</p></a>
        <a class="loc-card loc-card-link" href="/service-areas/clay-county/oakleaf-plantation"><h3>Oakleaf Plantation</h3><p>Busy community driveways, newer hardscapes, joint washout and strong daily-use patterns.</p></a>
        <a class="loc-card loc-card-link" href="/service-areas/clay-county/middleburg"><h3>Middleburg</h3><p>Larger properties and open exposure. Middleburg already has demonstrated Google Search visibility, so we are continuing to build into it.</p></a>
      </div>
      <div class="loc-card" style="margin-top:16px;padding:23px;"><h3 style="margin-top:0;">Green Cove Springs stays inside the Clay County hub</h3><p style="margin-bottom:0;color:var(--loc-muted);line-height:1.6;">HydroSeal serves suitable Green Cove Springs projects, but we are concentrating that coverage here instead of maintaining another overlapping location page.</p></div>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell"><span class="loc-eyebrow">What does the surface need?</span><h2>Clean, reseal or restore?</h2>
      <div class="loc-clay-decision">
        <article class="loc-card"><b>Surface is dirty but structurally sound</b><h3>Start with cleaning</h3><p>If the primary issue is organic buildup or surface contamination, cleaning may be the first step before deciding whether protection needs to be renewed.</p><p><a href="/paver-cleaning">Explore paver cleaning →</a></p></article>
        <article class="loc-card"><b>Protection is worn but compatible</b><h3>Evaluate resealing</h3><p>A previously sealed surface may be a resealing candidate if the remaining coating is sound and compatible. We evaluate before placing a new system over the old one.</p><p><a href="/paver-resealing">Explore paver resealing →</a></p></article>
        <article class="loc-card"><b>Joints, levels or coating are failing</b><h3>Plan restoration first</h3><p>Low joints, loose pavers, failed coatings or problem staining need correction before final sealing if the goal is a durable, even result.</p><p><a href="/paver-repair">Explore paver repair →</a></p></article>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell"><span class="loc-eyebrow">Clay County services</span><h2>Match the service to the hardscape</h2>
      <div class="loc-clay-services">
        <a class="loc-card" href="/paver-sealing/driveways"><h3>Driveway Paver Sealing</h3><p>Deep cleaning, joint restoration and controlled sealing for the largest curb-appeal surface on most homes.</p></a>
        <a class="loc-card" href="/paver-sealing/pool-decks"><h3>Pool Deck Sealing</h3><p>Moisture-aware preparation for paver pool decks exposed to shade, splash-out and organic growth.</p></a>
        <a class="loc-card" href="/paver-sealing/patios-walkways"><h3>Patios &amp; Walkways</h3><p>Restoration for shaded outdoor living areas, paths and entries with staining or joint loss.</p></a>
        <a class="loc-card" href="/paver-sealing/travertine-sealing"><h3>Travertine Sealing</h3><p>Separate stone-specific evaluation where the material, porosity and finish require a different system.</p></a>
        <a class="loc-card" href="/paver-sealing/sand-options"><h3>Joint Sand Options</h3><p>See the ASTM C144 joint-sand approach used when the project requires joint restoration.</p></a>
        <a class="loc-card" href="/paver-sealing-cost-calculator"><h3>Pricing Calculator</h3><p>Use the calculator for a starting point, then confirm the scope based on the actual surface condition.</p></a>
      </div>
    </div>
  </section>

  <section class="loc-section"><div class="loc-shell"><div class="elfsight-app-9609ee68-75f4-4602-9aac-1566529f501a" data-elfsight-app-lazy></div></div></section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell"><span class="loc-eyebrow">Clay County FAQ</span><h2>Local restoration questions</h2>
      <div class="loc-faq">
        <details><summary>Why do Clay County pavers get dark under trees?</summary><div class="answer">Tree canopy reduces direct sun and can keep a surface damp longer after rain or irrigation. That environment supports organic buildup, especially on shaded patios, walkways and driveway edges. The buildup should be removed before sealing.</div></details>
        <details><summary>Does HydroSeal replace joint sand before sealing?</summary><div class="answer">When joint restoration is part of the project, HydroSeal re-sands after cleaning using ASTM C144 kiln-dried sand before the sealing step. The exact amount of joint work depends on the existing condition.</div></details>
        <details><summary>Do you seal pool decks in Fleming Island and Orange Park?</summary><div class="answer">Yes, HydroSeal works on suitable paver pool decks throughout the Clay County service area. Pool surfaces receive a moisture-aware prep and application plan rather than being treated exactly like a driveway.</div></details>
        <details><summary>Can an old failed sealer simply be covered with a new one?</summary><div class="answer">Not always. If the existing coating is failing, incompatible or trapping moisture, adding another layer can make the appearance worse. The old system has to be evaluated before a compatible restoration plan is selected.</div></details>
      </div>
    </div>
  </section>
  ''' + TRUST + r'''
  <section class="loc-final"><div class="loc-shell loc-final-inner"><div><span class="loc-eyebrow" style="color:#f2c77f;">Clay County estimates</span><h2>Restore the surface before another Florida season wears it down.</h2><p>Send photos of the pavers and the property address. We can identify the likely cleaning, sanding, repair and sealing scope before the project is scheduled.</p></div><div class="loc-btn-row"><a class="loc-btn loc-btn--blue" href="/get-a-quote">Request a Quote</a><a class="loc-btn loc-btn--white" href="tel:+19045375000">Call HydroSeal</a></div></div></section>
</main>
'''

YULEE_MAIN = r'''
<main id="page" data-page class="loc-page loc-yulee">
  <section class="loc-yulee-hero">
    <div class="loc-shell loc-yulee-hero__grid">
      <div><span class="loc-eyebrow" style="color:#2b6b60;">Nassau County growth corridor</span><h1>Paver Sealing in Yulee &amp; Wildlight</h1><p class="loc-lede">Yulee and Wildlight are a different market from older Jacksonville neighborhoods: newer homes, large driveways, fresh outdoor-living areas and strong sun exposure make early maintenance and joint protection especially important. HydroSeal focuses this Nassau County page on practical restoration for driveways, patios, walkways and pool areas.</p><div class="loc-btn-row"><a class="loc-btn loc-btn--navy" href="/get-a-quote">Request a Yulee Quote</a><a class="loc-btn loc-btn--outline" href="tel:+19045375000">904.537.5000</a></div></div>
      <div class="loc-yulee-hero__visual"><img src="/assets/hero/hydroseal-driveway.webp" alt="Sealed paver driveway in Yulee Florida" loading="eager" width="1000" height="1000" fetchpriority="high" /><img src="/assets/hero/stained-pavers.webp" alt="Weathered pavers before restoration" loading="lazy" width="600" height="500" /><img src="/assets/hero/clay-county-paver-sealing-walkway.webp" alt="Paver walkway sealing in Northeast Florida" loading="lazy" width="600" height="500" /></div>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell"><span class="loc-eyebrow" style="color:#2b6b60;">What we see in Nassau County</span><h2>Newer pavers still need maintenance.</h2>
      <div class="loc-yulee-bento">
        <article class="loc-card"><h3>Large, visible driveways</h3><p>Many Yulee and Wildlight homes put a large paver driveway front and center. When color fades, joints wash low or tire traffic creates uneven wear, the entire front elevation can look older even when the house is relatively new.</p><div class="loc-btn-row"><a class="loc-btn loc-btn--white" href="/paver-sealing/driveways">Driveway Sealing</a></div></article>
        <article class="loc-card"><h3>Strong UV exposure</h3><p>Newer communities often have less mature tree canopy, so driveways and entries spend more of the day in direct Florida sun.</p></article>
        <article class="loc-card"><h3>Joint sand washout</h3><p>Storms, irrigation and repeated cleaning can lower the joints long before the pavers themselves need major repair.</p></article>
        <article class="loc-card"><h3>Outdoor living expansion</h3><p>Patios, walkways and pool areas add more connected hardscape that benefits from a consistent maintenance plan.</p></article>
        <article class="loc-card"><h3>Wildlight coverage</h3><p>Wildlight is intentionally built into this Yulee page so Nassau County authority is concentrated on one useful market page instead of competing URLs.</p></article>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell"><span class="loc-eyebrow" style="color:#2b6b60;">Choose the surface</span><h2>Three common Yulee paver projects</h2>
      <div class="loc-yulee-strip">
        <a class="loc-card" href="/paver-sealing/driveways"><span>01 • Front of home</span><h3>Driveway Sealing</h3><p>Deep cleaning, joint restoration and even sealing for curb appeal, vehicle traffic and full-sun exposure.</p></a>
        <a class="loc-card" href="/paver-sealing/patios-walkways"><span>02 • Outdoor living</span><h3>Patios &amp; Walkways</h3><p>Cleaning and protection for entries, side paths, backyard patios and connected paver living areas.</p></a>
        <a class="loc-card" href="/paver-sealing/pool-decks"><span>03 • Water exposure</span><h3>Pool Deck Sealing</h3><p>Moisture-aware prep for paver pool decks, with application decisions made around the surface and use.</p></a>
      </div>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell"><span class="loc-eyebrow" style="color:#2b6b60;">When the surface changes</span><h2>A simple maintenance timeline</h2>
      <div class="loc-yulee-timeline">
        <article class="loc-card"><b>Stage 1</b><h3>Color starts flattening</h3><p>The surface looks drier or less uniform, especially in open sun. This is a good time to inspect rather than wait for full wear-through.</p></article>
        <article class="loc-card"><b>Stage 2</b><h3>Joints begin dropping</h3><p>Rain and irrigation expose low joints along driveway edges or drainage paths. Re-sanding may become part of the project.</p></article>
        <article class="loc-card"><b>Stage 3</b><h3>Staining becomes obvious</h3><p>Organic growth, irrigation marks or vehicle staining increase the cleaning scope required before sealing.</p></article>
        <article class="loc-card"><b>Stage 4</b><h3>Old coating becomes uneven</h3><p>Previously sealed pavers can wear patchy. At that point we evaluate compatibility and whether the job is standard resealing or a heavier restoration.</p></article>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell loc-yulee-coverage">
      <div class="loc-card coverage-dark"><span class="loc-eyebrow" style="color:#9bd3c6;">Yulee + Wildlight</span><h2>One Nassau County page on purpose</h2><p>HydroSeal is consolidating Yulee and Wildlight into a single dedicated market page. That lets us build deeper local information, project examples and internal links into one URL instead of splitting authority between two overlapping pages.</p><div class="loc-chip-row"><span class="loc-chip">Yulee</span><span class="loc-chip">Wildlight</span><span class="loc-chip">Nassau County</span></div></div>
      <div class="loc-card"><span class="loc-eyebrow" style="color:#2b6b60;">Restoration support</span><h2>More than a seal coat</h2><p class="loc-lede">If the pavers need additional prep, use the supporting service pages to understand the restoration path before sealing.</p><div class="loc-related" style="grid-template-columns:1fr 1fr;"><div><ul><li><a href="/paver-cleaning">Paver Cleaning</a></li><li><a href="/paver-repair">Paver Repair</a></li><li><a href="/paver-resealing">Paver Resealing</a></li></ul></div><div><ul><li><a href="/paver-sealing/sand-options">Joint Sand Options</a></li><li><a href="/paver-sealing/travertine-sealing">Travertine Sealing</a></li><li><a href="/paver-sealing-cost-calculator">Pricing Calculator</a></li></ul></div></div></div>
    </div>
  </section>

  <section class="loc-section">
    <div class="loc-shell"><span class="loc-eyebrow" style="color:#2b6b60;">How HydroSeal approaches the job</span><h2>Prep first. Then sand. Then seal.</h2>
      <div class="loc-related">
        <div class="loc-card"><h3>1. Evaluate &amp; clean</h3><p>We inspect surface condition, staining, drainage, existing coatings and joint depth, then clean for the actual problem instead of using one generic rinse.</p></div>
        <div class="loc-card"><h3>2. Restore joint stability</h3><p>Where the project requires it, joints are reset with ASTM C144 kiln-dried sand after cleaning and before final sealing.</p></div>
        <div class="loc-card"><h3>3. Apply a controlled system</h3><p>Sealer is applied only after the surface is prepared for it, with coverage and cure expectations matched to the hardscape and weather.</p></div>
      </div>
    </div>
  </section>

  <section class="loc-section loc-section--soft">
    <div class="loc-shell"><span class="loc-eyebrow" style="color:#2b6b60;">Yulee FAQ</span><h2>Questions about paver sealing in Yulee &amp; Wildlight</h2>
      <div class="loc-faq">
        <details><summary>Do newer Yulee pavers really need sealing?</summary><div class="answer">Newer pavers can still fade, lose joint sand and become harder to keep uniform under Florida sun, storms, irrigation and traffic. The right maintenance timing depends on the actual surface condition rather than the age of the house alone.</div></details>
        <details><summary>Does HydroSeal serve Wildlight?</summary><div class="answer">Yes. Wildlight is part of HydroSeal's Yulee and Nassau County service coverage. We intentionally represent both markets on this single dedicated page.</div></details>
        <details><summary>What types of paver surfaces do you seal in Yulee?</summary><div class="answer">HydroSeal works on suitable paver driveways, patios, walkways and pool decks, and evaluates select natural-stone surfaces when the material and condition fit our process.</div></details>
        <details><summary>What happens if my joint sand is already washing out?</summary><div class="answer">Low or missing joint sand is evaluated as part of the project. When joint restoration is included, the surface is cleaned first and the joints are reset before the final sealing step.</div></details>
      </div>
    </div>
  </section>

  <section class="loc-section"><div class="loc-shell loc-related"><div class="loc-card"><h3>Nearby Core Markets</h3><ul><li><a href="/service-areas/jacksonville">Jacksonville</a></li><li><a href="/service-areas/st-johns-county">St. Johns County</a></li><li><a href="/service-areas/clay-county">Clay County</a></li></ul></div><div class="loc-card"><h3>Paver Services</h3><ul><li><a href="/paver-sealing/driveways">Driveway Sealing</a></li><li><a href="/paver-sealing/pool-decks">Pool Deck Sealing</a></li><li><a href="/paver-sealing/patios-walkways">Patios &amp; Walkways</a></li></ul></div><div class="loc-card"><h3>Learn Before You Hire</h3><ul><li><a href="/learning-center/sealing/what-should-professional-paver-sealing-include">What Professional Sealing Includes</a></li><li><a href="/learning-center/problems/why-is-sand-coming-out-of-my-pavers">Why Sand Leaves Paver Joints</a></li><li><a href="/learning-center/sealing/how-long-does-paver-sealing-last-in-florida">How Long Sealing Lasts</a></li></ul></div></div></section>
  ''' + TRUST + r'''
  <section class="loc-final"><div class="loc-shell loc-final-inner"><div><span class="loc-eyebrow" style="color:#9bd3c6;">Yulee &amp; Wildlight</span><h2>Build the maintenance plan before the pavers look worn out.</h2><p>Send photos and the address. HydroSeal can review the surface and recommend the right cleaning, joint restoration and sealing scope.</p></div><div class="loc-btn-row"><a class="loc-btn loc-btn--blue" href="/get-a-quote">Request a Quote</a><a class="loc-btn loc-btn--white" href="tel:+19045375000">Call HydroSeal</a></div></div></section>
</main>
'''

rebuild(
    'service-areas/jacksonville/index.html',
    'Jacksonville Paver Sealing | Driveways, Pool Decks & Patios | HydroSeal',
    'Jacksonville paver sealing for driveways, pool decks, patios and walkways with deep cleaning, ASTM C144 joint restoration and professional Trident sealing.',
    JAX_MAIN,
    [
        ('How often should pavers be sealed in Jacksonville?', 'Reseal timing depends on sun exposure, traffic, drainage, coastal conditions and surface wear. HydroSeal recommends maintenance from actual condition rather than a fixed calendar alone.'),
        ('Why does joint sand disappear so quickly on some Jacksonville driveways?', 'Heavy rain, irrigation, slopes and repeated washing can move joint sand out of paver joints. Low joints should be evaluated and restored before sealing when needed.'),
        ('Can algae or mildew be sealed over?', 'No. Organic growth and contamination should be removed before sealing so it is not trapped beneath a fresh coating.'),
        ('Do you seal both driveways and pool decks in Jacksonville?', 'Yes. HydroSeal works on suitable paver driveways, pool decks, patios and walkways and evaluates select travertine surfaces.'),
    ],
)

rebuild(
    'service-areas/st-johns-county/index.html',
    'St. Johns County Paver Sealing | Nocatee, Ponte Vedra & More | HydroSeal',
    'Professional paver sealing across St. Johns County including Nocatee, Ponte Vedra, Julington Creek, Fruit Cove, Durbin Crossing and TrailMark.',
    STJ_MAIN,
    [
        ('How much does paver sealing cost in St. Johns County?', 'Pricing depends on square footage, surface condition, access, staining, joint condition, prior coatings and whether the project includes concrete pavers or natural stone.'),
        ('Do Nocatee and Ponte Vedra properties need the same sealing process?', 'Not necessarily. Coastal humidity, salt exposure, pool environments, shade, drainage and surface material can change the prep and sealing plan.'),
        ('Can you seal travertine pool decks in St. Johns County?', 'HydroSeal evaluates and seals select travertine surfaces using a stone-specific approach based on porosity, moisture and finish goals.'),
        ('Why hire a professional paver sealing company instead of adding another coat?', 'Cleaning, joint stability, moisture, old product compatibility and surface preparation determine whether a fresh sealing system has a sound foundation.'),
    ],
)

rebuild(
    'service-areas/clay-county/index.html',
    'Clay County Paver Sealing | Fleming Island, Orange Park & Oakleaf | HydroSeal',
    'Clay County paver sealing for Fleming Island, Orange Park, Oakleaf and Middleburg with restoration built around shade, moisture, joint loss and Florida storms.',
    CLAY_MAIN,
    [
        ('Why do Clay County pavers get dark under trees?', 'Tree canopy can keep pavers damp longer after rain or irrigation, which supports organic buildup. The buildup should be treated and removed before sealing.'),
        ('Does HydroSeal replace joint sand before sealing?', 'When joint restoration is part of the project, HydroSeal re-sands after cleaning using ASTM C144 kiln-dried sand before sealing.'),
        ('Do you seal pool decks in Fleming Island and Orange Park?', 'Yes. HydroSeal works on suitable paver pool decks throughout the Clay County service area using moisture-aware preparation and application.'),
        ('Can an old failed sealer simply be covered with a new one?', 'Not always. A failing or incompatible coating should be evaluated before another system is applied.'),
    ],
)

rebuild(
    'service-areas/yulee.html',
    'Paver Sealing Yulee & Wildlight FL | Driveways, Patios & Pool Decks | HydroSeal',
    'Paver sealing in Yulee and Wildlight, Florida for driveways, patios, walkways and pool decks with professional cleaning, joint restoration and sealing.',
    YULEE_MAIN,
    [
        ('Do newer Yulee pavers really need sealing?', 'Newer pavers can still fade, lose joint sand and become harder to maintain under Florida sun, storms, irrigation and traffic. Timing depends on the actual surface condition.'),
        ('Does HydroSeal serve Wildlight?', 'Yes. Wildlight is part of HydroSeal’s Yulee and Nassau County service coverage and is represented on the dedicated Yulee and Wildlight page.'),
        ('What types of paver surfaces do you seal in Yulee?', 'HydroSeal works on suitable paver driveways, patios, walkways and pool decks and evaluates select natural-stone surfaces.'),
        ('What happens if my joint sand is already washing out?', 'Low or missing joint sand is evaluated as part of the project and can be restored after cleaning before the final sealing step when included in the scope.'),
    ],
)

print('Rebuilt Jacksonville, St. Johns County, Clay County, and Yulee/Wildlight with distinct v3 layouts and FAQ schema.')

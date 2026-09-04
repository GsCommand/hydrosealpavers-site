from pathlib import Path
import json

GTAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-SXWZ2Z96S9"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-SXWZ2Z96S9');gtag('config','AW-17972657888');</script>'''

CSS = '''<link rel="stylesheet" href="/styles.css?v=20260903-jax-child" />
<link rel="stylesheet" href="/assets/css/modern-header.css?v=20260804-2" />
<link rel="stylesheet" href="/assets/css/core-location-v3.css?v=20260903" />
<link rel="stylesheet" href="/assets/css/jacksonville-child-v3.css?v=20260903" />'''


def schema(url, name, description, area, faq):
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type":"WebSite","@id":"https://hydrosealpavers.com/#website","url":"https://hydrosealpavers.com/","name":"HydroSeal"},
            {"@type":"WebPage","@id":url+"#webpage","url":url,"name":name,"description":description,"isPartOf":{"@id":"https://hydrosealpavers.com/#website"}},
            {"@type":"Service","@id":url+"#service","name":name.replace(" | HydroSeal", ""),"serviceType":"Paver sealing, cleaning, joint-sand restoration and hardscape restoration","provider":{"@id":"https://hydrosealpavers.com/#business"},"areaServed":area,"url":url},
            {"@type":"BreadcrumbList","itemListElement":[
                {"@type":"ListItem","position":1,"name":"Home","item":"https://hydrosealpavers.com/"},
                {"@type":"ListItem","position":2,"name":"Service Areas","item":"https://hydrosealpavers.com/service-areas"},
                {"@type":"ListItem","position":3,"name":"Jacksonville","item":"https://hydrosealpavers.com/service-areas/jacksonville"},
                {"@type":"ListItem","position":4,"name":area[0]["name"],"item":url}
            ]},
            {"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
        ]
    }
    return '<script type="application/ld+json">'+json.dumps(graph, ensure_ascii=False)+'</script>'


def doc(title, desc, canonical, image, body, area, faq):
    return f'''<!doctype html>
<html lang="en">
<head>
{GTAG}
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<link rel="icon" href="/assets/favicons/favicon.ico" sizes="any" />
<link rel="icon" type="image/png" href="/assets/favicons/favicon-32x32.png" sizes="32x32" />
<link rel="apple-touch-icon" href="/assets/favicons/apple-touch-icon.png" />
<meta name="theme-color" content="#0F6EA8" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta name="robots" content="index,follow,max-image-preview:large" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="HydroSeal" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="https://hydrosealpavers.com{image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="https://hydrosealpavers.com{image}" />
{CSS}
{schema(canonical,title,desc,area,faq)}
</head>
<body>
<div data-include="/partials/header.html"></div>
{body}
<div data-include="/partials/footer.html"></div>
<script src="/assets/js/include.js" defer></script>
<script src="/assets/js/router.js" defer></script>
<script src="/assets/js/nav.js" defer></script>
<script src="/assets/js/analytics.js" defer></script>
<script defer src="/assets/js/third-party-loader.js"></script>
</body>
</html>'''

BEACH_URL='https://hydrosealpavers.com/service-areas/jacksonville/jacksonville-beach'
BEACH_TITLE='Jacksonville Beach Paver Sealing | Neptune Beach & Atlantic Beach | HydroSeal'
BEACH_DESC='Professional paver sealing for Jacksonville Beach, Neptune Beach and Atlantic Beach with coastal cleaning, joint-sand restoration and surface-specific sealing.'
BEACH_FAQ=[
('Do you provide paver sealing in Jacksonville Beach, Neptune Beach and Atlantic Beach?','Yes. HydroSeal serves suitable residential paver projects across Jacksonville Beach, Neptune Beach and Atlantic Beach, with scope based on the actual surface, access and current scheduling.'),
('What makes paver maintenance different near Jacksonville’s beaches?','Open sun, coastal humidity, wind-driven rain, irrigation, salt-laden air, organic growth and fast-changing weather can all affect how quickly a paver surface fades or loses joint material.'),
('Can you seal both beach-area driveways and pool decks?','Yes. HydroSeal works on suitable paver driveways, pool decks, patios and walkways. Pool areas receive a separate moisture-aware preparation plan rather than being treated exactly like driveways.'),
('Should algae, mildew or dark coastal buildup be sealed over?','No. Organic growth and contamination should be removed before sealing so they are not trapped below the fresh system.'),
]
BEACH_BODY='''
<main id="page" data-page class="jx-child jx-beach">
<section class="jx-beach-hero">
  <img src="/assets/hero/jacksonville-pool-paver-sealing.jpg" alt="Paver sealing near Jacksonville Beach Florida" loading="eager" decoding="async" fetchpriority="high" />
  <div class="jx-shell jx-beach-hero__inner"><div class="jx-beach-hero__panel">
    <span class="jx-eyebrow" style="color:#9fe5f7;">Jacksonville Beaches • Duval County</span>
    <h1>Coastal Paver Sealing for Jacksonville Beach</h1>
    <p>Jacksonville Beach, Neptune Beach and Atlantic Beach share the coast, but not every hardscape ages the same way. Full-sun driveways, shaded patios, pool decks behind screen enclosures and older beach-area pavers each need a different prep decision before sealing.</p>
    <div class="jx-btns"><a class="jx-btn jx-btn--blue" href="/get-a-quote">Request a Quote</a><a class="jx-btn jx-btn--white" href="tel:+19045375000">Call 904.537.5000</a></div>
  </div></div>
</section>
<div class="jx-shell jx-proof"><div class="jx-proof-grid"><div><strong>Coastal Prep</strong><span>Built around sun, humidity and drainage</span></div><div><strong>Joint Restoration</strong><span>ASTM C144 kiln-dried sand</span></div><div><strong>Driveways + Pool Decks</strong><span>Different surfaces, different plans</span></div><div><strong>2-Year Warranty</strong><span>Workmanship and adhesion coverage</span></div></div></div>

<section class="jx-section"><div class="jx-shell"><span class="jx-eyebrow">Three beach communities</span><h2>Same coastline. Different exposure patterns.</h2><p class="jx-lede">The Beaches are close together geographically, but tree cover, distance from the ocean, irrigation, drainage and how much of the property stays in open sun all change what we look for before cleaning or sealing.</p><div class="jx-beach-zones">
<article class="jx-card"><b>Jacksonville Beach</b><h3>Open sun and high-visibility hardscapes</h3><p>Driveways and pool areas can stay exposed for most of the day. UV, vehicle use, storms and irrigation can flatten color and lower joints faster on open surfaces.</p></article>
<article class="jx-card"><b>Neptune Beach</b><h3>Shade and moisture pockets</h3><p>Mature landscaping can keep walkways, patios and driveway edges damp longer, creating darker organic buildup and uneven appearance between shaded and sunny sections.</p></article>
<article class="jx-card"><b>Atlantic Beach</b><h3>Mature trees plus coastal air</h3><p>Older neighborhoods can combine tree canopy, wind-driven moisture and mixed-age pavers, so cleaning and coating compatibility matter before another sealer is added.</p></article>
</div></div></section>

<section class="jx-section jx-section--soft"><div class="jx-shell jx-beach-split"><div class="jx-beach-photo"><img src="/assets/hero/paver-sealing-jacksonville-driveway.webp" alt="Jacksonville Beaches paver driveway restoration" loading="lazy" decoding="async" /></div><div><span class="jx-eyebrow">What coastal exposure changes</span><h2>Four things we check before sealing.</h2><div class="jx-coast-factors">
<article class="jx-card"><h3>Sun exposure</h3><p>Open surfaces can fade faster and show wear earlier than areas protected by tree canopy or structures.</p></article>
<article class="jx-card"><h3>Drainage</h3><p>Storm runoff and irrigation can move sand from joints and leave low areas holding moisture longer.</p></article>
<article class="jx-card"><h3>Organic buildup</h3><p>Shade, humidity and landscaping create mildew, algae and tannin staining that must be addressed before sealing.</p></article>
<article class="jx-card"><h3>Prior coatings</h3><p>Older beach-area pavers may have uneven or incompatible sealer remnants that change the restoration path.</p></article>
</div></div></div></section>

<section class="jx-section"><div class="jx-shell"><span class="jx-eyebrow">Choose the hardscape</span><h2>Beach-area paver services by surface.</h2><div class="jx-services">
<a class="jx-card" href="/paver-sealing/driveways"><span>Driveways</span><h3>Paver driveway sealing</h3><p>Cleaning, joint restoration and sealing built around traffic, runoff and open coastal exposure.</p></a>
<a class="jx-card" href="/paver-sealing/pool-decks"><span>Pool decks</span><h3>Moisture-aware sealing</h3><p>Pool decks need careful drying, traction awareness and a scope matched to splash-out and shade.</p></a>
<a class="jx-card" href="/paver-sealing/patios-walkways"><span>Outdoor living</span><h3>Patios & walkways</h3><p>Shade and organic buildup often matter more on side paths, entries and backyard living areas.</p></a>
<a class="jx-card" href="/paver-sealing/travertine-sealing"><span>Natural stone</span><h3>Travertine sealing</h3><p>Stone is evaluated separately because porosity and moisture behavior differ from concrete pavers.</p></a>
</div></div></section>

<section class="jx-section jx-section--soft"><div class="jx-shell"><span class="jx-eyebrow">HydroSeal process</span><h2>Coastal restoration starts with the substrate, not the final coat.</h2><div class="jx-process">
<article class="jx-card"><b>01</b><h3>Inspect</h3><p>We evaluate old sealer, staining, drainage, joint depth and how the surface is used.</p></article><article class="jx-card"><b>02</b><h3>Deep clean</h3><p>Organic growth, dirt and problem areas are treated before fresh product goes down.</p></article><article class="jx-card"><b>03</b><h3>Restore joints</h3><p>Where needed, low joints are reset with kiln-dried ASTM C144 joint sand.</p></article><article class="jx-card"><b>04</b><h3>Seal correctly</h3><p>Compatible sealer is applied only after the surface is properly prepared and ready to accept it.</p></article>
</div><div class="jx-btns"><a class="jx-btn jx-btn--outline" href="/paver-cleaning">Paver Cleaning</a><a class="jx-btn jx-btn--outline" href="/paver-resealing">Paver Resealing</a><a class="jx-btn jx-btn--outline" href="/paver-sealing/sand-options">Joint Sand Options</a></div></div></section>

<section class="jx-section"><div class="jx-shell"><div class="elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26" data-elfsight-app-lazy></div></div></section>
<section class="jx-section jx-section--soft"><div class="jx-shell"><span class="jx-eyebrow">Jacksonville Beaches FAQ</span><h2>Questions homeowners ask before sealing.</h2><div class="jx-faq">
<details><summary>Do you provide paver sealing in Jacksonville Beach, Neptune Beach and Atlantic Beach?</summary><div class="answer">Yes. HydroSeal serves suitable residential paver projects across all three Beaches communities, with scope based on actual surface condition and scheduling.</div></details>
<details><summary>What makes paver maintenance different near Jacksonville’s beaches?</summary><div class="answer">Open sun, coastal humidity, wind-driven rain, irrigation and salt-laden air can all affect fading, moisture and joint stability.</div></details>
<details><summary>Can you seal both beach-area driveways and pool decks?</summary><div class="answer">Yes. Driveways, pool decks, patios and walkways are common projects, but each surface receives its own preparation plan.</div></details>
<details><summary>Should algae or mildew be sealed over?</summary><div class="answer">No. Organic growth and contamination should be cleaned away before sealing so they are not trapped below the fresh system.</div></details>
</div></div></section>
<section class="jx-section"><div class="jx-shell jx-related"><div class="jx-card"><h3>Jacksonville Core Areas</h3><ul><li><a href="/service-areas/jacksonville">Jacksonville</a></li><li><a href="/service-areas/jacksonville/mandarin">Mandarin</a></li><li><a href="/service-areas/jacksonville/southside">Southside</a></li></ul></div><div class="jx-card"><h3>Restoration Services</h3><ul><li><a href="/paver-cleaning">Paver Cleaning</a></li><li><a href="/paver-repair">Paver Repair</a></li><li><a href="/paver-resealing">Paver Resealing</a></li><li><a href="/paver-sealing/sand-options">Joint Sand Options</a></li></ul></div><div class="jx-card"><h3>Planning Guides</h3><ul><li><a href="/learning-center/sealing/what-should-professional-paver-sealing-include">What Professional Sealing Includes</a></li><li><a href="/learning-center/problems/why-is-sand-coming-out-of-my-pavers">Why Joint Sand Comes Out</a></li><li><a href="/paver-sealing-cost-calculator">Pricing Calculator</a></li></ul></div></div></section>
<section class="jx-trust"><div class="jx-shell jx-trust-grid"><div>Licensed & Insured</div><div>Trident Master Certified</div><div>ASTM C144 Joint Sand</div><div>2-Year Workmanship Warranty</div></div></section>
<section class="jx-final"><div class="jx-shell jx-final-grid"><div><span class="jx-eyebrow" style="color:#9fe5f7;">Jacksonville Beaches</span><h2>Get the coastal prep right before the sealer goes down.</h2><p>Send the property address and photos of the driveway, pool deck, patio or walkway. HydroSeal can help identify the right cleaning, sanding and sealing scope.</p></div><div class="jx-btns"><a class="jx-btn jx-btn--blue" href="/get-a-quote">Request a Quote</a><a class="jx-btn jx-btn--white" href="tel:+19045375000">Call HydroSeal</a></div></div></section>
</main>'''

MAN_URL='https://hydrosealpavers.com/service-areas/jacksonville/mandarin'
MAN_TITLE='Mandarin Paver Sealing Jacksonville FL | Driveways & Pool Decks | HydroSeal'
MAN_DESC='Mandarin Jacksonville paver sealing for shaded driveways, patios and pool decks with deep cleaning, joint restoration and sealing built for mature tree canopy.'
MAN_FAQ=[
('Why do Mandarin pavers get dark under trees?','Mature tree canopy reduces direct sun and can keep surfaces damp longer after rain or irrigation. That environment supports organic growth and leaf staining, especially on shaded patios, walkways and driveway edges.'),
('Do you replace joint sand before sealing in Mandarin?','When joint restoration is part of the scope, HydroSeal cleans first, allows the surface to reach the right condition, then restores joints with kiln-dried ASTM C144 sand before sealing.'),
('Can you seal pool decks and patios in Mandarin?','Yes. HydroSeal works on suitable paver driveways, pool decks, patios and walkways throughout the Mandarin service area, with preparation adjusted to shade, drainage and use.'),
('What if my Mandarin pavers were sealed before?','Previously sealed surfaces are evaluated for remaining coating condition and compatibility. A worn but sound system may be a resealing candidate, while failed or incompatible coatings can require a different restoration approach.'),
]
MAN_BODY='''
<main id="page" data-page class="jx-child jx-mandarin">
<section class="jx-man-hero"><div class="jx-shell jx-man-hero__grid"><div><span class="jx-eyebrow" style="color:#a8d6c3;">Mandarin • South Jacksonville</span><h1>Paver Sealing Built for Mature Mandarin Properties</h1><p>Mandarin is one of Jacksonville's most established residential areas. Mature oaks, heavy landscaping, shaded driveways and pool decks, irrigation and older hardscapes can create a very different restoration problem than newer open-sun communities.</p><div class="jx-btns"><a class="jx-btn jx-btn--blue" href="/get-a-quote">Request a Quote</a><a class="jx-btn jx-btn--white" href="tel:+19045375000">Call 904.537.5000</a></div></div><div class="jx-man-hero__photo"><img src="/assets/hero/mandarin-paver-sealing-driveway.webp" alt="Mandarin Jacksonville paver driveway sealing" loading="eager" decoding="async" fetchpriority="high" /></div></div></section>
<div class="jx-shell jx-proof"><div class="jx-proof-grid"><div><strong>Shade-Aware Cleaning</strong><span>Built around canopy and organics</span></div><div><strong>Joint Restoration</strong><span>ASTM C144 kiln-dried sand</span></div><div><strong>Older Surface Evaluation</strong><span>Check repairs and prior coatings</span></div><div><strong>2-Year Warranty</strong><span>Workmanship and adhesion coverage</span></div></div></div>

<section class="jx-section"><div class="jx-shell jx-man-canopy"><aside class="jx-card jx-man-rail"><span class="jx-eyebrow" style="color:#a8d6c3;">Mandarin inspection list</span><h3>What mature landscaping changes</h3><ul><li>Longer dry-out under tree canopy</li><li>Leaf tannins and dark organic staining</li><li>Irrigation overspray near beds and edges</li><li>Older pavers with repairs or mixed wear</li><li>Pool decks hidden behind shade structures</li><li>Joint loss along drainage paths</li></ul></aside><div><span class="jx-eyebrow">Why Mandarin is different</span><h2>Shade can protect color while creating a moisture problem.</h2><div class="jx-man-stack"><article class="jx-card"><h3>Mature tree canopy</h3><p>Less direct sun can slow fading, but it can also keep surfaces wet longer and support algae, mildew and darker joint lines.</p></article><article class="jx-card"><h3>Leaf and irrigation staining</h3><p>Tannins, fertilizer residue, irrigation minerals and organic debris often drive the cleaning scope before sealing starts.</p></article><article class="jx-card"><h3>Established hardscapes</h3><p>Older driveways may have repaired sections, previous sealers or uneven joint depth that need to be evaluated for compatibility.</p></article><article class="jx-card"><h3>Backyard living areas</h3><p>Pool decks, patios and walkways often have different shade and moisture patterns than the front driveway, so one process does not fit every surface.</p></article></div></div></div></section>

<section class="jx-section jx-section--soft"><div class="jx-shell"><span class="jx-eyebrow">What does the Mandarin surface need?</span><h2>Clean, reseal or restore?</h2><p class="jx-lede">The useful decision is not simply whether the pavers look faded. We look at joint condition, contamination, old coating, drainage and how much of the surface still has usable protection.</p><div class="jx-man-decision"><article class="jx-card"><b>Mostly contamination</b><h3>Start with cleaning</h3><p>When the main issue is mildew, leaf staining or surface grime, cleaning comes first before deciding whether protection also needs to be renewed.</p><p><a href="/paver-cleaning">Explore paver cleaning →</a></p></article><article class="jx-card"><b>Protection is worn</b><h3>Evaluate resealing</h3><p>A previously sealed surface may be a resealing candidate when the remaining coating is sound and compatible with the next system.</p><p><a href="/paver-resealing">Explore paver resealing →</a></p></article><article class="jx-card"><b>Joints or levels are failing</b><h3>Restore first</h3><p>Low joints, loose pavers, failed coatings or problem staining should be corrected before the final sealing step.</p><p><a href="/paver-repair">Explore paver repair →</a></p></article></div></div></section>

<section class="jx-section"><div class="jx-shell"><span class="jx-eyebrow">Mandarin hardscapes</span><h2>Match the service to the surface.</h2><div class="jx-services"><a class="jx-card" href="/paver-sealing/driveways"><span>Front of home</span><h3>Driveway sealing</h3><p>Built around shade transitions, vehicle traffic, runoff and the condition of existing joint sand.</p></a><a class="jx-card" href="/paver-sealing/pool-decks"><span>Backyard</span><h3>Pool deck sealing</h3><p>Moisture-aware prep for shaded pool areas, screen enclosures and splash-out zones.</p></a><a class="jx-card" href="/paver-sealing/patios-walkways"><span>Outdoor living</span><h3>Patios & walkways</h3><p>Cleaning and protection for entries, side paths and backyard pavers affected by tree cover and organics.</p></a><a class="jx-card" href="/paver-sealing/travertine-sealing"><span>Natural stone</span><h3>Travertine sealing</h3><p>Stone-specific evaluation when porosity and moisture behavior require a separate system.</p></a></div></div></section>

<section class="jx-section jx-section--soft"><div class="jx-shell"><span class="jx-eyebrow">HydroSeal workflow</span><h2>Preparation matters more in shaded environments.</h2><div class="jx-process"><article class="jx-card"><b>01</b><h3>Evaluate</h3><p>We check tree cover, old sealer, joint depth, staining and drainage before setting the scope.</p></article><article class="jx-card"><b>02</b><h3>Clean deeply</h3><p>Organic growth and staining are treated rather than hidden under another layer of sealer.</p></article><article class="jx-card"><b>03</b><h3>Restore joints</h3><p>Where needed, the joint system is rebuilt with kiln-dried ASTM C144 sand.</p></article><article class="jx-card"><b>04</b><h3>Seal once ready</h3><p>The surface must be properly prepared and dry enough before a compatible system is applied.</p></article></div><div class="jx-btns"><a class="jx-btn jx-btn--outline" href="/paver-sealing/sand-options">Joint Sand Options</a><a class="jx-btn jx-btn--outline" href="/paver-sealing-cost-calculator">Pricing Calculator</a></div></div></section>
<section class="jx-section"><div class="jx-shell"><div class="elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26" data-elfsight-app-lazy></div></div></section>
<section class="jx-section jx-section--soft"><div class="jx-shell"><span class="jx-eyebrow">Mandarin FAQ</span><h2>Questions from established Jacksonville properties.</h2><div class="jx-faq"><details><summary>Why do Mandarin pavers get dark under trees?</summary><div class="answer">Mature tree canopy can keep pavers damp longer after rain or irrigation. That environment supports organic growth and leaf staining, especially along shaded edges and patios.</div></details><details><summary>Do you replace joint sand before sealing in Mandarin?</summary><div class="answer">When joint restoration is part of the scope, the surface is cleaned first and low joints are restored with kiln-dried ASTM C144 sand before sealing.</div></details><details><summary>Can you seal pool decks and patios in Mandarin?</summary><div class="answer">Yes. HydroSeal works on suitable driveways, pool decks, patios and walkways, with prep adjusted to shade, drainage and surface use.</div></details><details><summary>What if my Mandarin pavers were sealed before?</summary><div class="answer">Previously sealed surfaces are evaluated for remaining coating condition and compatibility before another system is applied.</div></details></div></div></section>
<section class="jx-section"><div class="jx-shell jx-related"><div class="jx-card"><h3>Jacksonville Core Areas</h3><ul><li><a href="/service-areas/jacksonville">Jacksonville</a></li><li><a href="/service-areas/jacksonville/jacksonville-beach">Jacksonville Beach</a></li><li><a href="/service-areas/jacksonville/southside">Southside</a></li></ul></div><div class="jx-card"><h3>Restoration Services</h3><ul><li><a href="/paver-cleaning">Paver Cleaning</a></li><li><a href="/paver-repair">Paver Repair</a></li><li><a href="/paver-resealing">Paver Resealing</a></li><li><a href="/paver-sealing/sand-options">Joint Sand Options</a></li></ul></div><div class="jx-card"><h3>Planning Guides</h3><ul><li><a href="/learning-center/sealing/what-should-professional-paver-sealing-include">What Professional Sealing Includes</a></li><li><a href="/learning-center/problems/why-is-sand-coming-out-of-my-pavers">Why Joint Sand Comes Out</a></li><li><a href="/paver-sealing-cost-calculator">Pricing Calculator</a></li></ul></div></div></section>
<section class="jx-trust"><div class="jx-shell jx-trust-grid"><div>Licensed & Insured</div><div>Trident Master Certified</div><div>ASTM C144 Joint Sand</div><div>2-Year Workmanship Warranty</div></div></section>
<section class="jx-final"><div class="jx-shell jx-final-grid"><div><span class="jx-eyebrow" style="color:#a8d6c3;">Mandarin estimates</span><h2>Build the restoration around the shade, not around a generic template.</h2><p>Send the property address and photos. HydroSeal can review the driveway, pool deck, patio or walkway and recommend the right cleaning, sanding, repair and sealing scope.</p></div><div class="jx-btns"><a class="jx-btn jx-btn--blue" href="/get-a-quote">Request a Quote</a><a class="jx-btn jx-btn--white" href="tel:+19045375000">Call HydroSeal</a></div></div></section>
</main>'''

SS_URL='https://hydrosealpavers.com/service-areas/jacksonville/southside'
SS_TITLE='Southside Jacksonville Paver Sealing | Driveways & Pool Decks | HydroSeal'
SS_DESC='Southside Jacksonville paver sealing for Deerwood, eTown, Glen Kernan, Pablo Creek Reserve and Tamaya with cleaning, joint restoration and sealing.'
SS_FAQ=[
('What areas does the Southside Jacksonville page cover?','HydroSeal uses the Southside page as the primary service page for Southside Jacksonville and selected nearby communities including Deerwood, eTown, Glen Kernan, Pablo Creek Reserve and Tamaya.'),
('Why do Southside driveways lose joint sand?','Large driveways can channel storm water and irrigation runoff along slopes, edges and drainage paths. Repeated washing and daily vehicle traffic can make low joints more noticeable over time.'),
('Do newer Southside pavers still need professional maintenance?','Yes. Newer hardscapes are still exposed to strong sun, storms, irrigation and vehicle traffic. Maintenance timing should be based on actual color, joint condition, coating wear and drainage rather than the age of the neighborhood alone.'),
('Can HydroSeal seal pool decks in Southside Jacksonville?','Yes. HydroSeal works on suitable paver pool decks and patios, with prep and application adjusted for shade, splash-out, screen enclosures and moisture exposure.'),
]
SS_BODY='''
<main id="page" data-page class="jx-child jx-southside">
<section class="jx-ss-hero"><div class="jx-shell jx-ss-hero__grid"><div><span class="jx-eyebrow" style="color:#8bdcf3;">Southside Jacksonville</span><h1>Paver Sealing for Jacksonville’s High-Growth Southside</h1><p>Southside properties often combine large visible driveways, newer paver installations, frequent irrigation, strong sun and heavy daily vehicle use. HydroSeal builds the maintenance plan around those real wear patterns for Southside, Deerwood, eTown, Glen Kernan, Pablo Creek Reserve and Tamaya.</p><div class="jx-btns"><a class="jx-btn jx-btn--blue" href="/get-a-quote">Request a Quote</a><a class="jx-btn jx-btn--white" href="tel:+19045375000">Call 904.537.5000</a></div></div><div class="jx-ss-stats"><div><strong>Large driveways</strong><span>More surface area means runoff and joint condition matter.</span></div><div><strong>Strong UV</strong><span>Open-sun pavers can flatten in color faster.</span></div><div><strong>Daily traffic</strong><span>Tire use and repeated entry patterns create visible wear.</span></div><div><strong>Irrigation</strong><span>Overspray and drainage paths affect staining and joints.</span></div></div></div></section>
<div class="jx-shell jx-proof"><div class="jx-proof-grid"><div><strong>Driveway-Focused Prep</strong><span>Traffic and runoff evaluated first</span></div><div><strong>Joint Restoration</strong><span>ASTM C144 kiln-dried sand</span></div><div><strong>New + Existing Pavers</strong><span>Scope based on current condition</span></div><div><strong>2-Year Warranty</strong><span>Workmanship and adhesion coverage</span></div></div></div>

<section class="jx-section"><div class="jx-shell"><span class="jx-eyebrow">Southside communities</span><h2>One strong Southside page for five important local markets.</h2><p class="jx-lede">Instead of splitting closely related Southside communities across many shallow pages, this page carries the service context for the places where similar driveway, irrigation and exposure patterns overlap.</p><div class="jx-ss-communities"><article class="jx-card"><h3>Deerwood</h3><p>Established homes, landscaping and large visible driveways where shade and irrigation can create mixed wear.</p></article><article class="jx-card"><h3>eTown</h3><p>Newer hardscapes with open exposure, frequent irrigation and high curb-appeal expectations.</p></article><article class="jx-card"><h3>Glen Kernan</h3><p>Large premium driveways and outdoor living areas where even finish quality matters across broad surfaces.</p></article><article class="jx-card"><h3>Pablo Creek Reserve</h3><p>High-end paver systems that benefit from early maintenance before color and joints become visibly uneven.</p></article><article class="jx-card"><h3>Tamaya</h3><p>Newer community pavers exposed to strong sun, irrigation, traffic and seasonal storm runoff.</p></article></div></div></section>

<section class="jx-section jx-section--soft"><div class="jx-shell"><span class="jx-eyebrow">Southside maintenance cycle</span><h2>Catch the wear before the driveway needs heavier restoration.</h2><div class="jx-ss-lifecycle"><article><b>Stage 1</b><h3>Color loses depth</h3><p>Open sun and traffic start flattening the appearance while the joints may still look relatively stable.</p></article><article><b>Stage 2</b><h3>Joints begin dropping</h3><p>Runoff exposes low sand along edges, slopes and vehicle paths, making the system look less finished.</p></article><article><b>Stage 3</b><h3>Staining builds</h3><p>Irrigation marks, organics and vehicle contamination increase the cleaning scope required before sealing.</p></article><article><b>Stage 4</b><h3>Old coating wears unevenly</h3><p>Previously sealed pavers can become patchy, making compatibility and restoration decisions more important.</p></article></div></div></section>

<section class="jx-section"><div class="jx-shell"><span class="jx-eyebrow">Choose the service</span><h2>Southside paver maintenance by surface type.</h2><div class="jx-services"><a class="jx-card" href="/paver-sealing/driveways"><span>Driveways</span><h3>High-visibility driveway sealing</h3><p>Deep cleaning, joint restoration and controlled sealing for tire traffic, runoff and strong UV.</p></a><a class="jx-card" href="/paver-sealing/pool-decks"><span>Pool decks</span><h3>Backyard moisture planning</h3><p>Pool areas receive a separate prep strategy around splash-out, shade and cure conditions.</p></a><a class="jx-card" href="/paver-sealing/patios-walkways"><span>Outdoor living</span><h3>Patios & walkways</h3><p>Entries, paths and patios get surface-specific cleaning and protection based on use and exposure.</p></a><a class="jx-card" href="/paver-sealing/travertine-sealing"><span>Natural stone</span><h3>Travertine sealing</h3><p>Stone-specific evaluation when material porosity and moisture call for a different system.</p></a></div></div></section>

<section class="jx-section jx-section--soft"><div class="jx-shell"><span class="jx-eyebrow">HydroSeal workflow</span><h2>Build the service around the actual Southside surface.</h2><div class="jx-process"><article class="jx-card"><b>01</b><h3>Inspect</h3><p>We evaluate the coating, joint depth, runoff, staining, traffic and paver condition.</p></article><article class="jx-card"><b>02</b><h3>Clean</h3><p>Organic buildup, irrigation staining and surface grime are addressed before sealing.</p></article><article class="jx-card"><b>03</b><h3>Re-sand</h3><p>Where required, low joints are restored with kiln-dried ASTM C144 joint sand.</p></article><article class="jx-card"><b>04</b><h3>Seal</h3><p>A compatible sealer is applied only after the surface is properly prepared and ready.</p></article></div><div class="jx-btns"><a class="jx-btn jx-btn--outline" href="/paver-cleaning">Paver Cleaning</a><a class="jx-btn jx-btn--outline" href="/paver-repair">Paver Repair</a><a class="jx-btn jx-btn--outline" href="/paver-resealing">Paver Resealing</a><a class="jx-btn jx-btn--outline" href="/paver-sealing/sand-options">Joint Sand Options</a></div></div></section>
<section class="jx-section"><div class="jx-shell"><div class="elfsight-app-bfab489f-7fca-4f05-ba5a-d92616b76b26" data-elfsight-app-lazy></div></div></section>
<section class="jx-section jx-section--soft"><div class="jx-shell"><span class="jx-eyebrow">Southside FAQ</span><h2>Questions about newer and high-traffic hardscapes.</h2><div class="jx-faq"><details><summary>What areas does the Southside Jacksonville page cover?</summary><div class="answer">This page is the primary HydroSeal service page for Southside Jacksonville and selected nearby communities including Deerwood, eTown, Glen Kernan, Pablo Creek Reserve and Tamaya.</div></details><details><summary>Why do Southside driveways lose joint sand?</summary><div class="answer">Large driveways can channel storm water and irrigation along slopes, edges and drainage paths. Repeated washing and vehicle traffic can make low joints more visible over time.</div></details><details><summary>Do newer Southside pavers still need professional maintenance?</summary><div class="answer">Yes. Newer pavers are still exposed to strong sun, storms, irrigation and traffic. Maintenance should be based on actual color, joint condition and coating wear.</div></details><details><summary>Can HydroSeal seal pool decks in Southside Jacksonville?</summary><div class="answer">Yes. Suitable paver pool decks and patios are common projects, with prep adjusted to shade, splash-out and moisture exposure.</div></details></div></div></section>
<section class="jx-section"><div class="jx-shell jx-related"><div class="jx-card"><h3>Jacksonville Core Areas</h3><ul><li><a href="/service-areas/jacksonville">Jacksonville</a></li><li><a href="/service-areas/jacksonville/jacksonville-beach">Jacksonville Beach</a></li><li><a href="/service-areas/jacksonville/mandarin">Mandarin</a></li></ul></div><div class="jx-card"><h3>Restoration Services</h3><ul><li><a href="/paver-cleaning">Paver Cleaning</a></li><li><a href="/paver-repair">Paver Repair</a></li><li><a href="/paver-resealing">Paver Resealing</a></li><li><a href="/paver-sealing/sand-options">Joint Sand Options</a></li></ul></div><div class="jx-card"><h3>Planning Guides</h3><ul><li><a href="/learning-center/sealing/what-should-professional-paver-sealing-include">What Professional Sealing Includes</a></li><li><a href="/learning-center/problems/why-is-sand-coming-out-of-my-pavers">Why Joint Sand Comes Out</a></li><li><a href="/paver-sealing-cost-calculator">Pricing Calculator</a></li></ul></div></div></section>
<section class="jx-trust"><div class="jx-shell jx-trust-grid"><div>Licensed & Insured</div><div>Trident Master Certified</div><div>ASTM C144 Joint Sand</div><div>2-Year Workmanship Warranty</div></div></section>
<section class="jx-final"><div class="jx-shell jx-final-grid"><div><span class="jx-eyebrow" style="color:#8bdcf3;">Southside Jacksonville</span><h2>Protect the curb appeal before open-sun wear becomes obvious.</h2><p>Send the address and surface photos. HydroSeal can review the driveway, pool deck, patio or walkway and recommend the right cleaning, sanding, repair and sealing scope.</p></div><div class="jx-btns"><a class="jx-btn jx-btn--blue" href="/get-a-quote">Request a Quote</a><a class="jx-btn jx-btn--white" href="tel:+19045375000">Call HydroSeal</a></div></div></section>
</main>'''

pages = {
 Path('service-areas/jacksonville/jacksonville-beach.html'): doc(BEACH_TITLE,BEACH_DESC,BEACH_URL,'/assets/hero/jacksonville-pool-paver-sealing.jpg',BEACH_BODY,[{"@type":"City","name":"Jacksonville Beach"},{"@type":"City","name":"Neptune Beach"},{"@type":"City","name":"Atlantic Beach"}],BEACH_FAQ),
 Path('service-areas/jacksonville/mandarin.html'): doc(MAN_TITLE,MAN_DESC,MAN_URL,'/assets/hero/mandarin-paver-sealing-driveway.webp',MAN_BODY,[{"@type":"Place","name":"Mandarin, Jacksonville, FL"},{"@type":"City","name":"Jacksonville"},{"@type":"AdministrativeArea","name":"Duval County"}],MAN_FAQ),
 Path('service-areas/jacksonville/southside.html'): doc(SS_TITLE,SS_DESC,SS_URL,'/assets/hero/southside-paver-sealing-driveway.webp',SS_BODY,[{"@type":"Place","name":"Southside Jacksonville, FL"},{"@type":"Place","name":"Deerwood, Jacksonville, FL"},{"@type":"Place","name":"eTown, Jacksonville, FL"},{"@type":"Place","name":"Glen Kernan, Jacksonville, FL"},{"@type":"Place","name":"Pablo Creek Reserve, Jacksonville, FL"},{"@type":"Place","name":"Tamaya, Jacksonville, FL"}],SS_FAQ),
}

for path, content in pages.items():
    path.write_text(content.rstrip()+"\n", encoding='utf-8')

print('Rebuilt Jacksonville Beach, Mandarin and Southside with distinct v3 layouts.')
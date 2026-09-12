from pathlib import Path
import re


def inject_before_main(path: str, marker: str, html: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if marker in text:
        print(f"already present: {path}")
        return
    if "</main>" not in text:
        raise SystemExit(f"missing </main> in {path}")
    text = text.replace("</main>", html.rstrip() + "\n</main>", 1)
    p.write_text(text, encoding="utf-8")
    print(f"updated: {path}")


inject_before_main(
    "index.html",
    'id="hs-near-me-static"',
    '''
  <section id="hs-near-me-static" class="section home-faq" aria-labelledby="hs-near-me-title">
    <div class="container">
      <h2 id="hs-near-me-title">How do I find a paver sealing company near me?</h2>
      <p>If you are searching for <strong>paver sealing near me</strong>, <strong>paver cleaning and sealing near me</strong>, or a <strong>paver sealing company near me</strong>, HydroSeal serves Jacksonville, St. Johns County, Ponte Vedra, Nocatee, Orange Park, Fleming Island, and nearby Northeast Florida communities. We evaluate paver condition, joint sand, previous sealer, drainage, and surface type before recommending cleaning, resealing, or restoration.</p>
    </div>
  </section>
''',
)

inject_before_main(
    "paver-cleaning/index.html",
    'id="hs-search-intent-cleaning"',
    '''
  <section id="hs-search-intent-cleaning" class="sd-section sd-section--soft" aria-labelledby="hs-search-intent-cleaning-title">
    <div class="sd-shell">
      <span class="sd-kicker">Local paver cleaning &amp; restoration</span>
      <h2 id="hs-search-intent-cleaning-title">Paver cleaning, sealing and restoration near Jacksonville.</h2>
      <p class="sd-lead">Homeowners searching for <strong>paver cleaning and sealing near me</strong> or <strong>paver restoration near me</strong> often need more than high-pressure washing. HydroSeal serves Jacksonville, St. Johns County, Ponte Vedra, Nocatee, Orange Park, Fleming Island, and nearby communities with surface-specific cleaning, joint evaluation, and sealing-ready preparation. <a href="/paver-resealing/">See our paver resealing and restoration process.</a></p>
    </div>
  </section>
''',
)

inject_before_main(
    "paver-resealing/index.html",
    'id="hs-search-intent-resealing"',
    '''
  <section id="hs-search-intent-resealing" class="reseal-section alt" aria-labelledby="hs-search-intent-resealing-title">
    <div class="reseal-wrap">
      <p class="eyebrow">Local resealing &amp; restoration</p>
      <h2 id="hs-search-intent-resealing-title">Paver restoration and resealing across Northeast Florida.</h2>
      <p>If you are searching for <strong>paver restoration near me</strong> or <strong>paver sealing near me</strong>, the condition of the old coating matters as much as the new sealer. HydroSeal evaluates whitening, peeling, fading, joint-sand loss, moisture, and coating compatibility before recommending cleaning, resealing, or stripping. <a href="/learning-center/problems/cleaning-resealing-or-stripping">Learn when cleaning, resealing or stripping is appropriate.</a></p>
    </div>
  </section>
''',
)

inject_before_main(
    "paver-sealing/driveways.html",
    'id="hs-search-intent-driveway"',
    '''
  <section id="hs-search-intent-driveway" class="dw-section dw-section--soft" aria-labelledby="hs-search-intent-driveway-title">
    <div class="dw-shell">
      <span class="dw-kicker">Driveway service near you</span>
      <h2 id="hs-search-intent-driveway-title">Driveway paver sealing for Jacksonville and nearby communities.</h2>
      <p class="dw-lead">Homeowners searching for <strong>driveway paver sealing near me</strong> can use HydroSeal for professional cleaning, joint-sand restoration, and breathable sealing throughout Jacksonville, St. Johns County, Ponte Vedra, Nocatee, Orange Park, Fleming Island, and nearby Northeast Florida areas. <a href="/get-a-quote">Request a driveway quote.</a></p>
    </div>
  </section>
''',
)

inject_before_main(
    "paver-sealing/travertine-sealing.html",
    'id="hs-search-intent-travertine"',
    '''
  <section id="hs-search-intent-travertine" class="section" aria-labelledby="hs-search-intent-travertine-title">
    <div class="container">
      <p class="eyebrow">Natural-stone service near you</p>
      <h2 id="hs-search-intent-travertine-title">Travertine sealing for Northeast Florida pool decks and patios.</h2>
      <p>If you are searching for <strong>travertine sealing near me</strong>, HydroSeal provides material-specific cleaning and protection for travertine pool decks, patios, and outdoor living areas across Jacksonville, St. Johns County, Ponte Vedra, Nocatee, and surrounding communities. Natural stone is evaluated for porosity, moisture, fill condition, staining, and previous treatments before sealing. <a href="/get-a-quote">Request a travertine quote.</a></p>
    </div>
  </section>
''',
)

inject_before_main(
    "service-areas/st-johns-county/index.html",
    'id="hs-search-intent-st-johns"',
    '''
  <section id="hs-search-intent-st-johns" class="section" aria-labelledby="hs-search-intent-st-johns-title">
    <div class="container">
      <p class="eyebrow">St. Johns County paver sealing</p>
      <h2 id="hs-search-intent-st-johns-title">Paver sealing in St. Johns and St. Augustine, Florida.</h2>
      <p>HydroSeal provides <strong>paver sealing in St. Johns, FL</strong> and serves homeowners looking for <strong>paver sealing in St. Augustine, FL</strong>, along with Nocatee, Ponte Vedra, Palm Valley, Julington Creek, World Golf Village, and nearby St. Johns County communities. Services include driveway sealing, pool deck sealing, paver cleaning, joint-sand restoration, and travertine sealing. <a href="/get-a-quote">Request a local paver sealing quote.</a></p>
    </div>
  </section>
''',
)

analytics = Path("assets/js/analytics.js")
text = analytics.read_text(encoding="utf-8")
text, removed = re.subn(
    r"\n  function ensureSearchIntentCopyLoader\(\) \{.*?\n  \}\n",
    "\n",
    text,
    count=1,
    flags=re.S,
)
text = text.replace("  ensureSearchIntentCopyLoader();\n", "")
if "search-intent-copy.js" in text:
    raise SystemExit("search intent loader still present in analytics.js")
analytics.write_text(text, encoding="utf-8")
print(f"analytics loader removed: {removed}")

injected = Path("assets/js/search-intent-copy.js")
if injected.exists():
    injected.unlink()
    print("removed assets/js/search-intent-copy.js")

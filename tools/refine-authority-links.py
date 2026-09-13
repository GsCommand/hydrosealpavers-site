from pathlib import Path

p = Path('learning-center/hiring/how-to-choose-a-paver-sealing-company-in-northeast-florida/index.html')
text = p.read_text(encoding='utf-8')
old = '<h2>Local experience matters, but proximity is not enough</h2><p><a href="/service-areas/jacksonville">Jacksonville</a>, <a href="/service-areas/st-johns-county">St. Johns County</a>, and <a href="/service-areas/clay-county">Clay County</a> share heat and rain, but properties differ in irrigation, shade, drainage, salt exposure, pool chemicals, traffic, and paver type. A contractor should explain the conditions at your property rather than relying on a generic “Florida-proof” process.</p>'
new = '<h2>Local experience matters, but proximity is not enough</h2><p><a href="/service-areas/jacksonville">Jacksonville</a>, Nocatee, Ponte Vedra, Palm Valley, the Beaches, and <a href="/service-areas/clay-county">Clay County</a> share heat and rain, but properties differ in irrigation, shade, drainage, salt exposure, pool chemicals, traffic, and paver type. A contractor should explain the conditions at your property rather than relying on a generic “Florida-proof” process. For broader local coverage, see HydroSeal’s <a href="/service-areas/st-johns-county">St. Johns County service area</a>.</p>'
if new not in text:
    if old not in text:
        raise SystemExit('Expected hiring-guide paragraph not found')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')
print('refined hiring-guide contextual links')

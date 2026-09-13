#!/usr/bin/env python3
from pathlib import Path

replacements = {
    Path("service-areas/clay-county/index.html"): [
        (
            '"areaServed":[{"@type":"AdministrativeArea","name":"St. Johns County, FL"},{"@type":"AdministrativeArea","name":"Duval County, FL"},{"@type":"AdministrativeArea","name":"Clay County, FL"}]',
            '"areaServed":[{"@type":"AdministrativeArea","name":"Clay County, FL"},{"@type":"Place","name":"Fleming Island, FL"},{"@type":"Place","name":"Orange Park, FL"},{"@type":"Place","name":"Oakleaf Plantation, FL"},{"@type":"Place","name":"Middleburg, FL"}]'
        ),
    ],
    Path("service-areas/st-johns-county/index.html"): [
        (
            '"description":"HydroSeal provides professional paver and brick paver sealing in St. Johns, FL.","areaServed":[{"@type":"City","name":"St. Johns, FL"}]',
            '"description":"HydroSeal provides professional paver and brick paver sealing across St. Johns County, Florida.","areaServed":[{"@type":"AdministrativeArea","name":"St. Johns County, FL"},{"@type":"Place","name":"Nocatee, FL"},{"@type":"Place","name":"Ponte Vedra, FL"},{"@type":"Place","name":"Ponte Vedra Beach, FL"},{"@type":"Place","name":"Fruit Cove, FL"},{"@type":"Place","name":"Julington Creek, FL"},{"@type":"Place","name":"Durbin Crossing, FL"},{"@type":"Place","name":"TrailMark, FL"}]'
        ),
        (
            '"name":"Professional Brick Paver Sealing in St. Johns, FL","serviceType":["Professional Paver Sealing","Brick Paver Sealing"],"description":"HydroSeal provides professional brick paver sealing in St. Johns, FL for driveways, patios, pool decks, and walkways.","provider":{"@id":"https://hydrosealpavers.com/#business"},"areaServed":[{"@type":"City","name":"St. Johns, FL"}]',
            '"name":"Professional Paver Sealing in St. Johns County, FL","serviceType":["Professional Paver Sealing","Brick Paver Sealing"],"description":"HydroSeal provides professional paver sealing across St. Johns County, Florida for driveways, patios, pool decks, and walkways.","provider":{"@id":"https://hydrosealpavers.com/#business"},"areaServed":[{"@type":"AdministrativeArea","name":"St. Johns County, FL"},{"@type":"Place","name":"Nocatee, FL"},{"@type":"Place","name":"Ponte Vedra, FL"},{"@type":"Place","name":"Ponte Vedra Beach, FL"},{"@type":"Place","name":"Fruit Cove, FL"},{"@type":"Place","name":"Julington Creek, FL"},{"@type":"Place","name":"Durbin Crossing, FL"},{"@type":"Place","name":"TrailMark, FL"}]'
        ),
    ],
}

changed = []
for path, pairs in replacements.items():
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in pairs:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"Expected exactly one match in {path}, found {count}: {old[:90]}")
        text = text.replace(old, new, 1)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(str(path))

print("Updated:")
for item in changed:
    print(f"- {item}")

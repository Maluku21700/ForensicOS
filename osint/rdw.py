#!/usr/bin/env python3

import json
import re
import urllib.request
import urllib.parse


API = "https://opendata.rdw.nl/resource/m9d7-ebf2.json"


def clean_plate(plate):
    return re.sub(r"[^A-Z0-9]", "", plate.upper())


def lookup_plate(plate):
    plate = clean_plate(plate)

    if not plate:
        raise ValueError("Geen kenteken ingevoerd.")

    query = urllib.parse.urlencode({
        "$where": f"kenteken='{plate}'",
        "$limit": 1,
    })

    url = API + "?" + query

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ForensicOS/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    if not data:
        return None

    return data[0]


def show_vehicle(vehicle):
    fields = [
        ("Kenteken", "kenteken"),
        ("Voertuigsoort", "voertuigsoort"),
        ("Merk", "merk"),
        ("Handelsbenaming", "handelsbenaming"),
        ("Inrichting", "inrichting"),
        ("Kleur 1", "eerste_kleur"),
        ("Kleur 2", "tweede_kleur"),
        ("Aantal zitplaatsen", "aantal_zitplaatsen"),
        ("Aantal cilinders", "aantal_cilinders"),
        ("Cilinderinhoud", "cilinderinhoud"),
        ("Massa leeg", "massa_ledig_voertuig"),
        ("Massa rijklaar", "massa_rijklaar"),
        ("Catalogusprijs", "catalogusprijs"),
        ("Max snelheid", "maximale_constructiesnelheid"),
        ("WAM verzekerd", "wam_verzekerd"),
        ("Eerste toelating", "datum_eerste_toelating"),
        ("Eerste toelating NL", "datum_eerste_tenaamstelling_in_nederland"),
        ("Tenaamstelling", "datum_tenaamstelling"),
        ("APK vervaldatum", "vervaldatum_apk"),
    ]

    for label, key in fields:
        value = vehicle.get(key)

        if value not in (None, ""):
            print(f"{label:<24}: {value}")


def main():
    print("================================")
    print("        FORENICOS RDW")
    print("================================")
    print()
    print("RDW voertuiggegevens")
    print()

    plate = input("Kenteken: ").strip()

    try:
        vehicle = lookup_plate(plate)

        print()

        if vehicle is None:
            print("Geen voertuig gevonden.")
        else:
            show_vehicle(vehicle)

    except urllib.error.HTTPError as error:
        print("HTTP-fout:", error.code)

    except urllib.error.URLError as error:
        print("Netwerkfout:", error.reason)

    except TimeoutError:
        print("FOUT: verbinding duurde te lang.")

    except ValueError as error:
        print("FOUT:", error)

    print()
    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

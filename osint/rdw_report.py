#!/usr/bin/env python3

import json
import re
import urllib.parse
import urllib.request


VEHICLE_API = "https://opendata.rdw.nl/resource/m9d7-ebf2.json"


def clean_plate(plate):
    return re.sub(r"[^A-Z0-9]", "", plate.upper())


def lookup(plate):
    plate = clean_plate(plate)

    if not plate:
        raise ValueError("Ongeldig kenteken.")

    params = urllib.parse.urlencode({
        "$where": f"kenteken='{plate}'",
        "$limit": 1
    })

    url = VEHICLE_API + "?" + params

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ForensicOS/1.0"}
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


def show(label, data, key):
    value = data.get(key)

    if value not in (None, ""):
        print(f"{label:<30}: {value}")


def main():
    print("========================================")
    print("       FORENICOS RDW VEHICLE REPORT")
    print("========================================")
    print()

    plate = input("Kenteken: ")

    try:
        results = lookup(plate)

        if not results:
            print()
            print("Geen voertuig gevonden.")
            input("ENTER...")
            return

        vehicle = results[0]

        print()
        print("IDENTIFICATIE")
        print("----------------------------------------")

        show("Kenteken", vehicle, "kenteken")
        show("Merk", vehicle, "merk")
        show("Handelsbenaming", vehicle, "handelsbenaming")
        show("Voertuigsoort", vehicle, "voertuigsoort")
        show("Inrichting", vehicle, "inrichting")

        print()
        print("DATUMS")
        print("----------------------------------------")

        show(
            "Eerste toelating",
            vehicle,
            "datum_eerste_toelating"
        )

        show(
            "Eerste toelating NL",
            vehicle,
            "datum_eerste_tenaamstelling_in_nederland"
        )

        show(
            "Tenaamstelling",
            vehicle,
            "datum_tenaamstelling"
        )

        show(
            "APK vervaldatum",
            vehicle,
            "vervaldatum_apk"
        )

        print()
        print("TECHNIEK")
        print("----------------------------------------")

        show(
            "Cilinderinhoud",
            vehicle,
            "cilinderinhoud"
        )

        show(
            "Aantal cilinders",
            vehicle,
            "aantal_cilinders"
        )

        show(
            "Massa leeg",
            vehicle,
            "massa_ledig_voertuig"
        )

        show(
            "Massa rijklaar",
            vehicle,
            "massa_rijklaar"
        )

        show(
            "Max snelheid",
            vehicle,
            "maximale_constructiesnelheid"
        )

        show(
            "Aantal zitplaatsen",
            vehicle,
            "aantal_zitplaatsen"
        )

        print()
        print("BRANDSTOF / MILIEU")
        print("----------------------------------------")

        show(
            "Brandstof",
            vehicle,
            "brandstof_naam"
        )

        show(
            "CO2 uitstoot",
            vehicle,
            "co2_uitstoot_gecombineerd"
        )

        show(
            "Emissieklasse",
            vehicle,
            "emissiecode"
        )

        print()
        print("KLEUR")
        print("----------------------------------------")

        show(
            "Eerste kleur",
            vehicle,
            "eerste_kleur"
        )

        show(
            "Tweede kleur",
            vehicle,
            "tweede_kleur"
        )

        print()
        print("========================================")
        print("       RDW ANALYSE KLAAR")
        print("========================================")

    except urllib.error.URLError as error:
        print()
        print("Netwerkfout:", error)

    except ValueError as error:
        print()
        print("FOUT:", error)

    print()
    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

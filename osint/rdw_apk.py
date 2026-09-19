#!/usr/bin/env python3

import json
import re
import urllib.parse
import urllib.request


API = "https://opendata.rdw.nl/resource/8ys7-d773.json"


def clean_plate(plate):
    return re.sub(r"[^A-Z0-9]", "", plate.upper())


def lookup(plate):
    plate = clean_plate(plate)

    if not plate:
        raise ValueError("Geen geldig kenteken.")

    params = urllib.parse.urlencode({
        "$where": f"kenteken='{plate}'",
        "$limit": 100,
    })

    url = API + "?" + params

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ForensicOS/1.0"}
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


def main():
    print("========================================")
    print("        FORENICOS RDW APK")
    print("========================================")
    print()

    plate = input("Kenteken: ").strip()

    try:
        results = lookup(plate)

        print()

        if not results:
            print("Geen APK-gegevens gevonden.")
        else:
            print("APK-RESULTATEN")
            print("----------------------------------------")

            for index, item in enumerate(results, 1):

                print()
                print(f"Resultaat #{index}")

                for key, value in item.items():
                    if value not in (None, ""):
                        label = key.replace("_", " ")
                        print(f"{label:<35}: {value}")

                print("----------------------------------------")

            print()
            print("Aantal resultaten:", len(results))

    except urllib.error.HTTPError as error:
        print("HTTP-fout:", error.code)

    except urllib.error.URLError as error:
        print("Netwerkfout:", error.reason)

    except ValueError as error:
        print("FOUT:", error)

    print()
    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

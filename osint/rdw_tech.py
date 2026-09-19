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
        "$limit": 20,
    })

    url = API + "?" + params

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ForensicOS/1.0"}
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def show_value(label, value):
    if value not in (None, ""):
        print(f"{label:<38}: {value}")


def main():
    print("========================================")
    print("       FORENICOS RDW TECH")
    print("========================================")
    print()
    print("Technische / brandstofgegevens")
    print()

    plate = input("Kenteken: ").strip()

    try:
        results = lookup(plate)

        print()

        if not results:
            print("Geen technische gegevens gevonden.")
        else:
            for index, vehicle in enumerate(results, 1):

                print("========================================")
                print(f"RESULTAAT #{index}")
                print("========================================")

                show_value("Kenteken", vehicle.get("kenteken"))
                show_value("Brandstof", vehicle.get("brandstof_omschrijving"))
                show_value("Brandstof volgnummer", vehicle.get("brandstof_volgnummer"))

                print()
                print("--- VERBRUIK / EMISSIE ---")

                show_value(
                    "CO2 gecombineerd WLTP",
                    vehicle.get("emissie_co2_gecombineerd_wltp")
                )

                show_value(
                    "CO2 gewogen gecombineerd WLTP",
                    vehicle.get("emissie_co2_gewogen_gecombineerd_wltp")
                )

                show_value(
                    "Brandstofverbruik WLTP",
                    vehicle.get("brandstof_verbruik_gecombineerd_wltp")
                )

                show_value(
                    "Brandstofverbruik gewogen WLTP",
                    vehicle.get("brandstof_verbruik_gewogen_wltp")
                )

                show_value(
                    "Elektrisch verbruik WLTP",
                    vehicle.get("elektrisch_verbruik_enkel_elektrisch_wltp")
                )

                print()
                print("--- ELEKTRISCH ---")

                show_value(
                    "Elektrisch bereik",
                    vehicle.get("elektrisch_bereik")
                )

                show_value(
                    "Extern oplaadbaar",
                    vehicle.get("extern_oplaadbaar")
                )

                print()
                print("--- EMISSIE ---")

                show_value(
                    "Deeltjes type 1 WLTP",
                    vehicle.get("emissie_deeltjes_type1_wltp")
                )

                show_value(
                    "Deeltjes type 2 WLTP",
                    vehicle.get("emissie_deeltjes_type2_wltp")
                )

                print()

            print("Aantal resultaten:", len(results))

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

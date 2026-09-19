#!/usr/bin/env python3

import os


SIGNATURES = {
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"%PDF-": "PDF",
    b"GIF87a": "GIF",
    b"GIF89a": "GIF",
    b"PK\x03\x04": "ZIP",
}


def scan_for_signatures(filename):
    with open(filename, "rb") as file:
        data = file.read()

    findings = []

    for signature, file_type in SIGNATURES.items():
        start = 0

        while True:
            position = data.find(signature, start)

            if position == -1:
                break

            findings.append({
                "type": file_type,
                "offset": position,
                "signature": signature.hex(),
            })

            start = position + 1

    findings.sort(key=lambda item: item["offset"])

    return findings


def main():
    print("================================")
    print("       FORENICOS CARVER")
    print("================================")
    print()

    filename = input("Te scannen bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        findings = scan_for_signatures(filename)

        print()

        if not findings:
            print("Geen bekende signatures gevonden.")
        else:
            print("Gevonden signatures:")
            print("--------------------------------")

            for item in findings:
                print(
                    "Offset:",
                    item["offset"],
                    "| Type:",
                    item["type"],
                    "| Signature:",
                    item["signature"]
                )

            print("--------------------------------")
            print("Aantal gevonden:", len(findings))

    except PermissionError:
        print()
        print("FOUT: geen toestemming.")

    print()
    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

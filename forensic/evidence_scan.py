#!/usr/bin/env python3

import os
import hashlib
import mimetypes
from datetime import datetime


def sha256_file(filename):
    sha256 = hashlib.sha256()

    with open(filename, "rb") as file:
        while chunk := file.read(1024 * 1024):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_directory(directory):
    results = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)

            try:
                stat = os.stat(path)

                results.append({
                    "path": os.path.abspath(path),
                    "size": stat.st_size,
                    "type": mimetypes.guess_type(path)[0] or "Onbekend",
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                    "sha256": sha256_file(path),
                })

            except (PermissionError, OSError):
                pass

    return results


def main():
    print("================================")
    print("     FORENICOS EVIDENCE SCAN")
    print("================================")
    print()

    directory = input("Map: ").strip()

    if not os.path.isdir(directory):
        print()
        print("FOUT: map bestaat niet.")
        input("Druk ENTER...")
        return

    print()
    print("Evidence scan gestart...")
    print()

    results = scan_directory(directory)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = "evidence_" + timestamp + ".txt"

    with open(output, "w", encoding="utf-8") as report:
        report.write("FORENICOS EVIDENCE SCAN\n")
        report.write("=======================\n\n")
        report.write("Scan tijd: " + str(datetime.now()) + "\n")
        report.write("Map: " + os.path.abspath(directory) + "\n")
        report.write("Aantal bestanden: " + str(len(results)) + "\n\n")

        for item in results:
            report.write("--------------------------------\n")
            report.write("Bestand : " + item["path"] + "\n")
            report.write("Grootte : " + str(item["size"]) + " bytes\n")
            report.write("Type    : " + item["type"] + "\n")
            report.write("Gewijzigd: " + str(item["modified"]) + "\n")
            report.write("SHA-256 : " + item["sha256"] + "\n")

    print("Scan voltooid.")
    print()
    print("Bestanden gevonden:", len(results))
    print("Rapport:", output)
    print()

    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

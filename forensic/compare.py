#!/usr/bin/env python3

import os
import hashlib


def sha256_file(filename):
    sha256 = hashlib.sha256()

    with open(filename, "rb") as file:
        while chunk := file.read(1024 * 1024):
            sha256.update(chunk)

    return sha256.hexdigest()


def compare_files(file1, file2):
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    hash1 = sha256_file(file1)
    hash2 = sha256_file(file2)

    return size1, size2, hash1, hash2


def main():
    print("================================")
    print("      FORENICOS COMPARE")
    print("================================")
    print()

    file1 = input("Bestand 1: ").strip()
    file2 = input("Bestand 2: ").strip()

    if not os.path.isfile(file1):
        print()
        print("FOUT: bestand 1 bestaat niet.")
        input("Druk ENTER...")
        return

    if not os.path.isfile(file2):
        print()
        print("FOUT: bestand 2 bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        size1, size2, hash1, hash2 = compare_files(file1, file2)

        print()
        print("BESTAND 1")
        print("Pad     :", os.path.abspath(file1))
        print("Grootte :", size1, "bytes")
        print("SHA-256 :", hash1)

        print()
        print("BESTAND 2")
        print("Pad     :", os.path.abspath(file2))
        print("Grootte :", size2, "bytes")
        print("SHA-256 :", hash2)

        print()
        print("================================")

        if hash1 == hash2:
            print("RESULTAAT: IDENTIEK")
            print("De bestanden hebben dezelfde inhoud.")
        else:
            print("RESULTAAT: VERSCHILLEND")
            print("De bestanden hebben verschillende inhoud.")

        print("================================")

    except PermissionError:
        print()
        print("FOUT: geen toestemming.")

    print()
    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

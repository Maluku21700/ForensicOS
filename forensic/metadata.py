#!/usr/bin/env python3

import os
import struct
from datetime import datetime


def read_basic_metadata(filename):
    stat = os.stat(filename)

    return {
        "naam": os.path.basename(filename),
        "pad": os.path.abspath(filename),
        "grootte": stat.st_size,
        "inode": stat.st_ino,
        "permissions": oct(stat.st_mode & 0o777),
        "links": stat.st_nlink,
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "accessed": datetime.fromtimestamp(stat.st_atime),
        "changed": datetime.fromtimestamp(stat.st_ctime),
    }


def detect_format(filename):
    with open(filename, "rb") as file:
        header = file.read(16)

    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG image"

    if header.startswith(b"\xff\xd8\xff"):
        return "JPEG image"

    if header.startswith(b"%PDF"):
        return "PDF document"

    if header.startswith(b"PK\x03\x04"):
        return "ZIP/archive"

    if header.startswith(b"\x7fELF"):
        return "ELF executable"

    if header.startswith(b"MZ"):
        return "Windows executable"

    return "Onbekend"


def main():
    print("================================")
    print("      FORENICOS METADATA")
    print("================================")
    print()

    filename = input("Bestand: ").strip()

    try:
        info = read_basic_metadata(filename)
        file_format = detect_format(filename)

        print()
        print("Naam        :", info["naam"])
        print("Pad         :", info["pad"])
        print("Grootte     :", info["grootte"], "bytes")
        print("Inode       :", info["inode"])
        print("Permissions :", info["permissions"])
        print("Links       :", info["links"])
        print("Formaat     :", file_format)
        print("Gewijzigd   :", info["modified"])
        print("Geopend     :", info["accessed"])
        print("Metadata chg:", info["changed"])

    except FileNotFoundError:
        print()
        print("FOUT: bestand niet gevonden.")

    except PermissionError:
        print()
        print("FOUT: geen toestemming.")

    except IsADirectoryError:
        print()
        print("FOUT: dit is een map.")

    print()
    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

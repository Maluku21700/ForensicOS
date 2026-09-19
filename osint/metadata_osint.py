import hashlib
import mimetypes
import os
import re
import sys


KEYWORDS = [
    "gps",
    "latitude",
    "longitude",
    "location",
    "camera",
    "author",
    "producer",
    "software",
    "device",
    "model"
]


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/metadata_osint.py <bestand>")
        return

    path = sys.argv[1]

    if not os.path.isfile(path):
        print("Bestand bestaat niet.")
        return

    print("========== METADATA OSINT ==========")
    print("Name :", os.path.basename(path))
    print("Size :", os.path.getsize(path))
    print("MIME :", mimetypes.guess_type(path)[0])
    print("SHA256:", sha256(path))

    with open(path, "rb") as f:
        data = f.read(2 * 1024 * 1024)

    strings = re.findall(
        rb"[\x20-\x7e]{5,}",
        data
    )

    print("\nPotential indicators:")

    count = 0

    for raw in strings:
        value = raw.decode(
            "ascii",
            errors="ignore"
        )

        if any(
            keyword in value.lower()
            for keyword in KEYWORDS
        ):
            print(value[:300])
            count += 1

            if count >= 30:
                break

    print(
        "\nStrings zijn alleen indicatoren; "
        "geen gegarandeerde metadata."
    )


if __name__ == "__main__":
    main()

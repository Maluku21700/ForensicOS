import os
import re
import sys


def extract(path, minimum=4):
    with open(path, "rb") as f:
        data = f.read(10 * 1024 * 1024)

    pattern = rb"[\x20-\x7e]{%d,}" % minimum

    return [
        x.decode("ascii", errors="ignore")
        for x in re.findall(pattern, data)
    ]


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python forensic/strings.py <bestand>")
        return

    path = sys.argv[1]

    if not os.path.isfile(path):
        print("Bestand bestaat niet.")
        return

    for value in extract(path):
        print(value)


if __name__ == "__main__":
    main()

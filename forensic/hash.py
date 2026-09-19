import hashlib
import os
import sys


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python forensic/hash.py <bestand>")
        return

    path = sys.argv[1]

    if not os.path.isfile(path):
        print("Bestand bestaat niet.")
        return

    print("File   :", path)
    print("SHA256 :", sha256_file(path))


if __name__ == "__main__":
    main()

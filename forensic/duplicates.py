import hashlib
import os
import sys
from collections import defaultdict


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."

    hashes = defaultdict(list)

    for directory, _, files in os.walk(root):
        for filename in files:
            path = os.path.join(directory, filename)

            try:
                hashes[sha256(path)].append(path)
            except Exception:
                pass

    found = 0

    for digest, paths in hashes.items():
        if len(paths) > 1:
            found += 1

            print()
            print("SHA-256:", digest)

            for path in paths:
                print("  ", path)

    print()
    print("Duplicate groups:", found)


if __name__ == "__main__":
    main()

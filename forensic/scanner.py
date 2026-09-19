import hashlib
import os
import sys


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def scan(root):
    count = 0

    for directory, _, files in os.walk(root):
        for filename in files:
            path = os.path.join(directory, filename)

            try:
                size = os.path.getsize(path)
                digest = sha256(path)

                print(
                    f"{path} | {size} bytes | {digest}"
                )

                count += 1

            except (PermissionError, OSError) as e:
                print(f"[ERROR] {path}: {e}")

    print()
    print("Files scanned:", count)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.isdir(root):
        print("Directory bestaat niet.")
        return

    scan(root)


if __name__ == "__main__":
    main()

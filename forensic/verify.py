import hashlib
import sys


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def main():
    if len(sys.argv) != 3:
        print("Gebruik:")
        print("python forensic/verify.py <bestand> <verwachte_sha256>")
        return

    path = sys.argv[1]
    expected = sys.argv[2].lower()

    actual = sha256(path)

    print("Expected:", expected)
    print("Actual  :", actual)

    if actual == expected:
        print("RESULT  : MATCH")
    else:
        print("RESULT  : MISMATCH")


if __name__ == "__main__":
    main()

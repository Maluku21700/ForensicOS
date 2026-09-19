import math
import sys
from collections import Counter


def entropy(data):
    if not data:
        return 0.0

    counts = Counter(data)
    length = len(data)

    return -sum(
        (count / length) *
        math.log2(count / length)
        for count in counts.values()
    )


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python forensic/entropy.py <bestand>")
        return

    path = sys.argv[1]

    with open(path, "rb") as f:
        data = f.read(1024 * 1024)

    value = entropy(data)

    print("File    :", path)
    print("Sample  :", len(data), "bytes")
    print(f"Entropy : {value:.4f} bits/byte")


if __name__ == "__main__":
    main()

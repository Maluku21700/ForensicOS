import os
import sys


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python forensic/hexview.py <bestand>")
        return

    path = sys.argv[1]

    if not os.path.isfile(path):
        print("Bestand bestaat niet.")
        return

    size = 512

    if len(sys.argv) >= 3:
        try:
            size = min(int(sys.argv[2]), 4096)
        except ValueError:
            pass

    with open(path, "rb") as f:
        data = f.read(size)

    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]

        hexpart = " ".join(
            f"{byte:02x}" for byte in chunk
        )

        asciipart = "".join(
            chr(byte) if 32 <= byte <= 126 else "."
            for byte in chunk
        )

        print(
            f"{offset:08x}  "
            f"{hexpart:<47}  "
            f"{asciipart}"
        )


if __name__ == "__main__":
    main()

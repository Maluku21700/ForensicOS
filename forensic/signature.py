import sys


SIGNATURES = {
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"%PDF": "PDF",
    b"GIF87a": "GIF",
    b"GIF89a": "GIF",
    b"PK\x03\x04": "ZIP",
    b"\x7fELF": "ELF",
    b"MZ": "PE/Windows executable"
}


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python forensic/signature.py <bestand>")
        return

    path = sys.argv[1]

    with open(path, "rb") as f:
        header = f.read(32)

    found = False

    for signature, name in SIGNATURES.items():
        if header.startswith(signature):
            print("Signature:", name)
            found = True

    if not found:
        print("Signature: onbekend")


if __name__ == "__main__":
    main()

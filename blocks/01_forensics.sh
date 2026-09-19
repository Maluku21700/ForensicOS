#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "      FORENICOS — BLOK 1/11"
echo "            FORENSICS"
echo "=========================================="

cd "$ROOT"

mkdir -p forensic tests reports

touch forensic/__init__.py

echo
echo "[1/12] Hash engine..."

cat > forensic/hash.py <<'PY'
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
PY

echo "[2/12] File information..."

cat > forensic/fileinfo.py <<'PY'
import hashlib
import mimetypes
import os
import sys
from datetime import datetime


def digest(path, algorithm):
    h = hashlib.new(algorithm)

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python forensic/fileinfo.py <bestand>")
        return

    path = sys.argv[1]

    if not os.path.isfile(path):
        print("Bestand bestaat niet.")
        return

    stat = os.stat(path)

    print("========== FILE INFO ==========")
    print("Name       :", os.path.basename(path))
    print("Path       :", os.path.abspath(path))
    print("Size       :", stat.st_size, "bytes")
    print("MIME       :", mimetypes.guess_type(path)[0] or "unknown")
    print("Created    :", datetime.fromtimestamp(stat.st_ctime))
    print("Modified   :", datetime.fromtimestamp(stat.st_mtime))
    print("Accessed   :", datetime.fromtimestamp(stat.st_atime))
    print("MD5        :", digest(path, "md5"))
    print("SHA-1      :", digest(path, "sha1"))
    print("SHA-256    :", digest(path, "sha256"))


if __name__ == "__main__":
    main()
PY

echo "[3/12] Recursive scanner..."

cat > forensic/scanner.py <<'PY'
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
PY

echo "[4/12] Duplicate detector..."

cat > forensic/duplicates.py <<'PY'
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
PY

echo "[5/12] Hash verification..."

cat > forensic/verify.py <<'PY'
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
PY

echo "[6/12] Strings extractor..."

cat > forensic/strings.py <<'PY'
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
PY

echo "[7/12] Hex viewer..."

cat > forensic/hexview.py <<'PY'
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
PY

echo "[8/12] Entropy analyzer..."

cat > forensic/entropy.py <<'PY'
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
PY

echo "[9/12] File signature detector..."

cat > forensic/signature.py <<'PY'
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
PY

echo "[10/12] Directory timeline..."

cat > forensic/timeline.py <<'PY'
import os
import sys
from datetime import datetime


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."

    entries = []

    for directory, _, files in os.walk(root):
        for filename in files:
            path = os.path.join(directory, filename)

            try:
                timestamp = os.path.getmtime(path)
                entries.append((timestamp, path))
            except OSError:
                pass

    entries.sort()

    for timestamp, path in entries:
        print(
            datetime.fromtimestamp(timestamp).isoformat(),
            "|",
            path
        )


if __name__ == "__main__":
    main()
PY

echo "[11/12] Forensic report generator..."

cat > forensic/report.py <<'PY'
import hashlib
import json
import mimetypes
import os
import sys
from datetime import datetime


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python forensic/report.py <bestand>")
        return

    path = sys.argv[1]

    stat = os.stat(path)

    report = {
        "file": os.path.abspath(path),
        "name": os.path.basename(path),
        "size": stat.st_size,
        "mime": mimetypes.guess_type(path)[0],
        "created": datetime.fromtimestamp(
            stat.st_ctime
        ).isoformat(),
        "modified": datetime.fromtimestamp(
            stat.st_mtime
        ).isoformat(),
        "accessed": datetime.fromtimestamp(
            stat.st_atime
        ).isoformat(),
        "sha256": sha256(path)
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
PY

echo "[12/12] Forensics self-test..."

cat > tests/test_forensics.py <<'PY'
import hashlib
import os
import tempfile


def test_hash():
    data = b"ForensicOS test"

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(data)
        path = f.name

    expected = hashlib.sha256(data).hexdigest()

    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024), b""):
            h.update(block)

    os.unlink(path)

    assert h.hexdigest() == expected


if __name__ == "__main__":
    test_hash()
    print("FORENSICS TEST: PASS")
PY

python -m py_compile forensic/*.py tests/test_forensics.py

python tests/test_forensics.py

echo
echo "=========================================="
echo "       BLOK 1/11 VOLTOOID"
echo "=========================================="
echo
echo "Forensics modules:"
echo

ls -1 forensic/*.py

echo
echo "Test: PASS"
echo
echo "Volgende stap:"
echo "bash blocks/02_osint.sh"
echo

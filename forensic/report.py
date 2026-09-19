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

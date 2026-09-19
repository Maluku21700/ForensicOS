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

import hashlib
import os


def sha256_file(path):
    path = os.path.expanduser(path)

    digest = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            digest.update(chunk)

    return digest.hexdigest()


def collect_file(path):
    path = os.path.abspath(
        os.path.expanduser(path)
    )

    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    stat = os.stat(path)

    return {
        "path": path,
        "filename": os.path.basename(path),
        "size": stat.st_size,
        "sha256": sha256_file(path),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(
            "Gebruik: python -m cases.evidence FILE"
        )
        raise SystemExit(1)

    print(
        collect_file(sys.argv[1])
    )

import hashlib
import os


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def audit_directory(directory):
    results = []

    if not os.path.isdir(directory):
        return results

    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)

            try:
                results.append({
                    "path": path,
                    "size": os.path.getsize(path),
                    "sha256": sha256(path)
                })
            except (PermissionError, FileNotFoundError):
                continue

    return results


def main():
    print("========== FILE INTEGRITY AUDIT ==========\n")

    directory = input(
        "Directory om te controleren [~/ForensicOS]: "
    ).strip()

    if not directory:
        directory = os.path.expanduser("~/ForensicOS")
    else:
        directory = os.path.expanduser(directory)

    results = audit_directory(directory)

    for item in results:
        print(
            f"{item['sha256']}  "
            f"{item['size']:>10}  "
            f"{item['path']}"
        )

    print("\nBestanden:", len(results))


if __name__ == "__main__":
    main()

import os


def main():
    print("========== SUID FILE AUDIT ==========\n")

    roots = ["/usr/bin", "/usr/sbin", "/bin", "/sbin"]
    found = []

    for root in roots:
        if not os.path.isdir(root):
            continue

        for current_root, dirs, files in os.walk(root):
            for name in files:
                path = os.path.join(current_root, name)

                try:
                    mode = os.stat(path).st_mode

                    if mode & 0o4000:
                        found.append(path)

                except (PermissionError, FileNotFoundError):
                    continue

    for path in sorted(set(found)):
        print(path)

    print("\nAantal SUID-bestanden:", len(set(found)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os


def analyze_tree(directory):
    files = 0
    directories = 0
    total_size = 0

    for root, dirs, filenames in os.walk(directory):
        directories += len(dirs)

        for filename in filenames:
            files += 1
            path = os.path.join(root, filename)

            try:
                total_size += os.path.getsize(path)
            except (PermissionError, OSError):
                pass

    return files, directories, total_size


def print_tree(directory, prefix=""):
    try:
        entries = sorted(os.listdir(directory))
    except (PermissionError, OSError):
        print(prefix + "[geen toegang]")
        return

    for index, name in enumerate(entries):
        path = os.path.join(directory, name)

        last = index == len(entries) - 1
        branch = "└── " if last else "├── "

        print(prefix + branch + name)

        if os.path.isdir(path) and not os.path.islink(path):
            new_prefix = prefix + ("    " if last else "│   ")
            print_tree(path, new_prefix)


def main():
    print("================================")
    print("       FORENICOS TREE")
    print("================================")
    print()

    directory = input("Map: ").strip()

    if not os.path.isdir(directory):
        print()
        print("FOUT: map bestaat niet.")
        input("Druk ENTER...")
        return

    print()
    print("Mappenstructuur:")
    print()

    print_tree(directory)

    files, directories, total_size = analyze_tree(directory)

    print()
    print("================================")
    print("STATISTIEKEN")
    print("================================")
    print("Bestanden :", files)
    print("Mappen    :", directories)
    print("Totale grootte:", total_size, "bytes")
    print()

    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

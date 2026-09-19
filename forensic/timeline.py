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

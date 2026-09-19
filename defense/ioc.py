import os


IOC_FILE = os.path.expanduser(
    "~/ForensicOS/config/ioc.txt"
)


def main():
    print("\n========== IOC SCANNER ==========\n")

    if not os.path.exists(IOC_FILE):
        print("Geen IOC database gevonden.")
        print()
        print("Bestand:")
        print(IOC_FILE)
        return

    with open(IOC_FILE, errors="ignore") as f:
        iocs = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    print("IOC entries:", len(iocs))

    if not iocs:
        return

    root = input("Directory om te scannen: ").strip()

    if not os.path.isdir(root):
        print("Directory bestaat niet.")
        return

    for current, dirs, files in os.walk(root):
        for filename in files:
            path = os.path.join(current, filename)

            try:
                with open(path, errors="ignore") as f:
                    content = f.read(2 * 1024 * 1024)

                for ioc in iocs:
                    if ioc in content:
                        print("[MATCH]", path, "=>", ioc)

            except Exception:
                pass


if __name__ == "__main__":
    main()

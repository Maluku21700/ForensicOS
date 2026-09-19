import importlib
import os
import sys


ROOT = os.path.expanduser("~/ForensicOS")

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


MODULES = {
    "1": ("FORENSICS", "forensic"),
    "2": ("OSINT", "osint"),
    "3": ("RF / RTL-SDR", "rf"),
    "4": ("NETWORK SWEEP", "sweep"),
    "5": ("SURVEILLANCE", "surveillance"),
    "6": ("DEFENSE / LAB", "defense"),
    "7": ("TERMINAL", "terminal"),
    "8": ("SYSTEM", "system"),
    "9": ("CASE MANAGEMENT", "cases"),
}


def banner():
    print("""
========================================
            FORENICOS
          ALPHA BETA ALPHA
========================================
""")


def discover(directory):
    path = os.path.join(ROOT, directory)

    if not os.path.isdir(path):
        return []

    modules = []

    for filename in sorted(os.listdir(path)):
        if not filename.endswith(".py"):
            continue

        if filename == "__init__.py":
            continue

        if filename.startswith("_"):
            continue

        modules.append(
            filename[:-3]
        )

    return modules


def run_module(directory, module_name):
    full_name = f"{directory}.{module_name}"

    try:
        module = importlib.import_module(full_name)
    except Exception as e:
        print("\nModule kon niet geladen worden:")
        print(e)
        input("\nENTER...")
        return

    if not hasattr(module, "main"):
        print(
            f"\n{full_name} heeft geen main() functie."
        )
        input("\nENTER...")
        return

    try:
        module.main()
    except KeyboardInterrupt:
        print("\n\nGestopt door gebruiker.")
    except Exception as e:
        print("\nModule fout:")
        print(e)

    input("\nENTER...")


def submenu(title, directory):
    while True:
        modules = discover(directory)

        print("\n")
        print("=" * 40)
        print(title)
        print("=" * 40)

        if not modules:
            print("Geen modules gevonden.")
            input("\nENTER...")
            return

        for index, module in enumerate(
            modules,
            start=1
        ):
            print(
                f"[{index}] {module}"
            )

        print("[0] TERUG")

        choice = input(
            f"\n{title} > "
        ).strip()

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            module_name = modules[index]
        except (
            ValueError,
            IndexError
        ):
            print("Ongeldige keuze.")
            continue

        run_module(
            directory,
            module_name
        )


def main():
    while True:
        banner()

        for key, (name, directory) in MODULES.items():
            print(
                f"[{key}] {name}"
            )

        print("[0] EXIT")

        choice = input(
            "\nForensicOS > "
        ).strip()

        if choice == "0":
            print("\nForensicOS afgesloten.")
            break

        if choice in MODULES:
            name, directory = MODULES[choice]

            submenu(
                name,
                directory
            )
        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()

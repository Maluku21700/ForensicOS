#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 10/11"
echo "          CORE / LAUNCHER"
echo "=========================================="

cd "$ROOT"

mkdir -p core config logs reports tests

echo
echo "[1/4] Configuration..."

cat > config/config.json <<'JSON'
{
  "name": "ForensicOS",
  "codename": "Alpha Beta Alpha",
  "version": "0.1.0",
  "language": "nl",
  "paths": {
    "cases": "cases",
    "reports": "reports",
    "logs": "logs",
    "tests": "tests"
  },
  "modules": {
    "forensics": "forensic",
    "osint": "osint",
    "rf": "rf",
    "sweep": "sweep",
    "surveillance": "surveillance",
    "defense": "defense",
    "terminal": "terminal",
    "system": "system",
    "cases": "cases"
  }
}
JSON

echo "[2/4] Core utilities..."

cat > core/utils.py <<'PY'
import json
import os


ROOT = os.path.expanduser("~/ForensicOS")


def load_config():
    path = os.path.join(
        ROOT,
        "config",
        "config.json"
    )

    with open(
        path,
        encoding="utf-8"
    ) as f:
        return json.load(f)


def clear_screen():
    os.system("clear")


def pause():
    input("\nDruk ENTER om door te gaan...")


def module_files(directory):
    path = os.path.join(ROOT, directory)

    if not os.path.isdir(path):
        return []

    return sorted(
        name[:-3]
        for name in os.listdir(path)
        if name.endswith(".py")
        and name != "__init__.py"
        and not name.startswith("_")
    )
PY

echo "[3/4] Main launcher..."

cat > core/main.py <<'PY'
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
PY

echo "[4/4] Core tests..."

cat > tests/test_core.py <<'PY'
import json
import os
import sys


ROOT = os.path.expanduser("~/ForensicOS")

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def test_config():
    path = os.path.join(
        ROOT,
        "config",
        "config.json"
    )

    assert os.path.exists(path)

    with open(
        path,
        encoding="utf-8"
    ) as f:
        config = json.load(f)

    assert config["name"] == "ForensicOS"
    assert config["codename"] == "Alpha Beta Alpha"
    assert "modules" in config


def test_main_import():
    import core.main

    assert core.main.MODULES


def test_directories():
    required = [
        "forensic",
        "osint",
        "rf",
        "sweep",
        "surveillance",
        "defense",
        "terminal",
        "system",
        "cases",
    ]

    for directory in required:
        assert os.path.isdir(
            os.path.join(
                ROOT,
                directory
            )
        )


if __name__ == "__main__":
    test_config()
    test_main_import()
    test_directories()

    print("CORE TEST: PASS")
PY

echo
echo "[TEST] Compiling core..."

python -m py_compile core/*.py tests/test_core.py

echo "[TEST] Running core test..."

PYTHONPATH="$ROOT" python tests/test_core.py

echo
echo "=========================================="
echo "       BLOK 10/11 VOLTOOID"
echo "=========================================="

echo
echo "Core:"
ls -1 core/*.py

echo
echo "Test: PASS"

echo
echo "Launcher test:"
echo "python core/main.py"

echo
echo "Volgende:"
echo "bash blocks/11_tests.sh"

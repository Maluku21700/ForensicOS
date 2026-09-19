#!/bin/bash

set -e

PROJECT="$HOME/ForensicOS"

echo "=============================================="
echo "       FORENICOS FULL BACKEND INSTALL"
echo "       ALPHA BETA ALPHA"
echo "=============================================="
echo

cd "$PROJECT"

echo "[1/12] Mappen maken..."

mkdir -p \
    core \
    forensic \
    osint \
    rf \
    sweep \
    surveillance \
    defense \
    terminal \
    system \
    cases \
    config \
    reports \
    logs \
    tests

for dir in \
    forensic \
    osint \
    rf \
    sweep \
    surveillance \
    defense \
    terminal \
    system \
    cases
do
    touch "$dir/__init__.py"
done

echo "[2/12] Python omgeving controleren..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

python -m pip install --upgrade pip >/dev/null 2>&1 || true

echo "[3/12] Basisconfiguratie..."

cat > config/config.json <<'JSON'
{
    "name": "ForensicOS",
    "codename": "Alpha Beta Alpha",
    "version": "0.1.0",
    "mode": "backend",
    "gui": false,
    "logging": true,
    "offline_first": true,
    "max_case_users": 2
}
JSON

echo "[4/12] Logger..."

cat > core/logger.py <<'PY'
import logging
import os

BASE = os.path.expanduser("~/ForensicOS")
LOG_DIR = os.path.join(BASE, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "forensicOS.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("ForensicOS")
PY

echo "[5/12] System module..."

cat > system/info.py <<'PY'
import os
import platform
import shutil
import subprocess


def cmd(command):
    try:
        return subprocess.check_output(
            command,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "N/A"


def main():
    print("\n========== SYSTEM INFO ==========\n")

    print("Hostname :", platform.node())
    print("OS       :", platform.platform())
    print("Kernel   :", platform.release())
    print("Arch     :", platform.machine())
    print("Python   :", platform.python_version())
    print("CPU      :", platform.processor())
    print("CPU cores:", os.cpu_count())

    ram = cmd(["free", "-h"])
    print("\nRAM:")
    print(ram)

    disk = shutil.disk_usage("/")
    print("\nDisk:")
    print(f"Total: {disk.total / 1024**3:.1f} GB")
    print(f"Used : {disk.used / 1024**3:.1f} GB")
    print(f"Free : {disk.free / 1024**3:.1f} GB")

    print("\nUptime:")
    print(cmd(["uptime", "-p"]))

    temp = "/sys/class/thermal/thermal_zone0/temp"

    if os.path.exists(temp):
        try:
            with open(temp) as f:
                value = int(f.read()) / 1000
            print(f"\nCPU temperature: {value:.1f} °C")
        except Exception:
            pass


if __name__ == "__main__":
    main()
PY

echo "[6/12] Defense modules..."

cat > defense/processes.py <<'PY'
import subprocess


def main():
    print("\n========== PROCESS ANALYZER ==========\n")

    result = subprocess.run(
        ["ps", "aux", "--sort=-%cpu"],
        capture_output=True,
        text=True
    )

    print(result.stdout)


if __name__ == "__main__":
    main()
PY


cat > defense/services.py <<'PY'
import subprocess


def main():
    print("\n========== SERVICE ANALYZER ==========\n")

    try:
        result = subprocess.run(
            ["systemctl", "--type=service", "--no-pager"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY


cat > defense/persistence.py <<'PY'
import os
import subprocess


PATHS = [
    "/etc/systemd/system",
    "/etc/cron.d",
    "/etc/cron.daily",
    "/etc/cron.hourly",
    "/etc/cron.monthly",
    "/etc/cron.weekly",
    os.path.expanduser("~/.config/systemd/user"),
    os.path.expanduser("~/.config/autostart")
]


def main():
    print("\n========== PERSISTENCE SCANNER ==========\n")

    for path in PATHS:
        print(f"\n--- {path} ---")

        if not os.path.exists(path):
            print("Niet aanwezig.")
            continue

        if os.path.isdir(path):
            try:
                print(
                    subprocess.check_output(
                        ["ls", "-la", path],
                        text=True
                    )
                )
            except Exception as e:
                print("FOUT:", e)
        else:
            print(path)

    print("\nDit is een diagnostische scan.")
    print("Een gevonden entry is niet automatisch malware.")


if __name__ == "__main__":
    main()
PY


cat > defense/integrity.py <<'PY'
import hashlib
import os


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def main():
    print("\n========== FILE INTEGRITY ==========\n")

    path = input("Bestand: ").strip()

    if not os.path.isfile(path):
        print("Bestand bestaat niet.")
        return

    try:
        print("SHA-256:")
        print(sha256(path))
    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY


cat > defense/ioc.py <<'PY'
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
PY


cat > config/ioc.txt <<'TXT'
# ForensicOS local IOC database
# Voeg alleen indicatoren toe die je zelf wilt controleren.
TXT

echo "[7/12] Network modules..."

cat > sweep/network.py <<'PY'
import socket
import subprocess


def run(command):
    try:
        return subprocess.check_output(
            command,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "N/A"


def main():
    print("\n========== NETWORK SWEEP ==========\n")

    print("Hostname:")
    print(socket.gethostname())

    print("\nInterfaces:")
    print(run(["ip", "-brief", "addr"]))

    print("\nRoutes:")
    print(run(["ip", "route"]))

    print("\nARP/Neighbors:")
    print(run(["ip", "neigh"]))


if __name__ == "__main__":
    main()
PY


cat > surveillance/connections.py <<'PY'
import subprocess


def main():
    print("\n========== CONNECTION MONITOR ==========\n")

    try:
        result = subprocess.run(
            ["ss", "-tunap"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY


cat > surveillance/listening.py <<'PY'
import subprocess


def main():
    print("\n========== LISTENING PORTS ==========\n")

    try:
        result = subprocess.run(
            ["ss", "-lntup"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[8/12] RF module..."

cat > rf/device.py <<'PY'
import subprocess


def main():
    print("\n========== RTL-SDR DEVICE ==========\n")

    try:
        result = subprocess.run(
            ["rtl_test", "-t"],
            capture_output=True,
            text=True,
            timeout=10
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr)

    except FileNotFoundError:
        print("rtl_test is niet geïnstalleerd.")
        print("Installatie:")
        print("sudo apt install rtl-sdr")

    except subprocess.TimeoutExpired:
        print("RTL-SDR test timeout.")


if __name__ == "__main__":
    main()
PY


cat > rf/info.py <<'PY'
import subprocess


def main():
    print("\n========== RF USB DEVICES ==========\n")

    try:
        print(
            subprocess.check_output(
                ["lsusb"],
                text=True
            )
        )
    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[9/12] Case manager..."

cat > cases/manager.py <<'PY'
import hashlib
import json
import os
import shutil
from datetime import datetime


BASE = os.path.expanduser("~/ForensicOS/cases")


def load(case):
    path = os.path.join(BASE, case, "case.json")

    if not os.path.isfile(path):
        raise FileNotFoundError("Case bestaat niet.")

    with open(path) as f:
        return json.load(f)


def save(case, data):
    path = os.path.join(BASE, case, "case.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def new_case():
    name = input("Case naam: ").strip()

    if not name:
        return

    safe = "".join(
        c for c in name
        if c.isalnum() or c in "_-"
    )

    path = os.path.join(BASE, safe)

    if os.path.exists(path):
        print("Case bestaat al.")
        return

    os.makedirs(os.path.join(path, "evidence"))
    os.makedirs(os.path.join(path, "reports"))

    data = {
        "case": safe,
        "created": datetime.now().isoformat(),
        "notes": [],
        "evidence": []
    }

    save(safe, data)

    print("Case aangemaakt:", safe)


def list_cases():
    print("\n========== CASES ==========\n")

    if not os.path.isdir(BASE):
        print("Geen cases.")
        return

    cases = [
        x for x in os.listdir(BASE)
        if os.path.isdir(os.path.join(BASE, x))
    ]

    if not cases:
        print("Geen cases.")
        return

    for case in sorted(cases):
        print("-", case)


def add_note():
    case = input("Case: ").strip()

    try:
        data = load(case)
    except FileNotFoundError as e:
        print(e)
        return

    note = input("Notitie: ").strip()

    data["notes"].append({
        "time": datetime.now().isoformat(),
        "text": note
    })

    save(case, data)

    print("Opgeslagen.")


def add_evidence():
    case = input("Case: ").strip()
    source = input("Bestand: ").strip()

    try:
        data = load(case)
    except FileNotFoundError as e:
        print(e)
        return

    if not os.path.isfile(source):
        print("Bestand bestaat niet.")
        return

    destination = os.path.join(
        BASE,
        case,
        "evidence",
        os.path.basename(source)
    )

    shutil.copy2(source, destination)

    h = hashlib.sha256()

    with open(destination, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    data["evidence"].append({
        "file": os.path.basename(destination),
        "sha256": h.hexdigest(),
        "added": datetime.now().isoformat()
    })

    save(case, data)

    print("Evidence toegevoegd.")
    print("SHA-256:", h.hexdigest())


def main():
    while True:
        print("\n========== CASE MANAGER ==========")
        print("[1] Nieuwe case")
        print("[2] Cases")
        print("[3] Notitie")
        print("[4] Evidence toevoegen")
        print("[0] Terug")

        choice = input("\nCase > ").strip()

        if choice == "1":
            new_case()
        elif choice == "2":
            list_cases()
        elif choice == "3":
            add_note()
        elif choice == "4":
            add_evidence()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
PY

echo "[10/12] Terminal utilities..."

cat > terminal/commands.py <<'PY'
import os
import subprocess


def main():
    print("\n========== TERMINAL TOOLS ==========\n")

    print("PWD :", os.getcwd())

    while True:
        command = input("ForensicOS-shell > ").strip()

        if command in ("exit", "quit", "back"):
            break

        if not command:
            continue

        try:
            subprocess.run(
                command,
                shell=True
            )
        except Exception as e:
            print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[11/12] Centrale launcher..."

cat > core/main.py <<'PY'
#!/usr/bin/env python3

import os
import subprocess
import sys


ROOT = os.path.expanduser("~/ForensicOS")


SECTIONS = [
    ("FORENSICS", "forensic"),
    ("OSINT", "osint"),
    ("RF / RTL-SDR", "rf"),
    ("NETWORK SWEEP", "sweep"),
    ("SURVEILLANCE", "surveillance"),
    ("DEFENSE / LAB", "defense"),
    ("TERMINAL", "terminal"),
    ("SYSTEM", "system"),
    ("CASE MANAGEMENT", "cases")
]


def modules(directory):
    path = os.path.join(ROOT, directory)

    if not os.path.isdir(path):
        return []

    return sorted(
        file[:-3]
        for file in os.listdir(path)
        if file.endswith(".py")
        and file != "__init__.py"
    )


def run(directory, module):
    path = os.path.join(
        ROOT,
        directory,
        module + ".py"
    )

    print()
    print("=" * 50)
    print("START:", directory + "/" + module)
    print("=" * 50)
    print()

    subprocess.run([
        sys.executable,
        path
    ])


def menu(directory, title):
    while True:
        items = modules(directory)

        print()
        print("=" * 50)
        print(title)
        print("=" * 50)

        if not items:
            print("Geen modules.")
        else:
            for number, item in enumerate(items, 1):
                print(f"[{number}] {item}")

        print("[0] Terug")

        choice = input("\nKeuze > ").strip()

        if choice == "0":
            return

        try:
            number = int(choice)
            module = items[number - 1]
        except (ValueError, IndexError):
            print("Ongeldige keuze.")
            continue

        run(directory, module)


def main():
    while True:
        print()
        print("=" * 50)
        print("             FORENICOS")
        print("          ALPHA BETA ALPHA")
        print("=" * 50)
        print()

        for number, (name, _) in enumerate(SECTIONS, 1):
            print(f"[{number}] {name}")

        print("[0] EXIT")

        choice = input("\nForensicOS > ").strip()

        if choice == "0":
            print("ForensicOS afgesloten.")
            break

        try:
            number = int(choice)
            title, directory = SECTIONS[number - 1]
        except (ValueError, IndexError):
            print("Ongeldige keuze.")
            continue

        menu(directory, title)


if __name__ == "__main__":
    main()
PY

chmod +x core/main.py

echo "[12/12] Tests uitvoeren..."

python -m py_compile \
    core/*.py \
    cases/*.py \
    defense/*.py \
    rf/*.py \
    sweep/*.py \
    surveillance/*.py \
    system/*.py \
    terminal/*.py

echo
echo "=============================================="
echo "          INSTALLATIE VOLTOOID"
echo "=============================================="
echo
echo "Start:"
echo
echo "cd ~/ForensicOS"
echo "source .venv/bin/activate"
echo "python core/main.py"
echo
echo "GUI: NOG NIET GEÏNSTALLEERD"
echo "Backend: ACTIEF"
echo

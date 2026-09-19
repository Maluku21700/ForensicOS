#!/bin/bash

set -e

echo "========================================"
echo "        FORENICOS BACKEND BUILD"
echo "        Alpha Beta Alpha"
echo "========================================"

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
    tests \
    logs

touch \
    forensic/__init__.py \
    osint/__init__.py \
    rf/__init__.py \
    sweep/__init__.py \
    surveillance/__init__.py \
    defense/__init__.py \
    terminal/__init__.py \
    system/__init__.py \
    cases/__init__.py

# -------------------------------------------------
# CASE MANAGER
# -------------------------------------------------

cat > cases/manager.py <<'PY'
#!/usr/bin/env python3

import json
import os
from datetime import datetime

BASE = os.path.expanduser("~/ForensicOS/cases")


def create_case(name):
    safe = "".join(
        c for c in name
        if c.isalnum() or c in "-_"
    )

    if not safe:
        raise ValueError("Ongeldige case naam.")

    path = os.path.join(BASE, safe)
    os.makedirs(path, exist_ok=True)

    data = {
        "case": safe,
        "created": datetime.now().isoformat(),
        "findings": [],
        "evidence": [],
        "notes": []
    }

    with open(os.path.join(path, "case.json"), "w") as f:
        json.dump(data, f, indent=2)

    return path


def add_note(case, note):
    path = os.path.join(BASE, case, "case.json")

    if not os.path.isfile(path):
        raise FileNotFoundError("Case bestaat niet.")

    with open(path) as f:
        data = json.load(f)

    data["notes"].append({
        "time": datetime.now().isoformat(),
        "note": note
    })

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def list_cases():
    if not os.path.isdir(BASE):
        return []

    return sorted(
        x for x in os.listdir(BASE)
        if os.path.isdir(os.path.join(BASE, x))
    )


def main():
    print("================================")
    print("       FORENICOS CASE MANAGER")
    print("================================")

    print()
    print("[1] Nieuwe case")
    print("[2] Cases bekijken")
    print("[3] Notitie toevoegen")

    choice = input("\nKeuze: ").strip()

    if choice == "1":
        name = input("Case naam: ").strip()
        try:
            path = create_case(name)
            print("Case aangemaakt:", path)
        except ValueError as e:
            print("FOUT:", e)

    elif choice == "2":
        cases = list_cases()

        if not cases:
            print("Geen cases.")
        else:
            for case in cases:
                print("-", case)

    elif choice == "3":
        case = input("Case: ").strip()
        note = input("Notitie: ").strip()

        try:
            add_note(case, note)
            print("Notitie opgeslagen.")
        except FileNotFoundError as e:
            print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

# -------------------------------------------------
# SYSTEM INFO
# -------------------------------------------------

cat > system/info.py <<'PY'
#!/usr/bin/env python3

import os
import platform
import shutil
import subprocess


def command(cmd):
    try:
        return subprocess.check_output(
            cmd,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "Onbekend"


def main():
    print("================================")
    print("       FORENICOS SYSTEM")
    print("================================")

    print("Hostname :", platform.node())
    print("OS       :", platform.platform())
    print("Kernel   :", platform.release())
    print("Arch     :", platform.machine())
    print("Python   :", platform.python_version())
    print("CPU      :", platform.processor())
    print("CPU cores:", os.cpu_count())

    mem = shutil.disk_usage("/")
    print()
    print("Root storage:")
    print("Total    :", round(mem.total / 1024**3, 2), "GB")
    print("Used     :", round(mem.used / 1024**3, 2), "GB")
    print("Free     :", round(mem.free / 1024**3, 2), "GB")

    print()
    print("Uptime:")
    print(command(["uptime", "-p"]))

    print()
    print("Temperature:")

    temp = "/sys/class/thermal/thermal_zone0/temp"

    try:
        with open(temp) as f:
            value = int(f.read()) / 1000

        print(f"{value:.1f} °C")
    except Exception:
        print("Niet beschikbaar")


if __name__ == "__main__":
    main()
PY

# -------------------------------------------------
# NETWORK SWEEP
# -------------------------------------------------

cat > sweep/network.py <<'PY'
#!/usr/bin/env python3

import socket
import subprocess


def run(cmd):
    try:
        return subprocess.check_output(
            cmd,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "Niet beschikbaar"


def main():
    print("================================")
    print("       FORENICOS SWEEP")
    print("================================")

    hostname = socket.gethostname()

    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "Onbekend"

    print("Hostname :", hostname)
    print("IP       :", local_ip)

    print()
    print("Interfaces:")
    print(run(["ip", "-brief", "addr"]))

    print()
    print("Routes:")
    print(run(["ip", "route"]))

    print()
    print("DNS:")
    print(run(["cat", "/etc/resolv.conf"]))


if __name__ == "__main__":
    main()
PY

# -------------------------------------------------
# CONNECTION MONITOR
# -------------------------------------------------

cat > surveillance/connections.py <<'PY'
#!/usr/bin/env python3

import subprocess


def main():
    print("================================")
    print("    FORENICOS CONNECTION MONITOR")
    print("================================")
    print()

    try:
        result = subprocess.run(
            ["ss", "-tunap"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as error:
        print("FOUT:", error)


if __name__ == "__main__":
    main()
PY

# -------------------------------------------------
# LISTENING PORTS
# -------------------------------------------------

cat > surveillance/listening.py <<'PY'
#!/usr/bin/env python3

import subprocess


def main():
    print("================================")
    print("     FORENICOS LISTENING PORTS")
    print("================================")
    print()

    try:
        result = subprocess.run(
            ["ss", "-lntup"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as error:
        print("FOUT:", error)


if __name__ == "__main__":
    main()
PY

# -------------------------------------------------
# PROCESS INSPECTOR
# -------------------------------------------------

cat > defense/processes.py <<'PY'
#!/usr/bin/env python3

import subprocess


def main():
    print("================================")
    print("      FORENICOS PROCESS SCAN")
    print("================================")
    print()

    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True
    )

    print(result.stdout)


if __name__ == "__main__":
    main()
PY

# -------------------------------------------------
# PERSISTENCE CHECK
# -------------------------------------------------

cat > defense/persistence.py <<'PY'
#!/usr/bin/env python3

import os
import subprocess


def show(title, path):
    print()
    print("--------------------------------")
    print(title)
    print("--------------------------------")

    if os.path.exists(path):
        if os.path.isdir(path):
            print(subprocess.run(
                ["ls", "-la", path],
                capture_output=True,
                text=True
            ).stdout)
        else:
            print(path)
    else:
        print("Niet aanwezig.")


def main():
    print("================================")
    print("     FORENICOS PERSISTENCE SCAN")
    print("================================")

    show(
        "SYSTEMD SERVICES",
        "/etc/systemd/system"
    )

    show(
        "SYSTEMD USER SERVICES",
        os.path.expanduser("~/.config/systemd/user")
    )

    show(
        "CRON",
        "/etc/cron.d"
    )

    show(
        "AUTOSTART",
        os.path.expanduser("~/.config/autostart")
    )

    print()
    print("Dit is een diagnostische scan.")
    print("Resultaten zijn niet automatisch malware.")


if __name__ == "__main__":
    main()
PY

# -------------------------------------------------
# RF DEVICE CHECK
# -------------------------------------------------

cat > rf/device.py <<'PY'
#!/usr/bin/env python3

import subprocess


def main():
    print("================================")
    print("        FORENICOS RF")
    print("================================")

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
        print("rtl_test ontbreekt.")
        print()
        print("Installeer met:")
        print("sudo apt install rtl-sdr")

    except subprocess.TimeoutExpired:
        print("RTL-SDR test timeout.")


if __name__ == "__main__":
    main()
PY

# -------------------------------------------------
# CENTRAL LAUNCHER
# -------------------------------------------------

cat > core/main.py <<'PY'
#!/usr/bin/env python3

import os
import subprocess
import sys


ROOT = os.path.expanduser("~/ForensicOS")


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


def find_modules(directory):
    path = os.path.join(ROOT, directory)

    if not os.path.isdir(path):
        return []

    return sorted(
        file[:-3]
        for file in os.listdir(path)
        if file.endswith(".py")
        and file != "__init__.py"
    )


def run_module(directory, module):
    script = os.path.join(
        ROOT,
        directory,
        module + ".py"
    )

    if not os.path.isfile(script):
        print("Module niet gevonden.")
        return

    print()
    print("START:", directory + "/" + module)
    print()

    subprocess.run(
        [sys.executable, script]
    )


def submenu(directory, title):
    while True:
        modules = find_modules(directory)

        print()
        print("================================")
        print("FORENICOS", title)
        print("================================")

        if not modules:
            print("Geen modules.")
        else:
            for index, module in enumerate(modules, 1):
                print(f"[{index}] {module}")

        print("[0] Terug")

        choice = input("\nKeuze: ").strip()

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            module = modules[index]
        except (ValueError, IndexError):
            print("Ongeldige keuze.")
            continue

        run_module(directory, module)


def main():
    while True:
        print()
        print("========================================")
        print("            FORENICOS")
        print("          ALPHA BETA ALPHA")
        print("========================================")
        print()
        print("[1] FORENSICS")
        print("[2] OSINT")
        print("[3] RF / RTL-SDR")
        print("[4] NETWORK SWEEP")
        print("[5] SURVEILLANCE")
        print("[6] DEFENSE / LAB")
        print("[7] TERMINAL")
        print("[8] SYSTEM")
        print("[9] CASE MANAGEMENT")
        print("[0] EXIT")

        choice = input("\nForensicOS > ").strip()

        if choice == "0":
            print("ForensicOS afgesloten.")
            return

        if choice in MODULES:
            title, directory = MODULES[choice]
            submenu(directory, title)
        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()
PY

chmod +x core/main.py

# -------------------------------------------------
# TEST
# -------------------------------------------------

echo
echo "========================================"
echo "        BACKEND BUILD COMPLETE"
echo "========================================"
echo
echo "Start ForensicOS met:"
echo
echo "python core/main.py"
echo
echo "Bestaande modules zijn NIET overschreven."
echo

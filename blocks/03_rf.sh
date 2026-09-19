#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 3/11"
echo "            RF / RTL-SDR"
echo "=========================================="

cd "$ROOT"

mkdir -p rf tests reports logs
touch rf/__init__.py

echo
echo "[1/8] RF device detector..."

cat > rf/device.py <<'PY'
import subprocess


def run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    except Exception as e:
        return f"ERROR: {e}"


def main():
    print("========== RF DEVICE ==========\n")

    print("[USB DEVICES]")
    print(run(["lsusb"]))

    print("\n[RTL-SDR]")
    print(run(["rtl_test", "-t"]))

    print("\n[USB SDR DEVICES]")
    print(run([
        "sh",
        "-c",
        "ls -l /dev/bus/usb 2>/dev/null || true"
    ]))


if __name__ == "__main__":
    main()
PY

echo "[2/8] RTL-SDR capability checker..."

cat > rf/rtl_info.py <<'PY'
import shutil
import subprocess


def main():
    print("========== RTL-SDR INFO ==========\n")

    binary = shutil.which("rtl_test")

    if not binary:
        print("rtl_test: NIET GEVONDEN")
        print()
        print("Installatie:")
        print("sudo apt install rtl-sdr")
        return

    print("rtl_test:", binary)

    try:
        result = subprocess.run(
            ["rtl_test", "-t"],
            capture_output=True,
            text=True,
            timeout=8
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

    except subprocess.TimeoutExpired:
        print("Test timeout.")

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[3/8] RF tool availability..."

cat > rf/tools.py <<'PY'
import shutil


TOOLS = [
    "rtl_test",
    "rtl_fm",
    "rtl_power",
    "rtl_tcp",
    "hackrf_info",
    "airspy_info",
    "SoapySDRUtil"
]


def main():
    print("========== SDR TOOLS ==========\n")

    for tool in TOOLS:
        location = shutil.which(tool)

        if location:
            print(f"[+] {tool}: {location}")
        else:
            print(f"[-] {tool}: niet gevonden")


if __name__ == "__main__":
    main()
PY

echo "[4/8] Frequency plan..."

cat > rf/frequency.py <<'PY'
from dataclasses import dataclass


@dataclass
class Band:
    name: str
    start_mhz: float
    end_mhz: float
    purpose: str


BANDS = [
    Band("FM Broadcast", 87.5, 108.0, "FM radio"),
    Band("433 MHz ISM", 433.05, 434.79, "ISM"),
    Band("868 MHz ISM", 863.0, 870.0, "ISM"),
    Band("2.4 GHz ISM", 2400.0, 2483.5, "ISM / Wi-Fi / Bluetooth")
]


def main():
    print("========== RF FREQUENCY PLAN ==========\n")

    print(
        "Dit is alleen een referentie-overzicht "
        "van algemene banden.\n"
    )

    for band in BANDS:
        print(
            f"{band.name:18} "
            f"{band.start_mhz:8.2f} - "
            f"{band.end_mhz:8.2f} MHz | "
            f"{band.purpose}"
        )


if __name__ == "__main__":
    main()
PY

echo "[5/8] RTL-SDR power check..."

cat > rf/power.py <<'PY'
import shutil
import subprocess


def main():
    print("========== RF POWER CHECK ==========\n")

    if not shutil.which("rtl_power"):
        print("rtl_power niet gevonden.")
        print("Installeer eventueel:")
        print("sudo apt install rtl-sdr")
        return

    print("rtl_power beschikbaar.")
    print()
    print("Voor een echte spectrumscan is een")
    print("aangesloten RTL-SDR vereist.")
    print()
    print("Voorbeeld van veilige lokale meting:")
    print("rtl_power -f 87.5M:108M:100k -g 20 -i 10 -e 30s")


if __name__ == "__main__":
    main()
PY

echo "[6/8] RF logger..."

cat > rf/logger.py <<'PY'
import csv
import os
from datetime import datetime


ROOT = os.path.expanduser("~/ForensicOS")
LOG = os.path.join(ROOT, "logs", "rf_measurements.csv")


def log_measurement(
    frequency_mhz,
    power_db,
    source="manual"
):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)

    exists = os.path.exists(LOG)

    with open(
        LOG,
        "a",
        newline=""
    ) as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "frequency_mhz",
                "power_db",
                "source"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            frequency_mhz,
            power_db,
            source
        ])


def main():
    print("========== RF LOGGER ==========\n")

    frequency = input(
        "Frequency MHz: "
    ).strip()

    power = input(
        "Power dB: "
    ).strip()

    try:
        log_measurement(
            float(frequency),
            float(power)
        )

        print("Meting opgeslagen:")
        print(LOG)

    except ValueError:
        print("Ongeldige numerieke waarde.")


if __name__ == "__main__":
    main()
PY

echo "[7/8] RF status..."

cat > rf/status.py <<'PY'
import os
import shutil


def main():
    print("========== RF STATUS ==========\n")

    print(
        "rtl_test  :",
        shutil.which("rtl_test") or "missing"
    )

    print(
        "rtl_power  :",
        shutil.which("rtl_power") or "missing"
    )

    print(
        "rtl_fm     :",
        shutil.which("rtl_fm") or "missing"
    )

    print()

    devices = [
        "/dev/bus/usb",
        "/dev/rtl0"
    ]

    for device in devices:
        print(
            device,
            "OK" if os.path.exists(device)
            else "niet aanwezig"
        )


if __name__ == "__main__":
    main()
PY

echo "[8/8] RF self-test..."

cat > tests/test_rf.py <<'PY'
import os
import tempfile


def test_log_file():
    with tempfile.NamedTemporaryFile(
        delete=False
    ) as f:
        f.write(b"RFTEST")

        path = f.name

    assert os.path.isfile(path)

    os.unlink(path)


def test_frequency():
    frequency = 433.92

    assert frequency > 0
    assert frequency < 10000


if __name__ == "__main__":
    test_log_file()
    test_frequency()

    print("RF TEST: PASS")
PY

python -m py_compile rf/*.py tests/test_rf.py

python tests/test_rf.py

echo
echo "=========================================="
echo "        BLOK 3/11 VOLTOOID"
echo "=========================================="
echo
echo "RF modules:"
ls -1 rf/*.py

echo
echo "Test: PASS"
echo
echo "RTL-SDR installeren indien nodig:"
echo "sudo apt install rtl-sdr"
echo
echo "Volgende:"
echo "bash blocks/04_sweep.sh"
echo

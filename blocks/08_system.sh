#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 8/11"
echo "              SYSTEM"
echo "=========================================="

cd "$ROOT"

mkdir -p system tests logs
touch system/__init__.py

echo
echo "[1/6] Hardware information..."

cat > system/hardware.py <<'PY'
import platform
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
    print("========== HARDWARE ==========\n")

    print("Architecture:")
    print(platform.machine())

    print("\nCPU:")
    print(run(["lscpu"]))

    print("\nMemory:")
    print(run(["free", "-h"]))


if __name__ == "__main__":
    main()
PY

echo "[2/6] Storage information..."

cat > system/storage.py <<'PY'
import subprocess


def main():
    print("========== STORAGE ==========\n")

    try:
        result = subprocess.run(
            ["lsblk", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)

    print("\nFilesystem usage:\n")

    try:
        result = subprocess.run(
            ["df", "-h"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[3/6] Memory information..."

cat > system/memory.py <<'PY'
import subprocess


def main():
    print("========== MEMORY ==========\n")

    try:
        result = subprocess.run(
            ["free", "-h"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[4/6] Temperature monitor..."

cat > system/temperature.py <<'PY'
import os
import glob


def read_thermal_zones():
    results = []

    paths = glob.glob(
        "/sys/class/thermal/thermal_zone*/temp"
    )

    for path in sorted(paths):
        try:
            with open(path) as f:
                value = int(f.read().strip())

            results.append(
                (path, value / 1000.0)
            )

        except (ValueError, PermissionError, FileNotFoundError):
            continue

    return results


def main():
    print("========== TEMPERATURE ==========\n")

    results = read_thermal_zones()

    if not results:
        print("Geen thermal zones gevonden.")
        return

    for path, temperature in results:
        zone = os.path.basename(
            os.path.dirname(path)
        )

        print(
            f"{zone}: "
            f"{temperature:.1f} °C"
        )


if __name__ == "__main__":
    main()
PY

echo "[5/6] Uptime and load..."

cat > system/status.py <<'PY'
import os
import platform


def main():
    print("========== SYSTEM STATUS ==========\n")

    print("Hostname:")
    print(platform.node())

    print("\nKernel:")
    print(platform.release())

    print("\nArchitecture:")
    print(platform.machine())

    print("\nCPU cores:")
    print(os.cpu_count())

    print("\nLoad average:")

    try:
        load = os.getloadavg()

        print(
            f"1 min : {load[0]:.2f}"
        )
        print(
            f"5 min : {load[1]:.2f}"
        )
        print(
            f"15 min: {load[2]:.2f}"
        )

    except OSError:
        print("Niet beschikbaar.")

    print("\nUptime:")

    try:
        with open("/proc/uptime") as f:
            seconds = float(
                f.read().split()[0]
            )

        hours = seconds / 3600

        print(f"{hours:.2f} uur")

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[6/6] System summary..."

cat > system/summary.py <<'PY'
import os
import platform
import shutil


def main():
    print("==========================================")
    print("        FORENICOS SYSTEM SUMMARY")
    print("==========================================\n")

    print("Hostname :", platform.node())
    print("OS       :", platform.system())
    print("Kernel   :", platform.release())
    print("Arch     :", platform.machine())
    print("CPU cores:", os.cpu_count())

    total, used, free = shutil.disk_usage("/")

    print("\nRoot filesystem:")
    print(f"Total: {total / 1024**3:.2f} GB")
    print(f"Used : {used / 1024**3:.2f} GB")
    print(f"Free : {free / 1024**3:.2f} GB")

    print("\nMemory:")

    try:
        with open("/proc/meminfo") as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith(
                ("MemTotal:", "MemAvailable:")
            ):
                print(line.strip())

    except Exception as e:
        print("FOUT:", e)

    print("\n==========================================")


if __name__ == "__main__":
    main()
PY

echo
echo "[TEST] Compiling system modules..."

python -m py_compile system/*.py

cat > tests/test_system.py <<'PY'
import os
import platform


def test_platform():
    assert platform.system()


def test_hostname():
    assert platform.node()


def test_cpu():
    assert os.cpu_count() is not None
    assert os.cpu_count() > 0


def test_proc():
    assert os.path.exists("/proc")


def test_memory():
    assert os.path.exists("/proc/meminfo")


def test_disk():
    assert os.path.exists("/")


if __name__ == "__main__":
    test_platform()
    test_hostname()
    test_cpu()
    test_proc()
    test_memory()
    test_disk()

    print("SYSTEM TEST: PASS")
PY

echo "[TEST] Running system test..."

python tests/test_system.py

echo
echo "=========================================="
echo "       BLOK 8/11 VOLTOOID"
echo "=========================================="

echo
echo "Modules:"
ls -1 system/*.py

echo
echo "Test: PASS"

echo
echo "Volgende:"
echo "bash blocks/09_cases.sh"

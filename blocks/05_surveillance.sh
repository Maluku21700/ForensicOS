#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 5/11"
echo "       SURVEILLANCE / DETECTION"
echo "=========================================="

cd "$ROOT"

mkdir -p surveillance tests reports logs
touch surveillance/__init__.py

echo
echo "[1/7] Process inventory..."

cat > surveillance/processes.py <<'PY'
import subprocess


def main():
    print("========== RUNNING PROCESSES ==========\n")

    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[2/7] Network connections..."

cat > surveillance/connections.py <<'PY'
import subprocess


def main():
    print("========== ACTIVE CONNECTIONS ==========\n")

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

echo "[3/7] Listening services..."

cat > surveillance/listening.py <<'PY'
import subprocess


def main():
    print("========== LISTENING SERVICES ==========\n")

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

echo "[4/7] USB inventory..."

cat > surveillance/usb.py <<'PY'
import subprocess


def main():
    print("========== USB DEVICES ==========\n")

    try:
        result = subprocess.run(
            ["lsusb"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except FileNotFoundError:
        print("lsusb niet beschikbaar.")
        print("Installeer eventueel: sudo apt install usbutils")

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[5/7] System services..."

cat > surveillance/services.py <<'PY'
import subprocess


def main():
    print("========== SYSTEM SERVICES ==========\n")

    try:
        result = subprocess.run(
            ["systemctl", "--no-pager", "--type=service", "--state=running"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[6/7] Login/session inventory..."

cat > surveillance/sessions.py <<'PY'
import subprocess


def run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return result.stdout

    except Exception as e:
        return f"FOUT: {e}"


def main():
    print("========== LOGIN / SESSION STATUS ==========\n")

    print("Current user:")
    print(run(["whoami"]))

    print("Logged-in users:")
    print(run(["who"]))

    print("Current sessions:")
    print(run(["loginctl", "list-sessions", "--no-legend"]))


if __name__ == "__main__":
    main()
PY

echo "[7/7] Surveillance summary..."

cat > surveillance/summary.py <<'PY'
import socket
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
    print("==========================================")
    print("       FORENICOS SURVEILLANCE")
    print("==========================================\n")

    print("Hostname:")
    print(socket.gethostname())

    print("\nCurrent user:")
    print(run(["whoami"]))

    print("\nRunning processes:")
    processes = run(["ps", "-e", "--no-headers"])
    print("Process count:", len(processes.splitlines()))

    print("\nActive network sockets:")
    sockets = run(["ss", "-tun"])
    print("Socket lines:", len(sockets.splitlines()))

    print("\nListening TCP/UDP:")
    print(run(["ss", "-lntu"]))

    print("\nRunning services:")
    services = run([
        "systemctl",
        "--no-pager",
        "--type=service",
        "--state=running"
    ])

    print("Service lines:", len(services.splitlines()))

    print("\n==========================================")


if __name__ == "__main__":
    main()
PY

echo
echo "[TEST] Compiling surveillance modules..."

python -m py_compile surveillance/*.py

echo "[TEST] Running surveillance test..."

cat > tests/test_surveillance.py <<'PY'
import socket
import subprocess


def test_hostname():
    assert socket.gethostname()


def test_processes():
    result = subprocess.run(
        ["ps", "-e"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert result.stdout


def test_sockets():
    result = subprocess.run(
        ["ss", "-tun"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0


if __name__ == "__main__":
    test_hostname()
    test_processes()
    test_sockets()

    print("SURVEILLANCE TEST: PASS")
PY

python tests/test_surveillance.py

echo
echo "=========================================="
echo "       BLOK 5/11 VOLTOOID"
echo "=========================================="

echo
echo "Modules:"
ls -1 surveillance/*.py

echo
echo "Test: PASS"

echo
echo "Volgende:"
echo "bash blocks/06_defense.sh"

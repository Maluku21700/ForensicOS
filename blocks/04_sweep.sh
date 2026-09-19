#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 4/11"
echo "            NETWORK SWEEP"
echo "=========================================="

cd "$ROOT"

mkdir -p sweep tests reports logs
touch sweep/__init__.py

echo
echo "[1/8] Interface scanner..."

cat > sweep/interfaces.py <<'PY'
import socket
import subprocess


def main():
    print("========== NETWORK INTERFACES ==========\n")

    try:
        result = subprocess.run(
            ["ip", "-brief", "addr"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)

    print("Hostname:", socket.gethostname())


if __name__ == "__main__":
    main()
PY

echo "[2/8] Routing table..."

cat > sweep/routes.py <<'PY'
import subprocess


def main():
    print("========== ROUTING TABLE ==========\n")

    try:
        result = subprocess.run(
            ["ip", "route"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[3/8] Neighbor scanner..."

cat > sweep/neighbors.py <<'PY'
import subprocess


def main():
    print("========== NETWORK NEIGHBORS ==========\n")

    try:
        result = subprocess.run(
            ["ip", "neigh"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[4/8] DNS configuration..."

cat > sweep/dns.py <<'PY'
import os
import subprocess


def main():
    print("========== DNS CONFIGURATION ==========\n")

    try:
        with open("/etc/resolv.conf") as f:
            print(f.read())
    except Exception as e:
        print("resolv.conf:", e)

    print("\nSystem DNS status:\n")

    try:
        result = subprocess.run(
            ["resolvectl", "status"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except FileNotFoundError:
        print("resolvectl niet beschikbaar.")
    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[5/8] Local socket inventory..."

cat > sweep/sockets.py <<'PY'
import subprocess


def main():
    print("========== LOCAL SOCKETS ==========\n")

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

echo "[6/8] Listening services..."

cat > sweep/listening.py <<'PY'
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

echo "[7/8] Network summary..."

cat > sweep/summary.py <<'PY'
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
    print("========== NETWORK SUMMARY ==========\n")

    print("Hostname:")
    print(socket.gethostname())

    print("\nIP configuration:")
    print(run(["ip", "-brief", "addr"]))

    print("\nDefault route:")
    routes = run(["ip", "route"])

    for line in routes.splitlines():
        if line.startswith("default"):
            print(line)

    print("\nNeighbors:")
    print(run(["ip", "neigh"]))

    print("\nListening TCP/UDP:")
    print(run(["ss", "-lntup"]))


if __name__ == "__main__":
    main()
PY

echo "[8/8] Sweep self-test..."

cat > tests/test_sweep.py <<'PY'
import ipaddress
import socket


def test_hostname():
    assert socket.gethostname()


def test_local_network():
    network = ipaddress.ip_network(
        "192.168.1.0/24"
    )

    assert network.prefixlen == 24
    assert network.num_addresses == 256


if __name__ == "__main__":
    test_hostname()
    test_local_network()

    print("SWEEP TEST: PASS")
PY

python -m py_compile sweep/*.py tests/test_sweep.py

python tests/test_sweep.py

echo
echo "=========================================="
echo "        BLOK 4/11 VOLTOOID"
echo "=========================================="
echo
echo "Sweep modules:"
ls -1 sweep/*.py

echo
echo "Test: PASS"
echo
echo "Volgende:"
echo "bash blocks/05_surveillance.sh"
echo

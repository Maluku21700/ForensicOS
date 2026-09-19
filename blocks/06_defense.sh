#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 6/11"
echo "          DEFENSE / LAB"
echo "=========================================="

cd "$ROOT"

mkdir -p defense tests reports logs
touch defense/__init__.py

echo
echo "[1/7] Firewall audit..."

cat > defense/firewall.py <<'PY'
import shutil
import subprocess


def main():
    print("========== FIREWALL STATUS ==========\n")

    if shutil.which("ufw"):
        result = subprocess.run(
            ["ufw", "status", "verbose"],
            capture_output=True,
            text=True
        )
        print(result.stdout or result.stderr)

    elif shutil.which("nft"):
        result = subprocess.run(
            ["nft", "list", "ruleset"],
            capture_output=True,
            text=True
        )
        print(result.stdout or result.stderr)

    else:
        print("Geen UFW of nftables gevonden.")


if __name__ == "__main__":
    main()
PY

echo "[2/7] Port audit..."

cat > defense/ports.py <<'PY'
import subprocess


def main():
    print("========== LISTENING PORT AUDIT ==========\n")

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

echo "[3/7] SUID audit..."

cat > defense/suid.py <<'PY'
import os


def main():
    print("========== SUID FILE AUDIT ==========\n")

    roots = ["/usr/bin", "/usr/sbin", "/bin", "/sbin"]
    found = []

    for root in roots:
        if not os.path.isdir(root):
            continue

        for current_root, dirs, files in os.walk(root):
            for name in files:
                path = os.path.join(current_root, name)

                try:
                    mode = os.stat(path).st_mode

                    if mode & 0o4000:
                        found.append(path)

                except (PermissionError, FileNotFoundError):
                    continue

    for path in sorted(set(found)):
        print(path)

    print("\nAantal SUID-bestanden:", len(set(found)))


if __name__ == "__main__":
    main()
PY

echo "[4/7] Cron audit..."

cat > defense/cron.py <<'PY'
import os
import subprocess


def main():
    print("========== CRON AUDIT ==========\n")

    paths = [
        "/etc/crontab",
        "/etc/cron.d",
        "/etc/cron.daily",
        "/etc/cron.hourly",
        "/etc/cron.weekly",
        "/etc/cron.monthly",
    ]

    for path in paths:
        print(f"\n--- {path} ---")

        if os.path.isfile(path):
            try:
                with open(path, errors="replace") as f:
                    print(f.read())
            except PermissionError:
                print("Permission denied")

        elif os.path.isdir(path):
            try:
                for item in sorted(os.listdir(path)):
                    print(item)
            except PermissionError:
                print("Permission denied")

    print("\n--- Current user crontab ---")

    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )

        print(result.stdout or "(geen crontab)")
    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[5/7] Systemd timer audit..."

cat > defense/timers.py <<'PY'
import subprocess


def main():
    print("========== SYSTEMD TIMERS ==========\n")

    try:
        result = subprocess.run(
            [
                "systemctl",
                "list-timers",
                "--all",
                "--no-pager"
            ],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[6/7] File integrity audit..."

cat > defense/integrity.py <<'PY'
import hashlib
import os


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def audit_directory(directory):
    results = []

    if not os.path.isdir(directory):
        return results

    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)

            try:
                results.append({
                    "path": path,
                    "size": os.path.getsize(path),
                    "sha256": sha256(path)
                })
            except (PermissionError, FileNotFoundError):
                continue

    return results


def main():
    print("========== FILE INTEGRITY AUDIT ==========\n")

    directory = input(
        "Directory om te controleren [~/ForensicOS]: "
    ).strip()

    if not directory:
        directory = os.path.expanduser("~/ForensicOS")
    else:
        directory = os.path.expanduser(directory)

    results = audit_directory(directory)

    for item in results:
        print(
            f"{item['sha256']}  "
            f"{item['size']:>10}  "
            f"{item['path']}"
        )

    print("\nBestanden:", len(results))


if __name__ == "__main__":
    main()
PY

echo "[7/7] Security summary..."

cat > defense/summary.py <<'PY'
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
    print("        FORENICOS DEFENSE SUMMARY")
    print("==========================================\n")

    print("Hostname:")
    print(socket.gethostname())

    print("\nKernel:")
    print(run(["uname", "-a"]))

    print("\nListening ports:")
    print(run(["ss", "-lntup"]))

    print("\nSystemd timers:")
    timers = run([
        "systemctl",
        "list-timers",
        "--all",
        "--no-pager"
    ])
    print(timers)

    print("\nFirewall:")

    ufw = run(["ufw", "status"])

    if "command not found" not in ufw.lower():
        print(ufw)
    else:
        print("UFW niet beschikbaar.")

    print("\n==========================================")


if __name__ == "__main__":
    main()
PY

echo
echo "[TEST] Compiling defense modules..."

python -m py_compile defense/*.py

echo "[TEST] Running defense test..."

cat > tests/test_defense.py <<'PY'
import os
import socket
import subprocess


def test_hostname():
    assert socket.gethostname()


def test_proc():
    assert os.path.exists("/proc")


def test_ss():
    result = subprocess.run(
        ["ss", "-lnt"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0


def test_hash():
    import hashlib

    data = b"ForensicOS"

    result = hashlib.sha256(data).hexdigest()

    assert len(result) == 64


if __name__ == "__main__":
    test_hostname()
    test_proc()
    test_ss()
    test_hash()

    print("DEFENSE TEST: PASS")
PY

python tests/test_defense.py

echo
echo "=========================================="
echo "       BLOK 6/11 VOLTOOID"
echo "=========================================="

echo
echo "Modules:"
ls -1 defense/*.py

echo
echo "Test: PASS"

echo
echo "Volgende:"
echo "bash blocks/07_terminal.sh"

#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 11/11"
echo "       COMPLETE INTEGRATION TEST"
echo "=========================================="

cd "$ROOT"

mkdir -p tests logs reports

echo
echo "[1/6] Python compilation..."

python -m py_compile \
    core/*.py \
    forensic/*.py \
    osint/*.py \
    rf/*.py \
    sweep/*.py \
    surveillance/*.py \
    defense/*.py \
    terminal/*.py \
    system/*.py \
    cases/*.py

echo "Compilation: PASS"

echo
echo "[2/6] Core tests..."

PYTHONPATH="$ROOT" python tests/test_core.py

echo
echo "[3/6] Module tests..."

PYTHONPATH="$ROOT" python tests/test_forensics.py
PYTHONPATH="$ROOT" python tests/test_osint.py
PYTHONPATH="$ROOT" python tests/test_rf.py
PYTHONPATH="$ROOT" python tests/test_sweep.py
PYTHONPATH="$ROOT" python tests/test_surveillance.py
PYTHONPATH="$ROOT" python tests/test_defense.py
PYTHONPATH="$ROOT" python tests/test_terminal.py
PYTHONPATH="$ROOT" python tests/test_system.py
PYTHONPATH="$ROOT" python tests/test_cases.py

echo
echo "[4/6] Import test..."

PYTHONPATH="$ROOT" python - <<'PY'
import importlib

packages = [
    "core",
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

for package in packages:
    importlib.import_module(package)
    print(f"{package}: PASS")

print("IMPORT TEST: PASS")
PY

echo
echo "[5/6] Configuration test..."

PYTHONPATH="$ROOT" python - <<'PY'
import json
import os

root = os.path.expanduser("~/ForensicOS")

path = os.path.join(
    root,
    "config",
    "config.json"
)

with open(path, encoding="utf-8") as f:
    config = json.load(f)

assert config["name"] == "ForensicOS"
assert config["codename"] == "Alpha Beta Alpha"
assert config["version"]

print("Configuration: PASS")
print("Version:", config["version"])
PY

echo
echo "[6/6] Project structure..."

required_dirs=(
    core
    forensic
    osint
    rf
    sweep
    surveillance
    defense
    terminal
    system
    cases
    config
    reports
    logs
    tests
    blocks
)

for directory in "${required_dirs[@]}"; do
    if [ -d "$ROOT/$directory" ]; then
        echo "$directory: PASS"
    else
        echo "$directory: FAIL"
        exit 1
    fi
done

echo
echo "=========================================="
echo "       FORENICOS BACKEND: READY"
echo "=========================================="

echo
echo "Project:"
echo "$ROOT"

echo
echo "Python:"
python --version

echo
echo "Architecture:"
uname -m

echo
echo "Backend blocks:"
ls -1 blocks/*.sh

echo
echo "=========================================="
echo "        ALL TESTS: PASS"
echo "=========================================="

echo
echo "Backend fase afgerond."
echo
echo "Start launcher:"
echo "  python core/main.py"
echo
echo "GUI kan nu als volgende fase gebouwd worden."

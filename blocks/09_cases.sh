#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 9/11"
echo "          CASE MANAGEMENT"
echo "=========================================="

cd "$ROOT"

mkdir -p cases tests reports logs

echo
echo "[1/5] Case database..."

cat > cases/manager.py <<'PY'
import json
import os
import uuid
from datetime import datetime, timezone


ROOT = os.path.expanduser("~/ForensicOS")
CASES_DIR = os.path.join(ROOT, "cases")


def now():
    return datetime.now(timezone.utc).isoformat()


def case_path(case_id):
    return os.path.join(CASES_DIR, case_id)


def create_case(name, description=""):
    case_id = (
        datetime.now().strftime("%Y%m%d_%H%M%S")
        + "_"
        + uuid.uuid4().hex[:6]
    )

    directory = case_path(case_id)

    os.makedirs(
        os.path.join(directory, "evidence"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(directory, "reports"),
        exist_ok=True
    )

    data = {
        "case_id": case_id,
        "name": name,
        "description": description,
        "created": now(),
        "updated": now(),
        "evidence": [],
    }

    with open(
        os.path.join(directory, "case.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    return data


def load_case(case_id):
    path = os.path.join(
        case_path(case_id),
        "case.json"
    )

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_case(data):
    path = os.path.join(
        case_path(data["case_id"]),
        "case.json"
    )

    data["updated"] = now()

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def add_evidence(case_id, path, sha256=None):
    data = load_case(case_id)

    evidence = {
        "id": uuid.uuid4().hex,
        "path": os.path.abspath(
            os.path.expanduser(path)
        ),
        "sha256": sha256,
        "added": now(),
    }

    data["evidence"].append(evidence)

    save_case(data)

    return evidence


def list_cases():
    if not os.path.isdir(CASES_DIR):
        return []

    result = []

    for name in sorted(os.listdir(CASES_DIR)):
        directory = case_path(name)
        case_file = os.path.join(
            directory,
            "case.json"
        )

        if os.path.isfile(case_file):
            try:
                result.append(
                    load_case(name)
                )
            except Exception:
                continue

    return result


if __name__ == "__main__":
    case = create_case(
        "Demo Case",
        "ForensicOS test case"
    )

    print("Created case:")
    print(case["case_id"])
PY

echo "[2/5] Evidence hashing..."

cat > cases/evidence.py <<'PY'
import hashlib
import os


def sha256_file(path):
    path = os.path.expanduser(path)

    digest = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            digest.update(chunk)

    return digest.hexdigest()


def collect_file(path):
    path = os.path.abspath(
        os.path.expanduser(path)
    )

    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    stat = os.stat(path)

    return {
        "path": path,
        "filename": os.path.basename(path),
        "size": stat.st_size,
        "sha256": sha256_file(path),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(
            "Gebruik: python -m cases.evidence FILE"
        )
        raise SystemExit(1)

    print(
        collect_file(sys.argv[1])
    )
PY

echo "[3/5] Case reporting..."

cat > cases/report.py <<'PY'
import json
import os
from datetime import datetime, timezone

from .manager import load_case


def generate_report(case_id):
    data = load_case(case_id)

    report = {
        "generated": datetime.now(
            timezone.utc
        ).isoformat(),
        "case": data,
    }

    directory = os.path.join(
        os.path.expanduser("~/ForensicOS/cases"),
        case_id,
        "reports"
    )

    os.makedirs(
        directory,
        exist_ok=True
    )

    path = os.path.join(
        directory,
        "case_report.json"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False
        )

    return path


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(
            "Gebruik: python -m cases.report CASE_ID"
        )
        raise SystemExit(1)

    print(
        generate_report(sys.argv[1])
    )
PY

echo "[4/5] Case CLI..."

cat > cases/cli.py <<'PY'
from .manager import (
    create_case,
    list_cases,
    load_case,
)


def main():
    print("==========================================")
    print("       FORENICOS CASE MANAGER")
    print("==========================================")

    while True:
        print("""
[1] Nieuwe case
[2] Cases bekijken
[3] Case details
[0] Exit
""")

        choice = input("ForensicOS Cases > ").strip()

        if choice == "1":
            name = input("Case naam: ").strip()
            description = input(
                "Beschrijving: "
            ).strip()

            if not name:
                print("Case naam ontbreekt.")
                continue

            case = create_case(
                name,
                description
            )

            print(
                "\nCase aangemaakt:",
                case["case_id"]
            )

        elif choice == "2":
            cases = list_cases()

            if not cases:
                print("\nGeen cases.")
                continue

            print()

            for case in cases:
                print(
                    case["case_id"],
                    "|",
                    case["name"]
                )

        elif choice == "3":
            case_id = input(
                "Case ID: "
            ).strip()

            try:
                case = load_case(case_id)

                print("\nCase:")
                print(
                    "ID:",
                    case["case_id"]
                )
                print(
                    "Naam:",
                    case["name"]
                )
                print(
                    "Beschrijving:",
                    case["description"]
                )
                print(
                    "Evidence:",
                    len(case["evidence"])
                )

            except FileNotFoundError:
                print("Case niet gevonden.")

        elif choice == "0":
            break

        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()
PY

echo "[5/5] Case tests..."

cat > tests/test_cases.py <<'PY'
import os
import tempfile

from cases.manager import (
    create_case,
    load_case,
    add_evidence,
)
from cases.evidence import (
    sha256_file,
    collect_file,
)


def test_hashing():
    with tempfile.NamedTemporaryFile(
        mode="wb",
        delete=False
    ) as f:
        f.write(b"ForensicOS test")
        path = f.name

    try:
        digest = sha256_file(path)

        assert len(digest) == 64

        evidence = collect_file(path)

        assert evidence["size"] == 15
        assert evidence["sha256"] == digest

    finally:
        os.unlink(path)


def test_case_creation():
    case = create_case(
        "Test Case",
        "Automated test"
    )

    case_id = case["case_id"]

    try:
        loaded = load_case(case_id)

        assert loaded["name"] == "Test Case"
        assert loaded["description"] == "Automated test"
        assert loaded["evidence"] == []

        evidence = add_evidence(
            case_id,
            "/tmp/example.bin",
            "abc123"
        )

        loaded = load_case(case_id)

        assert len(
            loaded["evidence"]
        ) == 1

        assert (
            loaded["evidence"][0]["sha256"]
            == "abc123"
        )

    finally:
        import shutil

        shutil.rmtree(
            os.path.join(
                os.path.expanduser(
                    "~/ForensicOS/cases"
                ),
                case_id
            ),
            ignore_errors=True
        )


if __name__ == "__main__":
    test_hashing()
    test_case_creation()

    print("CASE TEST: PASS")
PY

echo
echo "[TEST] Compiling case modules..."

python -m py_compile cases/*.py tests/test_cases.py

echo "[TEST] Running case test..."

PYTHONPATH="$ROOT" python tests/test_cases.py

echo
echo "=========================================="
echo "       BLOK 9/11 VOLTOOID"
echo "=========================================="

echo
echo "Modules:"
ls -1 cases/*.py

echo
echo "Test: PASS"

echo
echo "Volgende:"
echo "bash blocks/10_core.sh"

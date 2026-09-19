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

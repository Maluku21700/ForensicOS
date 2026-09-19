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

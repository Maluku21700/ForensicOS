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

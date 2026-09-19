import json
import os
import sys


ROOT = os.path.expanduser("~/ForensicOS")

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def test_config():
    path = os.path.join(
        ROOT,
        "config",
        "config.json"
    )

    assert os.path.exists(path)

    with open(
        path,
        encoding="utf-8"
    ) as f:
        config = json.load(f)

    assert config["name"] == "ForensicOS"
    assert config["codename"] == "Alpha Beta Alpha"
    assert "modules" in config


def test_main_import():
    import core.main

    assert core.main.MODULES


def test_directories():
    required = [
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

    for directory in required:
        assert os.path.isdir(
            os.path.join(
                ROOT,
                directory
            )
        )


if __name__ == "__main__":
    test_config()
    test_main_import()
    test_directories()

    print("CORE TEST: PASS")

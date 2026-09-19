import json
import os


ROOT = os.path.expanduser("~/ForensicOS")


def load_config():
    path = os.path.join(
        ROOT,
        "config",
        "config.json"
    )

    with open(
        path,
        encoding="utf-8"
    ) as f:
        return json.load(f)


def clear_screen():
    os.system("clear")


def pause():
    input("\nDruk ENTER om door te gaan...")


def module_files(directory):
    path = os.path.join(ROOT, directory)

    if not os.path.isdir(path):
        return []

    return sorted(
        name[:-3]
        for name in os.listdir(path)
        if name.endswith(".py")
        and name != "__init__.py"
        and not name.startswith("_")
    )

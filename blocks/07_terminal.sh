#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 7/11"
echo "             TERMINAL"
echo "=========================================="

cd "$ROOT"

mkdir -p terminal tests logs
touch terminal/__init__.py

echo
echo "[1/5] Command runner..."

cat > terminal/runner.py <<'PY'
import subprocess


def run(command):
    """
    Run a command without invoking a shell.
    Accepts either a list or a whitespace-separated string.
    """

    if isinstance(command, str):
        command = command.split()

    if not command:
        return {
            "returncode": 0,
            "stdout": "",
            "stderr": ""
        }

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except FileNotFoundError:
        return {
            "returncode": 127,
            "stdout": "",
            "stderr": f"Command not found: {command[0]}"
        }

    except Exception as e:
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": str(e)
        }


def main():
    command = input("Command: ").strip()

    result = run(command)

    if result["stdout"]:
        print(result["stdout"], end="")

    if result["stderr"]:
        print(result["stderr"], end="")

    print("\nExit code:", result["returncode"])


if __name__ == "__main__":
    main()
PY

echo "[2/5] System terminal..."

cat > terminal/system.py <<'PY'
import os
import platform
import shutil


def main():
    print("========== SYSTEM TERMINAL ==========\n")

    print("OS:", platform.system())
    print("Release:", platform.release())
    print("Machine:", platform.machine())
    print("Python:", platform.python_version())
    print("Hostname:", platform.node())
    print("User:", os.environ.get("USER", "unknown"))

    print("\nDisk:")
    total, used, free = shutil.disk_usage("/")

    print(f"Total: {total / (1024**3):.2f} GB")
    print(f"Used : {used / (1024**3):.2f} GB")
    print(f"Free : {free / (1024**3):.2f} GB")


if __name__ == "__main__":
    main()
PY

echo "[3/5] Network terminal..."

cat > terminal/network.py <<'PY'
import subprocess


def run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr)

    except Exception as e:
        print("FOUT:", e)


def main():
    print("========== NETWORK TERMINAL ==========\n")

    print("[1] Interfaces")
    print("[2] Routes")
    print("[3] Neighbors")
    print("[4] Listening ports")
    print("[5] DNS")

    choice = input("\nKeuze: ").strip()

    commands = {
        "1": ["ip", "-brief", "addr"],
        "2": ["ip", "route"],
        "3": ["ip", "neigh"],
        "4": ["ss", "-lntup"],
        "5": ["cat", "/etc/resolv.conf"],
    }

    command = commands.get(choice)

    if command:
        run(command)
    else:
        print("Ongeldige keuze.")


if __name__ == "__main__":
    main()
PY

echo "[4/5] Interactive shell..."

cat > terminal/shell.py <<'PY'
import os
import shlex
import subprocess


BUILTINS = {
    "help",
    "pwd",
    "ls",
    "cd",
    "clear",
    "whoami",
    "exit",
    "quit",
}


def show_help():
    print("""
ForensicOS Terminal

Built-in:
  help       Help
  pwd        Current directory
  ls         List files
  cd PATH    Change directory
  clear      Clear screen
  whoami     Current user
  exit       Exit terminal

Andere normale Linux-commando's kunnen ook
worden uitgevoerd.
""")


def execute(command):
    if not command:
        return True

    try:
        parts = shlex.split(command)
    except ValueError as e:
        print("Parse error:", e)
        return True

    if not parts:
        return True

    cmd = parts[0]

    if cmd in ("exit", "quit"):
        return False

    if cmd == "help":
        show_help()
        return True

    if cmd == "pwd":
        print(os.getcwd())
        return True

    if cmd == "ls":
        target = parts[1] if len(parts) > 1 else "."
        try:
            for item in os.listdir(os.path.expanduser(target)):
                print(item)
        except Exception as e:
            print("FOUT:", e)
        return True

    if cmd == "cd":
        target = parts[1] if len(parts) > 1 else os.path.expanduser("~")

        try:
            os.chdir(os.path.expanduser(target))
        except Exception as e:
            print("FOUT:", e)

        return True

    if cmd == "clear":
        os.system("clear")
        return True

    if cmd == "whoami":
        subprocess.run(["whoami"])
        return True

    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True
        )

        if result.stdout:
            print(result.stdout, end="")

        if result.stderr:
            print(result.stderr, end="")

    except FileNotFoundError:
        print("Command niet gevonden:", cmd)

    except Exception as e:
        print("FOUT:", e)

    return True


def main():
    print("""
==========================================
          FORENICOS TERMINAL
==========================================
Typ 'help' voor beschikbare commando's.
Typ 'exit' om te stoppen.
""")

    while True:
        try:
            prompt = f"ForensicOS:{os.getcwd()}$ "
            command = input(prompt)

            if not execute(command):
                break

        except KeyboardInterrupt:
            print("\nGebruik 'exit' om te stoppen.")

        except EOFError:
            print()
            break


if __name__ == "__main__":
    main()
PY

echo "[5/5] Terminal tests..."

cat > tests/test_terminal.py <<'PY'
import os

from terminal.runner import run
from terminal.shell import execute


def test_runner():
    result = run(["echo", "ForensicOS"])

    assert result["returncode"] == 0
    assert "ForensicOS" in result["stdout"]


def test_runner_failure():
    result = run(["command_that_should_not_exist_12345"])

    assert result["returncode"] != 0


def test_pwd():
    original = os.getcwd()

    assert execute("pwd") is True

    os.chdir(original)


def test_help():
    assert execute("help") is True


def test_exit():
    assert execute("exit") is False


if __name__ == "__main__":
    test_runner()
    test_runner_failure()
    test_pwd()
    test_help()
    test_exit()

    print("TERMINAL TEST: PASS")
PY

echo
echo "[TEST] Compiling terminal modules..."

python -m py_compile terminal/*.py tests/test_terminal.py

echo "[TEST] Running terminal test..."

python tests/test_terminal.py

echo
echo "=========================================="
echo "       BLOK 7/11 VOLTOOID"
echo "=========================================="

echo
echo "Modules:"
ls -1 terminal/*.py

echo
echo "Test: PASS"

echo
echo "Volgende:"
echo "bash blocks/08_system.sh"

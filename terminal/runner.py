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

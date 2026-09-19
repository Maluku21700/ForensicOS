import subprocess


def run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return result.stdout

    except Exception as e:
        return f"FOUT: {e}"


def main():
    print("========== LOGIN / SESSION STATUS ==========\n")

    print("Current user:")
    print(run(["whoami"]))

    print("Logged-in users:")
    print(run(["who"]))

    print("Current sessions:")
    print(run(["loginctl", "list-sessions", "--no-legend"]))


if __name__ == "__main__":
    main()

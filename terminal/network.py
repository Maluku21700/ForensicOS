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

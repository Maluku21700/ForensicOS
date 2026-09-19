import socket
import subprocess


def run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"


def main():
    print("==========================================")
    print("        FORENICOS DEFENSE SUMMARY")
    print("==========================================\n")

    print("Hostname:")
    print(socket.gethostname())

    print("\nKernel:")
    print(run(["uname", "-a"]))

    print("\nListening ports:")
    print(run(["ss", "-lntup"]))

    print("\nSystemd timers:")
    timers = run([
        "systemctl",
        "list-timers",
        "--all",
        "--no-pager"
    ])
    print(timers)

    print("\nFirewall:")

    ufw = run(["ufw", "status"])

    if "command not found" not in ufw.lower():
        print(ufw)
    else:
        print("UFW niet beschikbaar.")

    print("\n==========================================")


if __name__ == "__main__":
    main()

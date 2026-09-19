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
    print("       FORENICOS SURVEILLANCE")
    print("==========================================\n")

    print("Hostname:")
    print(socket.gethostname())

    print("\nCurrent user:")
    print(run(["whoami"]))

    print("\nRunning processes:")
    processes = run(["ps", "-e", "--no-headers"])
    print("Process count:", len(processes.splitlines()))

    print("\nActive network sockets:")
    sockets = run(["ss", "-tun"])
    print("Socket lines:", len(sockets.splitlines()))

    print("\nListening TCP/UDP:")
    print(run(["ss", "-lntu"]))

    print("\nRunning services:")
    services = run([
        "systemctl",
        "--no-pager",
        "--type=service",
        "--state=running"
    ])

    print("Service lines:", len(services.splitlines()))

    print("\n==========================================")


if __name__ == "__main__":
    main()

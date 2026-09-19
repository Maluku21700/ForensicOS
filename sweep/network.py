import socket
import subprocess


def run(command):
    try:
        return subprocess.check_output(
            command,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "N/A"


def main():
    print("\n========== NETWORK SWEEP ==========\n")

    print("Hostname:")
    print(socket.gethostname())

    print("\nInterfaces:")
    print(run(["ip", "-brief", "addr"]))

    print("\nRoutes:")
    print(run(["ip", "route"]))

    print("\nARP/Neighbors:")
    print(run(["ip", "neigh"]))


if __name__ == "__main__":
    main()

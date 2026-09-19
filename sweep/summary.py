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
    print("========== NETWORK SUMMARY ==========\n")

    print("Hostname:")
    print(socket.gethostname())

    print("\nIP configuration:")
    print(run(["ip", "-brief", "addr"]))

    print("\nDefault route:")
    routes = run(["ip", "route"])

    for line in routes.splitlines():
        if line.startswith("default"):
            print(line)

    print("\nNeighbors:")
    print(run(["ip", "neigh"]))

    print("\nListening TCP/UDP:")
    print(run(["ss", "-lntup"]))


if __name__ == "__main__":
    main()

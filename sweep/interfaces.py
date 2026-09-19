import socket
import subprocess


def main():
    print("========== NETWORK INTERFACES ==========\n")

    try:
        result = subprocess.run(
            ["ip", "-brief", "addr"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)

    print("Hostname:", socket.gethostname())


if __name__ == "__main__":
    main()

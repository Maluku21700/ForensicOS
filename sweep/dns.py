import os
import subprocess


def main():
    print("========== DNS CONFIGURATION ==========\n")

    try:
        with open("/etc/resolv.conf") as f:
            print(f.read())
    except Exception as e:
        print("resolv.conf:", e)

    print("\nSystem DNS status:\n")

    try:
        result = subprocess.run(
            ["resolvectl", "status"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except FileNotFoundError:
        print("resolvectl niet beschikbaar.")
    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

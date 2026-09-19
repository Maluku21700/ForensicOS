import platform
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
    print("========== HARDWARE ==========\n")

    print("Architecture:")
    print(platform.machine())

    print("\nCPU:")
    print(run(["lscpu"]))

    print("\nMemory:")
    print(run(["free", "-h"]))


if __name__ == "__main__":
    main()

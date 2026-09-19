import os
import platform
import shutil


def main():
    print("========== SYSTEM TERMINAL ==========\n")

    print("OS:", platform.system())
    print("Release:", platform.release())
    print("Machine:", platform.machine())
    print("Python:", platform.python_version())
    print("Hostname:", platform.node())
    print("User:", os.environ.get("USER", "unknown"))

    print("\nDisk:")
    total, used, free = shutil.disk_usage("/")

    print(f"Total: {total / (1024**3):.2f} GB")
    print(f"Used : {used / (1024**3):.2f} GB")
    print(f"Free : {free / (1024**3):.2f} GB")


if __name__ == "__main__":
    main()

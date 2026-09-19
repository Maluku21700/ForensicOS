import os
import platform
import shutil


def main():
    print("==========================================")
    print("        FORENICOS SYSTEM SUMMARY")
    print("==========================================\n")

    print("Hostname :", platform.node())
    print("OS       :", platform.system())
    print("Kernel   :", platform.release())
    print("Arch     :", platform.machine())
    print("CPU cores:", os.cpu_count())

    total, used, free = shutil.disk_usage("/")

    print("\nRoot filesystem:")
    print(f"Total: {total / 1024**3:.2f} GB")
    print(f"Used : {used / 1024**3:.2f} GB")
    print(f"Free : {free / 1024**3:.2f} GB")

    print("\nMemory:")

    try:
        with open("/proc/meminfo") as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith(
                ("MemTotal:", "MemAvailable:")
            ):
                print(line.strip())

    except Exception as e:
        print("FOUT:", e)

    print("\n==========================================")


if __name__ == "__main__":
    main()

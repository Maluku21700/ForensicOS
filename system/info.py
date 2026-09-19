import os
import platform
import shutil
import subprocess


def cmd(command):
    try:
        return subprocess.check_output(
            command,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "N/A"


def main():
    print("\n========== SYSTEM INFO ==========\n")

    print("Hostname :", platform.node())
    print("OS       :", platform.platform())
    print("Kernel   :", platform.release())
    print("Arch     :", platform.machine())
    print("Python   :", platform.python_version())
    print("CPU      :", platform.processor())
    print("CPU cores:", os.cpu_count())

    ram = cmd(["free", "-h"])
    print("\nRAM:")
    print(ram)

    disk = shutil.disk_usage("/")
    print("\nDisk:")
    print(f"Total: {disk.total / 1024**3:.1f} GB")
    print(f"Used : {disk.used / 1024**3:.1f} GB")
    print(f"Free : {disk.free / 1024**3:.1f} GB")

    print("\nUptime:")
    print(cmd(["uptime", "-p"]))

    temp = "/sys/class/thermal/thermal_zone0/temp"

    if os.path.exists(temp):
        try:
            with open(temp) as f:
                value = int(f.read()) / 1000
            print(f"\nCPU temperature: {value:.1f} °C")
        except Exception:
            pass


if __name__ == "__main__":
    main()

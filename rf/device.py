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
    print("========== RF DEVICE ==========\n")

    print("[USB DEVICES]")
    print(run(["lsusb"]))

    print("\n[RTL-SDR]")
    print(run(["rtl_test", "-t"]))

    print("\n[USB SDR DEVICES]")
    print(run([
        "sh",
        "-c",
        "ls -l /dev/bus/usb 2>/dev/null || true"
    ]))


if __name__ == "__main__":
    main()

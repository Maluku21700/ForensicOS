import os
import shutil


def main():
    print("========== RF STATUS ==========\n")

    print(
        "rtl_test  :",
        shutil.which("rtl_test") or "missing"
    )

    print(
        "rtl_power  :",
        shutil.which("rtl_power") or "missing"
    )

    print(
        "rtl_fm     :",
        shutil.which("rtl_fm") or "missing"
    )

    print()

    devices = [
        "/dev/bus/usb",
        "/dev/rtl0"
    ]

    for device in devices:
        print(
            device,
            "OK" if os.path.exists(device)
            else "niet aanwezig"
        )


if __name__ == "__main__":
    main()

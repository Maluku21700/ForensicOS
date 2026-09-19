import subprocess


def main():
    print("========== USB DEVICES ==========\n")

    try:
        result = subprocess.run(
            ["lsusb"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except FileNotFoundError:
        print("lsusb niet beschikbaar.")
        print("Installeer eventueel: sudo apt install usbutils")

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

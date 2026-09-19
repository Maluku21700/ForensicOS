import subprocess


def main():
    print("\n========== RF USB DEVICES ==========\n")

    try:
        print(
            subprocess.check_output(
                ["lsusb"],
                text=True
            )
        )
    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

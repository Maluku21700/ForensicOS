import subprocess


def main():
    print("========== STORAGE ==========\n")

    try:
        result = subprocess.run(
            ["lsblk", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)

    print("\nFilesystem usage:\n")

    try:
        result = subprocess.run(
            ["df", "-h"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

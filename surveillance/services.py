import subprocess


def main():
    print("========== SYSTEM SERVICES ==========\n")

    try:
        result = subprocess.run(
            ["systemctl", "--no-pager", "--type=service", "--state=running"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

import subprocess


def main():
    print("\n========== SERVICE ANALYZER ==========\n")

    try:
        result = subprocess.run(
            ["systemctl", "--type=service", "--no-pager"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

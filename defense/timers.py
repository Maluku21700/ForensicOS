import subprocess


def main():
    print("========== SYSTEMD TIMERS ==========\n")

    try:
        result = subprocess.run(
            [
                "systemctl",
                "list-timers",
                "--all",
                "--no-pager"
            ],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

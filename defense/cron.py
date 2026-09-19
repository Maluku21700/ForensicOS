import os
import subprocess


def main():
    print("========== CRON AUDIT ==========\n")

    paths = [
        "/etc/crontab",
        "/etc/cron.d",
        "/etc/cron.daily",
        "/etc/cron.hourly",
        "/etc/cron.weekly",
        "/etc/cron.monthly",
    ]

    for path in paths:
        print(f"\n--- {path} ---")

        if os.path.isfile(path):
            try:
                with open(path, errors="replace") as f:
                    print(f.read())
            except PermissionError:
                print("Permission denied")

        elif os.path.isdir(path):
            try:
                for item in sorted(os.listdir(path)):
                    print(item)
            except PermissionError:
                print("Permission denied")

    print("\n--- Current user crontab ---")

    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )

        print(result.stdout or "(geen crontab)")
    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

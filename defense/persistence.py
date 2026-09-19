import os
import subprocess


PATHS = [
    "/etc/systemd/system",
    "/etc/cron.d",
    "/etc/cron.daily",
    "/etc/cron.hourly",
    "/etc/cron.monthly",
    "/etc/cron.weekly",
    os.path.expanduser("~/.config/systemd/user"),
    os.path.expanduser("~/.config/autostart")
]


def main():
    print("\n========== PERSISTENCE SCANNER ==========\n")

    for path in PATHS:
        print(f"\n--- {path} ---")

        if not os.path.exists(path):
            print("Niet aanwezig.")
            continue

        if os.path.isdir(path):
            try:
                print(
                    subprocess.check_output(
                        ["ls", "-la", path],
                        text=True
                    )
                )
            except Exception as e:
                print("FOUT:", e)
        else:
            print(path)

    print("\nDit is een diagnostische scan.")
    print("Een gevonden entry is niet automatisch malware.")


if __name__ == "__main__":
    main()

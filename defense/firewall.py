import shutil
import subprocess


def main():
    print("========== FIREWALL STATUS ==========\n")

    if shutil.which("ufw"):
        result = subprocess.run(
            ["ufw", "status", "verbose"],
            capture_output=True,
            text=True
        )
        print(result.stdout or result.stderr)

    elif shutil.which("nft"):
        result = subprocess.run(
            ["nft", "list", "ruleset"],
            capture_output=True,
            text=True
        )
        print(result.stdout or result.stderr)

    else:
        print("Geen UFW of nftables gevonden.")


if __name__ == "__main__":
    main()

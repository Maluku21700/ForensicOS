import subprocess
import sys


def query(name, record="TXT"):
    try:
        result = subprocess.run(
            ["dig", "+short", name, record],
            capture_output=True,
            text=True,
            timeout=5
        )

        return result.stdout.strip() or "-"

    except Exception:
        return "-"


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/email_domain.py <domain>")
        return

    domain = sys.argv[1]

    print("========== EMAIL DOMAIN ==========")
    print("Domain:", domain)

    print("\nMX:")
    print(query(domain, "MX"))

    print("\nSPF:")
    print(query(domain, "TXT"))

    print("\nDMARC:")
    print(query("_dmarc." + domain, "TXT"))

    print("\nDKIM default:")
    print(query(
        "default._domainkey." + domain,
        "TXT"
    ))


if __name__ == "__main__":
    main()

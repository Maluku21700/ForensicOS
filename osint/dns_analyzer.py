import socket
import subprocess
import sys


def query(domain, record):
    try:
        result = subprocess.run(
            ["dig", "+short", domain, record],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() or "-"
    except FileNotFoundError:
        return "dig ontbreekt"
    except Exception:
        return "-"


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/dns_analyzer.py <domain>")
        return

    domain = sys.argv[1]

    print("========== DNS ANALYZER ==========")
    print("Domain:", domain)

    for record in ["A", "AAAA", "MX", "NS", "CNAME", "TXT"]:
        print(f"\n[{record}]")
        print(query(domain, record))

    print("\n[DMARC]")
    print(query("_dmarc." + domain, "TXT"))

    print("\n[Reverse DNS]")
    try:
        print(socket.gethostbyaddr(
            socket.gethostbyname(domain)
        )[0])
    except Exception:
        print("-")


if __name__ == "__main__":
    main()

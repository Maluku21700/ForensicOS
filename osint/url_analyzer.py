import socket
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/url_analyzer.py <url>")
        return

    target = sys.argv[1]

    if "://" not in target:
        target = "https://" + target

    parsed = urlparse(target)

    print("========== URL ANALYZER ==========")
    print("URL      :", target)
    print("Scheme   :", parsed.scheme)
    print("Hostname :", parsed.hostname)
    print("Port     :", parsed.port or "default")
    print("Path     :", parsed.path or "/")
    print("Query    :", parsed.query or "-")

    if not parsed.hostname:
        return

    try:
        print("IP       :", socket.gethostbyname(parsed.hostname))
    except Exception:
        print("IP       : onbekend")

    try:
        request = Request(
            target,
            headers={"User-Agent": "ForensicOS/0.1"}
        )

        with urlopen(request, timeout=10) as response:
            print("HTTP     :", response.status)
            print("Final URL:", response.geturl())
            print("Type     :", response.headers.get("Content-Type"))

    except Exception as e:
        print("HTTP     : niet beschikbaar")
        print("Info     :", e)


if __name__ == "__main__":
    main()

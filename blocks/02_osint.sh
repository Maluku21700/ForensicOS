#!/bin/bash

set -e

ROOT="$HOME/ForensicOS"

echo "=========================================="
echo "       FORENICOS — BLOK 2/11"
echo "              OSINT"
echo "=========================================="

cd "$ROOT"

mkdir -p osint tests reports
touch osint/__init__.py

echo "[1/10] URL analyzer..."

cat > osint/url_analyzer.py <<'PY'
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
PY

echo "[2/10] DNS analyzer..."

cat > osint/dns_analyzer.py <<'PY'
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
PY

echo "[3/10] IP analyzer..."

cat > osint/ip_analyzer.py <<'PY'
import ipaddress
import socket
import sys


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/ip_analyzer.py <ip>")
        return

    value = sys.argv[1]

    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        print("Ongeldig IP-adres.")
        return

    print("========== IP ANALYZER ==========")
    print("IP          :", ip)
    print("Version     :", ip.version)
    print("Private     :", ip.is_private)
    print("Global      :", ip.is_global)
    print("Loopback    :", ip.is_loopback)
    print("Link-local  :", ip.is_link_local)
    print("Multicast   :", ip.is_multicast)
    print("Reserved    :", ip.is_reserved)

    try:
        print("Reverse DNS :", socket.gethostbyaddr(value)[0])
    except Exception:
        print("Reverse DNS : -")


if __name__ == "__main__":
    main()
PY

echo "[4/10] HTTP headers..."

cat > osint/http_headers.py <<'PY'
import sys
from urllib.request import Request, urlopen


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/http_headers.py <url>")
        return

    url = sys.argv[1]

    if "://" not in url:
        url = "https://" + url

    try:
        request = Request(
            url,
            headers={"User-Agent": "ForensicOS/0.1"}
        )

        with urlopen(request, timeout=10) as response:
            print("========== HTTP HEADERS ==========")
            print("Status:", response.status)
            print("URL   :", response.geturl())
            print()

            for key, value in response.headers.items():
                print(f"{key}: {value}")

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[5/10] Robots / sitemap..."

cat > osint/robots_sitemap.py <<'PY'
import sys
from urllib.parse import urljoin
from urllib.request import Request, urlopen


def fetch(url):
    request = Request(
        url,
        headers={"User-Agent": "ForensicOS/0.1"}
    )

    with urlopen(request, timeout=10) as response:
        return response.read().decode(
            "utf-8",
            errors="ignore"
        )


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/robots_sitemap.py <url>")
        return

    base = sys.argv[1].rstrip("/") + "/"

    print("========== ROBOTS / SITEMAP ==========")

    robots_url = urljoin(base, "robots.txt")

    try:
        content = fetch(robots_url)

        print("\n--- robots.txt ---")
        print(content[:10000])

        print("\n--- sitemap entries ---")

        for line in content.splitlines():
            if line.lower().startswith("sitemap:"):
                print(line.strip())

    except Exception as e:
        print("robots.txt:", e)

    for filename in ["sitemap.xml", "sitemap_index.xml"]:
        try:
            content = fetch(urljoin(base, filename))

            print(f"\n--- {filename} ---")
            print(content[:10000])

        except Exception:
            pass


if __name__ == "__main__":
    main()
PY

echo "[6/10] Email domain analyzer..."

cat > osint/email_domain.py <<'PY'
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
PY

echo "[7/10] Web technology detector..."

cat > osint/web_tech.py <<'PY'
import re
import sys
from urllib.request import Request, urlopen


PATTERNS = {
    "WordPress": [r"wp-content", r"wp-includes"],
    "Drupal": [r"drupalSettings", r"/sites/default/"],
    "Joomla": [r"/media/system/", r"Joomla"],
    "React": [r"react", r"__REACT"],
    "Next.js": [r"__NEXT_DATA__", r"_next/"],
    "Vue": [r"vue"],
    "Angular": [r"ng-version"],
    "Bootstrap": [r"bootstrap"],
    "jQuery": [r"jquery"],
    "Google Analytics": [r"google-analytics"],
    "Google Tag Manager": [r"googletagmanager"],
    "Cloudflare": [r"cloudflare"]
}


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/web_tech.py <url>")
        return

    url = sys.argv[1]

    if "://" not in url:
        url = "https://" + url

    try:
        request = Request(
            url,
            headers={"User-Agent": "ForensicOS/0.1"}
        )

        with urlopen(request, timeout=10) as response:
            html = response.read(
                5 * 1024 * 1024
            ).decode(
                "utf-8",
                errors="ignore"
            )

            headers = response.headers

        print("========== WEB TECHNOLOGY ==========")

        found = set()

        for name, patterns in PATTERNS.items():
            for pattern in patterns:
                if re.search(
                    pattern,
                    html,
                    re.IGNORECASE
                ):
                    found.add(name)
                    break

        for item in sorted(found):
            print("[+]", item)

        print("\nServer:", headers.get("Server", "-"))
        print("X-Powered-By:",
              headers.get("X-Powered-By", "-"))

        title = re.search(
            r"<title[^>]*>(.*?)</title>",
            html,
            re.IGNORECASE | re.DOTALL
        )

        print(
            "Title:",
            title.group(1).strip()
            if title else "-"
        )

        print(
            "\nIndicatieve detectie; "
            "false positives zijn mogelijk."
        )

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()
PY

echo "[8/10] Public username reference search..."

cat > osint/username_search.py <<'PY'
import sys
from urllib.parse import quote


SITES = {
    "GitHub":
        "https://github.com/{}",
    "GitLab":
        "https://gitlab.com/{}",
    "Reddit":
        "https://www.reddit.com/user/{}",
    "X":
        "https://x.com/{}",
    "Instagram":
        "https://www.instagram.com/{}/",
    "Twitch":
        "https://www.twitch.tv/{}",
    "YouTube":
        "https://www.youtube.com/@{}"
}


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/username_search.py <username>")
        return

    username = sys.argv[1].strip()

    print("========== USERNAME SEARCH ==========")
    print("Username:", username)
    print()

    for site, template in SITES.items():
        print(f"{site}: {template.format(quote(username))}")

    query = quote(f'"{username}"')

    print()
    print("Search engines:")
    print("Google    : https://www.google.com/search?q=" + query)
    print("Bing      : https://www.bing.com/search?q=" + query)
    print("DuckDuckGo: https://duckduckgo.com/?q=" + query)

    print()
    print("Alleen publieke bronnen.")
    print("Geen account-enumeratie of privédata.")


if __name__ == "__main__":
    main()
PY

echo "[9/10] Metadata OSINT..."

cat > osint/metadata_osint.py <<'PY'
import hashlib
import mimetypes
import os
import re
import sys


KEYWORDS = [
    "gps",
    "latitude",
    "longitude",
    "location",
    "camera",
    "author",
    "producer",
    "software",
    "device",
    "model"
]


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python osint/metadata_osint.py <bestand>")
        return

    path = sys.argv[1]

    if not os.path.isfile(path):
        print("Bestand bestaat niet.")
        return

    print("========== METADATA OSINT ==========")
    print("Name :", os.path.basename(path))
    print("Size :", os.path.getsize(path))
    print("MIME :", mimetypes.guess_type(path)[0])
    print("SHA256:", sha256(path))

    with open(path, "rb") as f:
        data = f.read(2 * 1024 * 1024)

    strings = re.findall(
        rb"[\x20-\x7e]{5,}",
        data
    )

    print("\nPotential indicators:")

    count = 0

    for raw in strings:
        value = raw.decode(
            "ascii",
            errors="ignore"
        )

        if any(
            keyword in value.lower()
            for keyword in KEYWORDS
        ):
            print(value[:300])
            count += 1

            if count >= 30:
                break

    print(
        "\nStrings zijn alleen indicatoren; "
        "geen gegarandeerde metadata."
    )


if __name__ == "__main__":
    main()
PY

echo "[10/10] OSINT self-test..."

cat > tests/test_osint.py <<'PY'
import ipaddress
import os
import tempfile
from urllib.parse import urlparse


def test_url():
    parsed = urlparse(
        "https://example.com/test?a=1"
    )

    assert parsed.hostname == "example.com"
    assert parsed.path == "/test"


def test_ip():
    ip = ipaddress.ip_address("192.168.1.1")

    assert ip.is_private
    assert not ip.is_global


def test_file():
    with tempfile.NamedTemporaryFile(
        delete=False
    ) as f:
        f.write(b"ForensicOS")

        path = f.name

    assert os.path.getsize(path) == 10

    os.unlink(path)


if __name__ == "__main__":
    test_url()
    test_ip()
    test_file()

    print("OSINT TEST: PASS")
PY

python -m py_compile osint/*.py tests/test_osint.py

python tests/test_osint.py

echo
echo "=========================================="
echo "        BLOK 2/11 VOLTOOID"
echo "=========================================="
echo
echo "OSINT modules:"
ls -1 osint/*.py

echo
echo "Test: PASS"
echo
echo "Volgende:"
echo "bash blocks/03_rf.sh"
echo

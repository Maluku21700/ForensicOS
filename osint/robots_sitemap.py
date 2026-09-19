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

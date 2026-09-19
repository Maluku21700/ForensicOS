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

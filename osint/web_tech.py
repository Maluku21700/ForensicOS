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

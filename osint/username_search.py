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

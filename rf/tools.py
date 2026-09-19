import shutil


TOOLS = [
    "rtl_test",
    "rtl_fm",
    "rtl_power",
    "rtl_tcp",
    "hackrf_info",
    "airspy_info",
    "SoapySDRUtil"
]


def main():
    print("========== SDR TOOLS ==========\n")

    for tool in TOOLS:
        location = shutil.which(tool)

        if location:
            print(f"[+] {tool}: {location}")
        else:
            print(f"[-] {tool}: niet gevonden")


if __name__ == "__main__":
    main()

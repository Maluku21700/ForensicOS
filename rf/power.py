import shutil
import subprocess


def main():
    print("========== RF POWER CHECK ==========\n")

    if not shutil.which("rtl_power"):
        print("rtl_power niet gevonden.")
        print("Installeer eventueel:")
        print("sudo apt install rtl-sdr")
        return

    print("rtl_power beschikbaar.")
    print()
    print("Voor een echte spectrumscan is een")
    print("aangesloten RTL-SDR vereist.")
    print()
    print("Voorbeeld van veilige lokale meting:")
    print("rtl_power -f 87.5M:108M:100k -g 20 -i 10 -e 30s")


if __name__ == "__main__":
    main()

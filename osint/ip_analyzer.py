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

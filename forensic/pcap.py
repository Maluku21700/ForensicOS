#!/usr/bin/env python3

import os
import struct


PCAP_MAGIC = {
    b"\xd4\xc3\xb2\xa1": "<",
    b"\xa1\xb2\xc3\xd4": ">",
    b"\x4d\x3c\xb2\xa1": "<",
    b"\xa1\xb2\x3c\x4d": ">",
}


def analyze_pcap(filename):
    with open(filename, "rb") as file:
        data = file.read()

    if len(data) < 24:
        return {"format": "Ongeldig/te klein", "packets": 0}

    magic = data[:4]

    if magic not in PCAP_MAGIC:
        if magic == b"\x0a\x0d\x0d\x0a":
            return {
                "format": "PCAPNG",
                "packets": "Niet berekend door deze basisparser"
            }

        return {
            "format": "Onbekend",
            "packets": 0
        }

    endian = PCAP_MAGIC[magic]

    offset = 24
    packets = 0
    tcp = 0
    udp = 0
    ipv4 = 0

    while offset + 16 <= len(data):
        try:
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack_from(
                endian + "IIII",
                data,
                offset
            )
        except struct.error:
            break

        packet_start = offset + 16
        packet_end = packet_start + incl_len

        if packet_end > len(data):
            break

        packet = data[packet_start:packet_end]
        packets += 1

        # Ethernet + IPv4
        if len(packet) >= 34:
            ether_type = struct.unpack(">H", packet[12:14])[0]

            if ether_type == 0x0800:
                ipv4 += 1

                protocol = packet[23]

                if protocol == 6:
                    tcp += 1
                elif protocol == 17:
                    udp += 1

        offset = packet_end

    return {
        "format": "PCAP",
        "packets": packets,
        "ipv4": ipv4,
        "tcp": tcp,
        "udp": udp,
    }


def main():
    print("================================")
    print("        FORENICOS PCAP")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        result = analyze_pcap(filename)

        print()
        print("Bestand :", os.path.abspath(filename))
        print("Grootte :", os.path.getsize(filename), "bytes")
        print("Formaat :", result["format"])

        if result["format"] == "PCAP":
            print("Packets :", result["packets"])
            print("IPv4    :", result["ipv4"])
            print("TCP     :", result["tcp"])
            print("UDP     :", result["udp"])
        else:
            print("Packets : niet beschikbaar")

    except PermissionError:
        print()
        print("FOUT: geen toestemming.")

    print()
    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import struct
import ipaddress
from collections import Counter


PCAP_MAGIC = {
    b"\xd4\xc3\xb2\xa1": "<",
    b"\xa1\xb2\xc3\xd4": ">",
    b"\x4d\x3c\xb2\xa1": "<",
    b"\xa1\xb2\x3c\x4d": ">",
}


PROTOCOLS = {
    6: "TCP",
    17: "UDP",
    58: "ICMPv6",
    43: "Routing",
    44: "Fragment",
    51: "AH",
    50: "ESP",
}


def ipv6_address(data):
    return str(ipaddress.IPv6Address(data))


def analyze_pcap(filename):
    with open(filename, "rb") as file:
        data = file.read()

    if len(data) < 24:
        raise ValueError("PCAP is te klein.")

    magic = data[:4]

    if magic not in PCAP_MAGIC:
        raise ValueError("Geen klassieke PCAP gevonden.")

    endian = PCAP_MAGIC[magic]
    offset = 24

    addresses = Counter()
    protocols = Counter()
    conversations = Counter()

    while offset + 16 <= len(data):

        try:
            _, _, incl_len, _ = struct.unpack_from(
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

        # Ethernet
        if len(packet) >= 14:

            ether_type = struct.unpack(">H", packet[12:14])[0]

            # IPv6
            if ether_type == 0x86DD and len(packet) >= 54:

                ip_start = 14

                version = packet[ip_start] >> 4

                if version == 6:

                    next_header = packet[ip_start + 6]

                    src_ip = ipv6_address(
                        packet[
                            ip_start + 8:
                            ip_start + 24
                        ]
                    )

                    dst_ip = ipv6_address(
                        packet[
                            ip_start + 24:
                            ip_start + 40
                        ]
                    )

                    protocol_name = PROTOCOLS.get(
                        next_header,
                        str(next_header)
                    )

                    addresses[src_ip] += 1
                    addresses[dst_ip] += 1

                    protocols[protocol_name] += 1

                    conversations[
                        (
                            src_ip,
                            dst_ip,
                            protocol_name
                        )
                    ] += 1

        offset = packet_end

    return addresses, protocols, conversations


def main():
    print("================================")
    print("      FORENICOS IPv6 STATS")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        addresses, protocols, conversations = analyze_pcap(
            filename
        )

        print()
        print("IPv6 PROTOCOLLEN")
        print("--------------------------------")

        if protocols:
            for protocol, count in protocols.most_common():
                print(f"{protocol:<15} {count}")
        else:
            print("Geen IPv6-verkeer gevonden.")

        print()
        print("IPv6 VERBINDINGEN")
        print("--------------------------------")

        for (
            src,
            dst,
            protocol
        ), count in conversations.most_common():

            print(
                f"{src} -> {dst} | "
                f"{protocol} : {count}"
            )

        print()
        print("IPv6 ADRESSEN")
        print("--------------------------------")

        for ip, count in addresses.most_common():
            print(f"{ip:<45} {count}")

        print()
        print("================================")
        print("IPv6 pakketten:", sum(protocols.values()))
        print("IPv6 adressen :", len(addresses))
        print("================================")

    except PermissionError:
        print()
        print("FOUT: geen toestemming.")

    except ValueError as error:
        print()
        print("FOUT:", error)

    print()
    input("Druk ENTER om af te sluiten...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import struct
from collections import Counter


PCAP_MAGIC = {
    b"\xd4\xc3\xb2\xa1": "<",
    b"\xa1\xb2\xc3\xd4": ">",
    b"\x4d\x3c\xb2\xa1": "<",
    b"\xa1\xb2\x3c\x4d": ">",
}


PROTOCOLS = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    41: "IPv6",
    47: "GRE",
    50: "ESP",
    51: "AH",
    58: "ICMPv6",
}


def ip_address(data):
    return ".".join(str(x) for x in data)


def analyze(filename):
    with open(filename, "rb") as file:
        data = file.read()

    if len(data) < 24:
        raise ValueError("PCAP is te klein.")

    magic = data[:4]

    if magic not in PCAP_MAGIC:
        raise ValueError("Geen klassieke PCAP gevonden.")

    endian = PCAP_MAGIC[magic]

    offset = 24

    packets = 0
    total_bytes = 0

    protocols = Counter()
    source_ips = Counter()
    destination_ips = Counter()
    ether_types = Counter()

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

        packets += 1
        total_bytes += len(packet)

        if len(packet) >= 14:

            ether_type = struct.unpack(
                ">H",
                packet[12:14]
            )[0]

            ether_types[ether_type] += 1

            # IPv4
            if ether_type == 0x0800 and len(packet) >= 34:

                ip_start = 14

                source = ip_address(
                    packet[ip_start + 12:
                           ip_start + 16]
                )

                destination = ip_address(
                    packet[ip_start + 16:
                           ip_start + 20]
                )

                protocol = packet[ip_start + 9]

                source_ips[source] += 1
                destination_ips[destination] += 1

                protocols[
                    PROTOCOLS.get(
                        protocol,
                        f"Protocol {protocol}"
                    )
                ] += 1

            # IPv6
            elif ether_type == 0x86DD and len(packet) >= 54:

                ip_start = 14

                if packet[ip_start] >> 4 == 6:

                    protocol = packet[ip_start + 6]

                    protocols[
                        PROTOCOLS.get(
                            protocol,
                            f"Next Header {protocol}"
                        )
                    ] += 1

        offset = packet_end

    return (
        packets,
        total_bytes,
        protocols,
        source_ips,
        destination_ips,
        ether_types,
    )


def main():
    print("================================")
    print("      FORENICOS PCAP REPORT")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        (
            packets,
            total_bytes,
            protocols,
            source_ips,
            destination_ips,
            ether_types,
        ) = analyze(filename)

        print()
        print("ALGEMEEN")
        print("--------------------------------")
        print("Bestand       :", os.path.abspath(filename))
        print("PCAP grootte  :", os.path.getsize(filename), "bytes")
        print("Pakketten     :", packets)
        print("Packet bytes  :", total_bytes)

        print()
        print("PROTOCOLLEN")
        print("--------------------------------")

        for protocol, count in protocols.most_common():
            print(f"{protocol:<20} {count}")

        print()
        print("TOP SOURCE IP'S")
        print("--------------------------------")

        for ip, count in source_ips.most_common(15):
            print(f"{ip:<18} {count}")

        print()
        print("TOP DESTINATION IP'S")
        print("--------------------------------")

        for ip, count in destination_ips.most_common(15):
            print(f"{ip:<18} {count}")

        print()
        print("ETHERNET TYPES")
        print("--------------------------------")

        for ether_type, count in ether_types.most_common():
            print(f"0x{ether_type:04x} : {count}")

        print()
        print("================================")
        print("       ANALYSE KLAAR")
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

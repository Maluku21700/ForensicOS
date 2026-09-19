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


ICMP_TYPES = {
    0: "Echo Reply",
    3: "Destination Unreachable",
    5: "Redirect",
    8: "Echo Request",
    11: "Time Exceeded",
    12: "Parameter Problem",
    13: "Timestamp Request",
    14: "Timestamp Reply",
    17: "Address Mask Request",
    18: "Address Mask Reply",
}


def ip_address(data):
    return ".".join(str(x) for x in data)


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

    types = Counter()
    conversations = Counter()
    addresses = Counter()

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
        if len(packet) >= 34:

            ether_type = struct.unpack(">H", packet[12:14])[0]

            # IPv4
            if ether_type == 0x0800:

                ip_start = 14
                version_ihl = packet[ip_start]
                ihl = (version_ihl & 0x0F) * 4

                if len(packet) >= ip_start + ihl + 4:

                    protocol = packet[ip_start + 9]

                    # ICMP
                    if protocol == 1:

                        src_ip = ip_address(
                            packet[ip_start + 12:ip_start + 16]
                        )

                        dst_ip = ip_address(
                            packet[ip_start + 16:ip_start + 20]
                        )

                        icmp_start = ip_start + ihl

                        icmp_type = packet[icmp_start]
                        icmp_code = packet[icmp_start + 1]

                        type_name = ICMP_TYPES.get(
                            icmp_type,
                            f"Type {icmp_type}"
                        )

                        types[
                            (type_name, icmp_code)
                        ] += 1

                        addresses[src_ip] += 1
                        addresses[dst_ip] += 1

                        conversations[
                            (src_ip, dst_ip, type_name)
                        ] += 1

        offset = packet_end

    return types, conversations, addresses


def main():
    print("================================")
    print("      FORENICOS ICMP STATS")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        types, conversations, addresses = analyze_pcap(
            filename
        )

        print()
        print("ICMP TYPES")
        print("--------------------------------")

        if types:
            for (name, code), count in types.most_common():
                print(
                    f"{name:<25} "
                    f"code {code:<3} {count}"
                )
        else:
            print("Geen ICMP-verkeer gevonden.")

        print()
        print("ICMP VERBINDINGEN")
        print("--------------------------------")

        for (src, dst, type_name), count in conversations.most_common():
            print(
                f"{src} -> {dst} | "
                f"{type_name} : {count}"
            )

        print()
        print("IP-ADRESSEN")
        print("--------------------------------")

        for ip, count in addresses.most_common():
            print(f"{ip:<18} {count}")

        print()
        print("================================")
        print("ICMP pakketten:", sum(types.values()))
        print("IP-adressen   :", len(addresses))
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

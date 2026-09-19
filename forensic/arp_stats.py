#!/usr/bin/env python3

import os
import struct
from collections import Counter, defaultdict


PCAP_MAGIC = {
    b"\xd4\xc3\xb2\xa1": "<",
    b"\xa1\xb2\xc3\xd4": ">",
    b"\x4d\x3c\xb2\xa1": "<",
    b"\xa1\xb2\x3c\x4d": ">",
}


def ip_address(data):
    return ".".join(str(x) for x in data)


def mac_address(data):
    return ":".join(f"{x:02x}" for x in data)


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

    operations = Counter()
    ip_mac = defaultdict(set)
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

        # Ethernet + ARP
        if len(packet) >= 42:

            ether_type = struct.unpack(">H", packet[12:14])[0]

            if ether_type == 0x0806:

                arp = packet[14:]

                hardware_type = struct.unpack(
                    ">H", arp[0:2]
                )[0]

                protocol_type = struct.unpack(
                    ">H", arp[2:4]
                )[0]

                hardware_size = arp[4]
                protocol_size = arp[5]

                operation = struct.unpack(
                    ">H", arp[6:8]
                )[0]

                # Ethernet + IPv4 ARP
                if (
                    hardware_type == 1
                    and protocol_type == 0x0800
                    and hardware_size == 6
                    and protocol_size == 4
                ):

                    sender_mac = mac_address(arp[8:14])
                    sender_ip = ip_address(arp[14:18])

                    target_mac = mac_address(arp[18:24])
                    target_ip = ip_address(arp[24:28])

                    if operation == 1:
                        operation_name = "REQUEST"

                    elif operation == 2:
                        operation_name = "REPLY"

                    else:
                        operation_name = str(operation)

                    operations[operation_name] += 1

                    ip_mac[sender_ip].add(sender_mac)

                    conversations[
                        (
                            sender_ip,
                            sender_mac,
                            target_ip,
                            target_mac,
                            operation_name,
                        )
                    ] += 1

        offset = packet_end

    return operations, ip_mac, conversations


def main():
    print("================================")
    print("       FORENICOS ARP STATS")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        operations, ip_mac, conversations = analyze_pcap(filename)

        print()
        print("ARP OPERATIES")
        print("--------------------------------")

        for operation, count in operations.most_common():
            print(f"{operation:<10} {count}")

        print()
        print("IP -> MAC")
        print("--------------------------------")

        for ip, macs in sorted(ip_mac.items()):
            for mac in sorted(macs):
                print(f"{ip:<18} {mac}")

        print()
        print("ARP VERKEER")
        print("--------------------------------")

        for (
            src_ip,
            src_mac,
            dst_ip,
            dst_mac,
            operation,
        ), count in conversations.most_common():

            print(
                f"{operation:<7} "
                f"{src_ip} ({src_mac}) -> "
                f"{dst_ip} ({dst_mac}) : {count}"
            )

        print()
        print("================================")
        print("ARP operaties:", sum(operations.values()))
        print("IP-adressen :", len(ip_mac))
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

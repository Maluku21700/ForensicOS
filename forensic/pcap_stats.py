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


def ip_address(data):
    return ".".join(str(byte) for byte in data)


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

    ip_pairs = Counter()
    ports = Counter()
    protocols = Counter()

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

        # Ethernet frame
        if len(packet) >= 14:
            ether_type = struct.unpack(">H", packet[12:14])[0]

            # IPv4
            if ether_type == 0x0800 and len(packet) >= 34:
                ip_header_start = 14

                version_ihl = packet[ip_header_start]
                ihl = (version_ihl & 0x0F) * 4

                if len(packet) < ip_header_start + ihl:
                    offset = packet_end
                    continue

                protocol = packet[ip_header_start + 9]

                source_ip = ip_address(
                    packet[ip_header_start + 12:
                          ip_header_start + 16]
                )

                destination_ip = ip_address(
                    packet[ip_header_start + 16:
                          ip_header_start + 20]
                )

                if protocol == 6:
                    protocol_name = "TCP"

                elif protocol == 17:
                    protocol_name = "UDP"

                else:
                    protocol_name = str(protocol)

                protocols[protocol_name] += 1

                ip_pairs[
                    (source_ip, destination_ip, protocol_name)
                ] += 1

                # TCP / UDP ports
                transport_start = ip_header_start + ihl

                if protocol in (6, 17):
                    if len(packet) >= transport_start + 4:
                        source_port, destination_port = struct.unpack(
                            ">HH",
                            packet[
                                transport_start:
                                transport_start + 4
                            ]
                        )

                        ports[
                            (
                                source_ip,
                                source_port,
                                destination_ip,
                                destination_port,
                                protocol_name
                            )
                        ] += 1

        offset = packet_end

    return ip_pairs, ports, protocols


def main():
    print("================================")
    print("    FORENICOS PCAP STATISTICS")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        ip_pairs, ports, protocols = analyze_pcap(filename)

        print()
        print("PROTOCOLLEN")
        print("--------------------------------")

        for protocol, count in protocols.most_common():
            print(f"{protocol:<8} {count}")

        print()
        print("IP-VERBINDINGEN")
        print("--------------------------------")

        for (src, dst, protocol), count in ip_pairs.most_common():
            print(f"{src} -> {dst} [{protocol}] : {count}")

        print()
        print("POORTEN")
        print("--------------------------------")

        for (
            src,
            src_port,
            dst,
            dst_port,
            protocol
        ), count in ports.most_common():

            print(
                f"{src}:{src_port} -> "
                f"{dst}:{dst_port} "
                f"[{protocol}] : {count}"
            )

        print()
        print("================================")
        print("Totaal IP-verbindingen:", len(ip_pairs))
        print("Totaal poortcombinaties:", len(ports))
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

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


QUERY_TYPES = {
    1: "A",
    2: "NS",
    5: "CNAME",
    6: "SOA",
    12: "PTR",
    15: "MX",
    16: "TXT",
    28: "AAAA",
    33: "SRV",
}


def ip_address(data):
    return ".".join(str(byte) for byte in data)


def read_dns_name(data, offset):
    labels = []
    original_offset = offset
    jumped = False
    visited = set()

    while offset < len(data):
        if offset in visited:
            return None, original_offset + 2

        visited.add(offset)

        length = data[offset]

        if length == 0:
            offset += 1
            break

        # DNS compression pointer
        if (length & 0xC0) == 0xC0:
            if offset + 1 >= len(data):
                return None, offset + 2

            pointer = ((length & 0x3F) << 8) | data[offset + 1]

            if pointer >= len(data):
                return None, offset + 2

            if not jumped:
                original_offset = offset + 2
                jumped = True

            offset = pointer
            continue

        if length > 63 or offset + 1 + length > len(data):
            return None, offset + 1

        label = data[offset + 1:offset + 1 + length]

        try:
            labels.append(label.decode("ascii"))
        except UnicodeDecodeError:
            labels.append("<non-ascii>")

        offset += 1 + length

    return ".".join(labels), original_offset if jumped else offset


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

    domains = Counter()
    query_types = Counter()
    dns_servers = Counter()
    queries = []

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

        # Ethernet + IPv4 + UDP
        if len(packet) >= 42:

            ether_type = struct.unpack(">H", packet[12:14])[0]

            if ether_type == 0x0800:

                ip_start = 14
                version_ihl = packet[ip_start]

                ihl = (version_ihl & 0x0F) * 4

                if len(packet) < ip_start + ihl:
                    offset = packet_end
                    continue

                protocol = packet[ip_start + 9]

                if protocol == 17:

                    src_ip = ip_address(
                        packet[ip_start + 12:ip_start + 16]
                    )

                    dst_ip = ip_address(
                        packet[ip_start + 16:ip_start + 20]
                    )

                    udp_start = ip_start + ihl

                    if len(packet) >= udp_start + 8:

                        src_port, dst_port = struct.unpack(
                            ">HH",
                            packet[udp_start:udp_start + 4]
                        )

                        # DNS usually uses port 53
                        if src_port == 53 or dst_port == 53:

                            dns_start = udp_start + 8

                            if len(packet) >= dns_start + 12:

                                transaction_id = struct.unpack(
                                    ">H",
                                    packet[dns_start:dns_start + 2]
                                )[0]

                                flags = struct.unpack(
                                    ">H",
                                    packet[dns_start + 2:dns_start + 4]
                                )[0]

                                qdcount = struct.unpack(
                                    ">H",
                                    packet[dns_start + 4:dns_start + 6]
                                )[0]

                                # QR bit:
                                # 0 = query
                                # 1 = response
                                is_response = bool(flags & 0x8000)

                                if not is_response and qdcount > 0:

                                    name, next_offset = read_dns_name(
                                        packet,
                                        dns_start + 12
                                    )

                                    if name:

                                        type_offset = next_offset

                                        if type_offset + 4 <= len(packet):

                                            qtype = struct.unpack(
                                                ">H",
                                                packet[
                                                    type_offset:
                                                    type_offset + 2
                                                ]
                                            )[0]

                                            qtype_name = QUERY_TYPES.get(
                                                qtype,
                                                str(qtype)
                                            )

                                            domains[name] += 1
                                            query_types[qtype_name] += 1
                                            dns_servers[dst_ip] += 1

                                            queries.append(
                                                (
                                                    src_ip,
                                                    dst_ip,
                                                    name,
                                                    qtype_name,
                                                    transaction_id
                                                )
                                            )

        offset = packet_end

    return domains, query_types, dns_servers, queries


def main():
    print("================================")
    print("      FORENICOS DNS STATS")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        domains, query_types, dns_servers, queries = analyze_pcap(
            filename
        )

        print()
        print("DNS-DOMEINEN")
        print("--------------------------------")

        if domains:
            for domain, count in domains.most_common():
                print(f"{domain:<45} {count}")
        else:
            print("Geen DNS-queries gevonden.")

        print()
        print("QUERY TYPES")
        print("--------------------------------")

        for qtype, count in query_types.most_common():
            print(f"{qtype:<8} {count}")

        print()
        print("DNS-SERVERS")
        print("--------------------------------")

        for server, count in dns_servers.most_common():
            print(f"{server:<18} {count}")

        print()
        print("QUERIES")
        print("--------------------------------")

        for src, dst, domain, qtype, transaction_id in queries:
            print(
                f"{src} -> {dst} | "
                f"{domain} | {qtype} | "
                f"ID {transaction_id}"
            )

        print()
        print("================================")
        print("Totaal DNS-queries:", len(queries))
        print("Unieke domeinen:", len(domains))
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

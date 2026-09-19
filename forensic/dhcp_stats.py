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


MESSAGE_TYPES = {
    1: "DISCOVER",
    2: "OFFER",
    3: "REQUEST",
    4: "DECLINE",
    5: "ACK",
    6: "NAK",
    7: "RELEASE",
    8: "INFORM",
}


def ip_address(data):
    return ".".join(str(x) for x in data)


def mac_address(data):
    return ":".join(f"{x:02x}" for x in data)


def parse_options(data):
    options = {}
    offset = 0

    while offset < len(data):

        option = data[offset]

        if option == 0:
            offset += 1
            continue

        if option == 255:
            break

        if offset + 1 >= len(data):
            break

        length = data[offset + 1]

        if offset + 2 + length > len(data):
            break

        value = data[
            offset + 2:
            offset + 2 + length
        ]

        options[option] = value
        offset += 2 + length

    return options


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

    message_types = Counter()
    clients = Counter()
    servers = Counter()
    requested_ips = Counter()
    hostnames = Counter()
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

        # Ethernet + IPv4 + UDP
        if len(packet) >= 42:

            ether_type = struct.unpack(
                ">H", packet[12:14]
            )[0]

            if ether_type == 0x0800:

                ip_start = 14
                ihl = (packet[ip_start] & 0x0F) * 4

                if len(packet) >= ip_start + ihl:

                    protocol = packet[ip_start + 9]

                    if protocol == 17:

                        udp_start = ip_start + ihl

                        if len(packet) >= udp_start + 8:

                            src_port, dst_port = struct.unpack(
                                ">HH",
                                packet[
                                    udp_start:
                                    udp_start + 4
                                ]
                            )

                            # DHCP: UDP 67/68
                            if (
                                src_port in (67, 68)
                                or dst_port in (67, 68)
                            ):

                                udp_payload = packet[
                                    udp_start + 8:
                                ]

                                # BOOTP header = 236 bytes
                                if len(udp_payload) >= 240:

                                    client_mac = mac_address(
                                        udp_payload[28:34]
                                    )

                                    yiaddr = ip_address(
                                        udp_payload[16:20]
                                    )

                                    options = parse_options(
                                        udp_payload[236:]
                                    )

                                    # DHCP message type option 53
                                    if 53 in options:
                                        msg_type = options[53][0]

                                        msg_name = MESSAGE_TYPES.get(
                                            msg_type,
                                            f"TYPE {msg_type}"
                                        )

                                        message_types[
                                            msg_name
                                        ] += 1

                                    else:
                                        msg_name = "UNKNOWN"

                                    clients[
                                        client_mac
                                    ] += 1

                                    if yiaddr != "0.0.0.0":
                                        requested_ips[
                                            yiaddr
                                        ] += 1

                                    # Hostname option 12
                                    if 12 in options:

                                        try:
                                            hostname = options[
                                                12
                                            ].decode(
                                                "utf-8",
                                                errors="replace"
                                            ).strip()

                                            if hostname:
                                                hostnames[
                                                    hostname
                                                ] += 1

                                        except Exception:
                                            pass

                                    # Server identifier option 54
                                    if 54 in options and len(
                                        options[54]
                                    ) == 4:

                                        server_ip = ip_address(
                                            options[54]
                                        )

                                        servers[
                                            server_ip
                                        ] += 1

                                    conversations[
                                        (
                                            client_mac,
                                            msg_name,
                                            yiaddr
                                        )
                                    ] += 1

        offset = packet_end

    return (
        message_types,
        clients,
        servers,
        requested_ips,
        hostnames,
        conversations,
    )


def main():
    print("================================")
    print("      FORENICOS DHCP STATS")
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
            message_types,
            clients,
            servers,
            requested_ips,
            hostnames,
            conversations,
        ) = analyze_pcap(filename)

        print()
        print("DHCP MESSAGE TYPES")
        print("--------------------------------")

        if message_types:
            for name, count in message_types.most_common():
                print(f"{name:<12} {count}")
        else:
            print("Geen DHCP-verkeer gevonden.")

        print()
        print("CLIENTS")
        print("--------------------------------")

        for mac, count in clients.most_common():
            print(f"{mac:<20} {count}")

        print()
        print("DHCP SERVERS")
        print("--------------------------------")

        for server, count in servers.most_common():
            print(f"{server:<18} {count}")

        print()
        print("IP-ADRESSEN")
        print("--------------------------------")

        for ip, count in requested_ips.most_common():
            print(f"{ip:<18} {count}")

        print()
        print("HOSTNAMEN")
        print("--------------------------------")

        for hostname, count in hostnames.most_common():
            print(f"{hostname:<35} {count}")

        print()
        print("DHCP VERKEER")
        print("--------------------------------")

        for (
            mac,
            message,
            ip
        ), count in conversations.most_common():

            print(
                f"{mac} | "
                f"{message:<8} | "
                f"{ip} : {count}"
            )

        print()
        print("================================")
        print("DHCP pakketten:", sum(message_types.values()))
        print("Clients       :", len(clients))
        print("Servers       :", len(servers))
        print("Hostnamen     :", len(hostnames))
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

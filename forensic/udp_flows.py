#!/usr/bin/env python3

import os
import struct
from collections import defaultdict


PCAP_MAGIC = {
    b"\xd4\xc3\xb2\xa1": "<",
    b"\xa1\xb2\xc3\xd4": ">",
    b"\x4d\x3c\xb2\xa1": "<",
    b"\xa1\xb2\x3c\x4d": ">",
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

    flows = defaultdict(lambda: {
        "packets": 0,
        "bytes": 0,
    })

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

            # IPv4
            if ether_type == 0x0800 and len(packet) >= 34:

                ip_start = 14
                version_ihl = packet[ip_start]
                ihl = (version_ihl & 0x0F) * 4

                if len(packet) >= ip_start + ihl:

                    protocol = packet[ip_start + 9]

                    # UDP
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

                            key = (
                                src_ip,
                                src_port,
                                dst_ip,
                                dst_port,
                            )

                            flows[key]["packets"] += 1
                            flows[key]["bytes"] += len(packet)

        offset = packet_end

    return flows


def main():
    print("================================")
    print("       FORENICOS UDP FLOWS")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        flows = analyze_pcap(filename)

        print()
        print("UDP FLOWS")
        print("--------------------------------")

        if not flows:
            print("Geen UDP-verkeer gevonden.")

        else:
            sorted_flows = sorted(
                flows.items(),
                key=lambda item: item[1]["bytes"],
                reverse=True
            )

            for (
                src_ip,
                src_port,
                dst_ip,
                dst_port,
            ), stats in sorted_flows:

                print(
                    f"{src_ip}:{src_port} -> "
                    f"{dst_ip}:{dst_port}"
                )

                print(
                    f"  Pakketten : {stats['packets']}"
                )

                print(
                    f"  Bytes     : {stats['bytes']}"
                )

                print("--------------------------------")

        print()
        print("Totaal UDP-flows:", len(flows))

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

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


def parse_http(payload):
    try:
        text = payload.decode("latin1", errors="ignore")
    except Exception:
        return None

    lines = text.split("\r\n")

    if not lines:
        return None

    first = lines[0]

    methods = (
        "GET ",
        "POST ",
        "PUT ",
        "DELETE ",
        "HEAD ",
        "OPTIONS ",
        "PATCH ",
    )

    if first.startswith(methods):
        parts = first.split(" ", 2)

        if len(parts) < 2:
            return None

        method = parts[0]
        path = parts[1]

        host = ""

        for line in lines[1:]:
            if line.lower().startswith("host:"):
                host = line[5:].strip()
                break

        return {
            "type": "request",
            "method": method,
            "path": path,
            "host": host,
            "status": "",
        }

    if first.startswith("HTTP/"):
        parts = first.split(" ", 2)

        if len(parts) < 2:
            return None

        status = parts[1]

        return {
            "type": "response",
            "method": "",
            "path": "",
            "host": "",
            "status": status,
        }

    return None


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

    hosts = Counter()
    methods = Counter()
    paths = Counter()
    statuses = Counter()

    requests = []
    responses = []

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

                    # TCP
                    if protocol == 6:

                        src_ip = ip_address(
                            packet[ip_start + 12:ip_start + 16]
                        )

                        dst_ip = ip_address(
                            packet[ip_start + 16:ip_start + 20]
                        )

                        tcp_start = ip_start + ihl

                        if len(packet) >= tcp_start + 20:

                            src_port, dst_port = struct.unpack(
                                ">HH",
                                packet[tcp_start:tcp_start + 4]
                            )

                            data_offset = (
                                packet[tcp_start + 12] >> 4
                            ) * 4

                            payload_start = tcp_start + data_offset

                            if payload_start <= len(packet):

                                payload = packet[payload_start:]

                                # HTTP commonly uses TCP 80
                                if src_port == 80 or dst_port == 80:

                                    result = parse_http(payload)

                                    if result:

                                        if result["type"] == "request":

                                            methods[
                                                result["method"]
                                            ] += 1

                                            if result["host"]:
                                                hosts[
                                                    result["host"]
                                                ] += 1

                                            if result["path"]:
                                                paths[
                                                    result["path"]
                                                ] += 1

                                            requests.append(
                                                (
                                                    src_ip,
                                                    dst_ip,
                                                    result["method"],
                                                    result["host"],
                                                    result["path"]
                                                )
                                            )

                                        elif result["type"] == "response":

                                            statuses[
                                                result["status"]
                                            ] += 1

                                            responses.append(
                                                (
                                                    src_ip,
                                                    dst_ip,
                                                    result["status"]
                                                )
                                            )

        offset = packet_end

    return hosts, methods, paths, statuses, requests, responses


def main():
    print("================================")
    print("      FORENICOS HTTP STATS")
    print("================================")
    print()

    filename = input("PCAP bestand: ").strip()

    if not os.path.isfile(filename):
        print()
        print("FOUT: bestand bestaat niet.")
        input("Druk ENTER...")
        return

    try:
        hosts, methods, paths, statuses, requests, responses = (
            analyze_pcap(filename)
        )

        print()
        print("HTTP HOSTS")
        print("--------------------------------")

        if hosts:
            for host, count in hosts.most_common():
                print(f"{host:<45} {count}")
        else:
            print("Geen HTTP-hosts gevonden.")

        print()
        print("METHODES")
        print("--------------------------------")

        for method, count in methods.most_common():
            print(f"{method:<10} {count}")

        print()
        print("STATUSCODES")
        print("--------------------------------")

        for status, count in statuses.most_common():
            print(f"{status:<10} {count}")

        print()
        print("URL-PADEN")
        print("--------------------------------")

        for path, count in paths.most_common():
            print(f"{path:<60} {count}")

        print()
        print("HTTP REQUESTS")
        print("--------------------------------")

        for src, dst, method, host, path in requests:
            print(
                f"{src} -> {dst} | "
                f"{method} | {host}{path}"
            )

        print()
        print("HTTP RESPONSES")
        print("--------------------------------")

        for src, dst, status in responses:
            print(
                f"{src} -> {dst} | "
                f"HTTP {status}"
            )

        print()
        print("================================")
        print("Requests :", len(requests))
        print("Responses:", len(responses))
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

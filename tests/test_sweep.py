import ipaddress
import socket


def test_hostname():
    assert socket.gethostname()


def test_local_network():
    network = ipaddress.ip_network(
        "192.168.1.0/24"
    )

    assert network.prefixlen == 24
    assert network.num_addresses == 256


if __name__ == "__main__":
    test_hostname()
    test_local_network()

    print("SWEEP TEST: PASS")

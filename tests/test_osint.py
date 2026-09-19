import ipaddress
import os
import tempfile
from urllib.parse import urlparse


def test_url():
    parsed = urlparse(
        "https://example.com/test?a=1"
    )

    assert parsed.hostname == "example.com"
    assert parsed.path == "/test"


def test_ip():
    ip = ipaddress.ip_address("192.168.1.1")

    assert ip.is_private
    assert not ip.is_global


def test_file():
    with tempfile.NamedTemporaryFile(
        delete=False
    ) as f:
        f.write(b"ForensicOS")

        path = f.name

    assert os.path.getsize(path) == 10

    os.unlink(path)


if __name__ == "__main__":
    test_url()
    test_ip()
    test_file()

    print("OSINT TEST: PASS")

import os
import socket
import subprocess


def test_hostname():
    assert socket.gethostname()


def test_proc():
    assert os.path.exists("/proc")


def test_ss():
    result = subprocess.run(
        ["ss", "-lnt"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0


def test_hash():
    import hashlib

    data = b"ForensicOS"

    result = hashlib.sha256(data).hexdigest()

    assert len(result) == 64


if __name__ == "__main__":
    test_hostname()
    test_proc()
    test_ss()
    test_hash()

    print("DEFENSE TEST: PASS")

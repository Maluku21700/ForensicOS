import socket
import subprocess


def test_hostname():
    assert socket.gethostname()


def test_processes():
    result = subprocess.run(
        ["ps", "-e"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert result.stdout


def test_sockets():
    result = subprocess.run(
        ["ss", "-tun"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0


if __name__ == "__main__":
    test_hostname()
    test_processes()
    test_sockets()

    print("SURVEILLANCE TEST: PASS")

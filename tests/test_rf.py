import os
import tempfile


def test_log_file():
    with tempfile.NamedTemporaryFile(
        delete=False
    ) as f:
        f.write(b"RFTEST")

        path = f.name

    assert os.path.isfile(path)

    os.unlink(path)


def test_frequency():
    frequency = 433.92

    assert frequency > 0
    assert frequency < 10000


if __name__ == "__main__":
    test_log_file()
    test_frequency()

    print("RF TEST: PASS")

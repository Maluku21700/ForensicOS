import hashlib
import os
import tempfile


def test_hash():
    data = b"ForensicOS test"

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(data)
        path = f.name

    expected = hashlib.sha256(data).hexdigest()

    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024), b""):
            h.update(block)

    os.unlink(path)

    assert h.hexdigest() == expected


if __name__ == "__main__":
    test_hash()
    print("FORENSICS TEST: PASS")

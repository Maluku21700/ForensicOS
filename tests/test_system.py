import os
import platform


def test_platform():
    assert platform.system()


def test_hostname():
    assert platform.node()


def test_cpu():
    assert os.cpu_count() is not None
    assert os.cpu_count() > 0


def test_proc():
    assert os.path.exists("/proc")


def test_memory():
    assert os.path.exists("/proc/meminfo")


def test_disk():
    assert os.path.exists("/")


if __name__ == "__main__":
    test_platform()
    test_hostname()
    test_cpu()
    test_proc()
    test_memory()
    test_disk()

    print("SYSTEM TEST: PASS")

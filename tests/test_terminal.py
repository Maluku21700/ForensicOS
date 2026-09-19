import os

from terminal.runner import run
from terminal.shell import execute


def test_runner():
    result = run(["echo", "ForensicOS"])

    assert result["returncode"] == 0
    assert "ForensicOS" in result["stdout"]


def test_runner_failure():
    result = run(["command_that_should_not_exist_12345"])

    assert result["returncode"] != 0


def test_pwd():
    original = os.getcwd()

    assert execute("pwd") is True

    os.chdir(original)


def test_help():
    assert execute("help") is True


def test_exit():
    assert execute("exit") is False


if __name__ == "__main__":
    test_runner()
    test_runner_failure()
    test_pwd()
    test_help()
    test_exit()

    print("TERMINAL TEST: PASS")

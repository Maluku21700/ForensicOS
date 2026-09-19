import shutil
import subprocess


def main():
    print("========== RTL-SDR INFO ==========\n")

    binary = shutil.which("rtl_test")

    if not binary:
        print("rtl_test: NIET GEVONDEN")
        print()
        print("Installatie:")
        print("sudo apt install rtl-sdr")
        return

    print("rtl_test:", binary)

    try:
        result = subprocess.run(
            ["rtl_test", "-t"],
            capture_output=True,
            text=True,
            timeout=8
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

    except subprocess.TimeoutExpired:
        print("Test timeout.")

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

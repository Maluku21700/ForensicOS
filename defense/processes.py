import subprocess


def main():
    print("\n========== PROCESS ANALYZER ==========\n")

    result = subprocess.run(
        ["ps", "aux", "--sort=-%cpu"],
        capture_output=True,
        text=True
    )

    print(result.stdout)


if __name__ == "__main__":
    main()

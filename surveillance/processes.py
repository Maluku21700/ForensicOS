import subprocess


def main():
    print("========== RUNNING PROCESSES ==========\n")

    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

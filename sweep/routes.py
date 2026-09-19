import subprocess


def main():
    print("========== ROUTING TABLE ==========\n")

    try:
        result = subprocess.run(
            ["ip", "route"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

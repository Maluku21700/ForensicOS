import subprocess


def main():
    print("========== MEMORY ==========\n")

    try:
        result = subprocess.run(
            ["free", "-h"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

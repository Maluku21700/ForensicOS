import subprocess


def main():
    print("========== LISTENING SERVICES ==========\n")

    try:
        result = subprocess.run(
            ["ss", "-lntup"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

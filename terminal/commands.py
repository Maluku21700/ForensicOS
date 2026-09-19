import os
import subprocess


def main():
    print("\n========== TERMINAL TOOLS ==========\n")

    print("PWD :", os.getcwd())

    while True:
        command = input("ForensicOS-shell > ").strip()

        if command in ("exit", "quit", "back"):
            break

        if not command:
            continue

        try:
            subprocess.run(
                command,
                shell=True
            )
        except Exception as e:
            print("FOUT:", e)


if __name__ == "__main__":
    main()

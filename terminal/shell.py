import os
import shlex
import subprocess


BUILTINS = {
    "help",
    "pwd",
    "ls",
    "cd",
    "clear",
    "whoami",
    "exit",
    "quit",
}


def show_help():
    print("""
ForensicOS Terminal

Built-in:
  help       Help
  pwd        Current directory
  ls         List files
  cd PATH    Change directory
  clear      Clear screen
  whoami     Current user
  exit       Exit terminal

Andere normale Linux-commando's kunnen ook
worden uitgevoerd.
""")


def execute(command):
    if not command:
        return True

    try:
        parts = shlex.split(command)
    except ValueError as e:
        print("Parse error:", e)
        return True

    if not parts:
        return True

    cmd = parts[0]

    if cmd in ("exit", "quit"):
        return False

    if cmd == "help":
        show_help()
        return True

    if cmd == "pwd":
        print(os.getcwd())
        return True

    if cmd == "ls":
        target = parts[1] if len(parts) > 1 else "."
        try:
            for item in os.listdir(os.path.expanduser(target)):
                print(item)
        except Exception as e:
            print("FOUT:", e)
        return True

    if cmd == "cd":
        target = parts[1] if len(parts) > 1 else os.path.expanduser("~")

        try:
            os.chdir(os.path.expanduser(target))
        except Exception as e:
            print("FOUT:", e)

        return True

    if cmd == "clear":
        os.system("clear")
        return True

    if cmd == "whoami":
        subprocess.run(["whoami"])
        return True

    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True
        )

        if result.stdout:
            print(result.stdout, end="")

        if result.stderr:
            print(result.stderr, end="")

    except FileNotFoundError:
        print("Command niet gevonden:", cmd)

    except Exception as e:
        print("FOUT:", e)

    return True


def main():
    print("""
==========================================
          FORENICOS TERMINAL
==========================================
Typ 'help' voor beschikbare commando's.
Typ 'exit' om te stoppen.
""")

    while True:
        try:
            prompt = f"ForensicOS:{os.getcwd()}$ "
            command = input(prompt)

            if not execute(command):
                break

        except KeyboardInterrupt:
            print("\nGebruik 'exit' om te stoppen.")

        except EOFError:
            print()
            break


if __name__ == "__main__":
    main()

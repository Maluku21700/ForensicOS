import os
import platform


def main():
    print("========== SYSTEM STATUS ==========\n")

    print("Hostname:")
    print(platform.node())

    print("\nKernel:")
    print(platform.release())

    print("\nArchitecture:")
    print(platform.machine())

    print("\nCPU cores:")
    print(os.cpu_count())

    print("\nLoad average:")

    try:
        load = os.getloadavg()

        print(
            f"1 min : {load[0]:.2f}"
        )
        print(
            f"5 min : {load[1]:.2f}"
        )
        print(
            f"15 min: {load[2]:.2f}"
        )

    except OSError:
        print("Niet beschikbaar.")

    print("\nUptime:")

    try:
        with open("/proc/uptime") as f:
            seconds = float(
                f.read().split()[0]
            )

        hours = seconds / 3600

        print(f"{hours:.2f} uur")

    except Exception as e:
        print("FOUT:", e)


if __name__ == "__main__":
    main()

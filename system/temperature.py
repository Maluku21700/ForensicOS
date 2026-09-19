import os
import glob


def read_thermal_zones():
    results = []

    paths = glob.glob(
        "/sys/class/thermal/thermal_zone*/temp"
    )

    for path in sorted(paths):
        try:
            with open(path) as f:
                value = int(f.read().strip())

            results.append(
                (path, value / 1000.0)
            )

        except (ValueError, PermissionError, FileNotFoundError):
            continue

    return results


def main():
    print("========== TEMPERATURE ==========\n")

    results = read_thermal_zones()

    if not results:
        print("Geen thermal zones gevonden.")
        return

    for path, temperature in results:
        zone = os.path.basename(
            os.path.dirname(path)
        )

        print(
            f"{zone}: "
            f"{temperature:.1f} °C"
        )


if __name__ == "__main__":
    main()

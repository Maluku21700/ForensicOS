import csv
import os
from datetime import datetime


ROOT = os.path.expanduser("~/ForensicOS")
LOG = os.path.join(ROOT, "logs", "rf_measurements.csv")


def log_measurement(
    frequency_mhz,
    power_db,
    source="manual"
):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)

    exists = os.path.exists(LOG)

    with open(
        LOG,
        "a",
        newline=""
    ) as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "frequency_mhz",
                "power_db",
                "source"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            frequency_mhz,
            power_db,
            source
        ])


def main():
    print("========== RF LOGGER ==========\n")

    frequency = input(
        "Frequency MHz: "
    ).strip()

    power = input(
        "Power dB: "
    ).strip()

    try:
        log_measurement(
            float(frequency),
            float(power)
        )

        print("Meting opgeslagen:")
        print(LOG)

    except ValueError:
        print("Ongeldige numerieke waarde.")


if __name__ == "__main__":
    main()

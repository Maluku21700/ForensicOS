from dataclasses import dataclass


@dataclass
class Band:
    name: str
    start_mhz: float
    end_mhz: float
    purpose: str


BANDS = [
    Band("FM Broadcast", 87.5, 108.0, "FM radio"),
    Band("433 MHz ISM", 433.05, 434.79, "ISM"),
    Band("868 MHz ISM", 863.0, 870.0, "ISM"),
    Band("2.4 GHz ISM", 2400.0, 2483.5, "ISM / Wi-Fi / Bluetooth")
]


def main():
    print("========== RF FREQUENCY PLAN ==========\n")

    print(
        "Dit is alleen een referentie-overzicht "
        "van algemene banden.\n"
    )

    for band in BANDS:
        print(
            f"{band.name:18} "
            f"{band.start_mhz:8.2f} - "
            f"{band.end_mhz:8.2f} MHz | "
            f"{band.purpose}"
        )


if __name__ == "__main__":
    main()

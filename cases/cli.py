from .manager import (
    create_case,
    list_cases,
    load_case,
)


def main():
    print("==========================================")
    print("       FORENICOS CASE MANAGER")
    print("==========================================")

    while True:
        print("""
[1] Nieuwe case
[2] Cases bekijken
[3] Case details
[0] Exit
""")

        choice = input("ForensicOS Cases > ").strip()

        if choice == "1":
            name = input("Case naam: ").strip()
            description = input(
                "Beschrijving: "
            ).strip()

            if not name:
                print("Case naam ontbreekt.")
                continue

            case = create_case(
                name,
                description
            )

            print(
                "\nCase aangemaakt:",
                case["case_id"]
            )

        elif choice == "2":
            cases = list_cases()

            if not cases:
                print("\nGeen cases.")
                continue

            print()

            for case in cases:
                print(
                    case["case_id"],
                    "|",
                    case["name"]
                )

        elif choice == "3":
            case_id = input(
                "Case ID: "
            ).strip()

            try:
                case = load_case(case_id)

                print("\nCase:")
                print(
                    "ID:",
                    case["case_id"]
                )
                print(
                    "Naam:",
                    case["name"]
                )
                print(
                    "Beschrijving:",
                    case["description"]
                )
                print(
                    "Evidence:",
                    len(case["evidence"])
                )

            except FileNotFoundError:
                print("Case niet gevonden.")

        elif choice == "0":
            break

        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()

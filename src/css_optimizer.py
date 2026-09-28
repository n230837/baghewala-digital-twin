# ============================================================
# BAGHEWALA DIGITAL TWIN
# CSS CANDIDATE GENERATOR
# ============================================================

from thermal_model import simulate_css_cycle


def generate_css_candidates():
    """
    Generate physically constrained CSS scenarios.

    These ranges are prototype search ranges based on the
    operating envelope currently encoded in our thermal model.

    They are NOT recommended Baghewala operating settings.
    """

    steam_temperatures = [
        250.0,
        270.0,
        285.0,
        300.0,
        320.0
    ]

    steam_volumes = [
        300.0,
        400.0,
        500.0,
        600.0,
        700.0
    ]

    injection_days = [
        14.0,
        17.0,
        21.0
    ]

    soak_days = [
        5.0,
        7.0
    ]

    candidates = []

    for steam_temperature in steam_temperatures:

        for steam_volume in steam_volumes:

            for injection in injection_days:

                for soak in soak_days:

                    result = simulate_css_cycle(
                        initial_temperature_c=47.0,
                        steam_temperature_c=
                            steam_temperature,
                        steam_volume_m3=
                            steam_volume,
                        injection_days=
                            injection,
                        soak_days=
                            soak
                    )

                    candidates.append({
                        "steam_temperature_c":
                            steam_temperature,

                        "steam_volume_m3":
                            steam_volume,

                        "injection_days":
                            injection,

                        "soak_days":
                            soak,

                        "heated_temperature_c":
                            result[
                                "heated_temperature_c"
                            ],

                        "production_start_temperature_c":
                            result[
                                "production_start_temperature_c"
                            ]
                    })

    return candidates


if __name__ == "__main__":

    print("================================================")
    print("       CSS CANDIDATE GENERATOR")
    print("================================================")

    candidates = generate_css_candidates()

    print(
        f"\nTotal CSS candidates: "
        f"{len(candidates)}"
    )

    print("\nFIRST 10 CANDIDATES")
    print("-------------------")

    for candidate in candidates[:10]:

        print(
            f"\nSteam: "
            f"{candidate['steam_temperature_c']:.0f} °C"
        )

        print(
            f"Volume: "
            f"{candidate['steam_volume_m3']:.0f} m³"
        )

        print(
            f"Injection: "
            f"{candidate['injection_days']:.0f} days"
        )

        print(
            f"Soak: "
            f"{candidate['soak_days']:.0f} days"
        )

        print(
            f"Heated temperature: "
            f"{candidate['heated_temperature_c']:.2f} °C"
        )

        print(
            f"Production-start temperature: "
            f"{candidate['production_start_temperature_c']:.2f} °C"
        )

    print("\n================================================")
    print("       CSS CANDIDATE GENERATION COMPLETE")
    print("================================================")
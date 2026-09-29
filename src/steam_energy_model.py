# ============================================================
# BAGHEWALA DIGITAL TWIN
# STEAM ENERGY MODEL
# ============================================================

# Prototype assumptions.
# These are NOT calibrated field energy measurements.


DEFAULT_STEAM_ENTHALPY_KWH_PER_M3 = 700.0

# Prototype reference value.
# Later this should come from the actual steam generator /
# field steam-generation system.


def calculate_steam_energy(
    steam_volume_m3,
    steam_temperature_c,
    injection_days
):
    """
    Estimate energy required for CSS steam injection.

    This is a prototype energy model.

    Energy depends primarily on:
        - steam volume
        - steam temperature
        - injection duration

    The temperature factor is normalized around 285°C.
    """

    if steam_volume_m3 < 0:
        raise ValueError(
            "Steam volume cannot be negative."
        )

    if injection_days <= 0:
        raise ValueError(
            "Injection duration must be positive."
        )

    if steam_temperature_c <= 0:
        raise ValueError(
            "Steam temperature must be positive."
        )

    # --------------------------------------------------------
    # Temperature factor
    # --------------------------------------------------------

    temperature_factor = (
        steam_temperature_c / 285.0
    )

    # --------------------------------------------------------
    # Base energy
    # --------------------------------------------------------

    energy_kwh = (
        steam_volume_m3
        * DEFAULT_STEAM_ENTHALPY_KWH_PER_M3
        * temperature_factor
    )

    return energy_kwh


def calculate_energy_per_barrel(
    energy_kwh,
    oil_production_bpd,
    production_days
):
    """
    Calculate energy consumed per barrel of produced oil.

    Energy per barrel = total energy / total oil produced.
    """

    if energy_kwh < 0:
        raise ValueError(
            "Energy cannot be negative."
        )

    if oil_production_bpd <= 0:
        raise ValueError(
            "Oil production must be positive."
        )

    if production_days <= 0:
        raise ValueError(
            "Production duration must be positive."
        )

    total_oil_barrels = (
        oil_production_bpd
        * production_days
    )

    energy_per_barrel_kwh = (
        energy_kwh
        / total_oil_barrels
    )

    return energy_per_barrel_kwh


def calculate_operating_cost(
    energy_kwh,
    steam_volume_m3,
    electricity_cost_per_kwh,
    steam_cost_per_m3
):
    """
    Calculate prototype CSS operating cost from energy and steam costs.

    Total operating cost =
        electricity cost + steam cost

    This is an operational cost estimate and depends on user-supplied
    economic assumptions; it is not a calibrated Baghewala field cost.
    """

    if energy_kwh < 0:
        raise ValueError("Energy cannot be negative.")

    if steam_volume_m3 < 0:
        raise ValueError("Steam volume cannot be negative.")

    if electricity_cost_per_kwh < 0:
        raise ValueError("Electricity cost cannot be negative.")

    if steam_cost_per_m3 < 0:
        raise ValueError("Steam cost cannot be negative.")

    electricity_cost = energy_kwh * electricity_cost_per_kwh
    steam_cost = steam_volume_m3 * steam_cost_per_m3
    total_operating_cost = electricity_cost + steam_cost

    return {
        "electricity_cost": electricity_cost,
        "steam_cost": steam_cost,
        "total_operating_cost": total_operating_cost
    }


if __name__ == "__main__":

    print("================================================")
    print("       STEAM ENERGY MODEL")
    print("================================================")

    test_cases = [
        (250.0, 500.0, 14.0),
        (285.0, 500.0, 14.0),
        (320.0, 500.0, 14.0),
        (320.0, 700.0, 14.0),
        (320.0, 700.0, 21.0)
    ]

    print("\nENERGY ESTIMATES")
    print("----------------")

    for temperature, volume, days in test_cases:

        energy = calculate_steam_energy(
            steam_volume_m3=volume,
            steam_temperature_c=temperature,
            injection_days=days
        )

        print(
            f"\nSteam temperature : "
            f"{temperature:.0f} °C"
        )

        print(
            f"Steam volume      : "
            f"{volume:.0f} m³"
        )

        print(
            f"Injection         : "
            f"{days:.0f} days"
        )

        print(
            f"Estimated energy  : "
            f"{energy:,.2f} kWh"
        )

    print("\n================================================")
    print("       STEAM ENERGY MODEL COMPLETE")
    print("================================================")
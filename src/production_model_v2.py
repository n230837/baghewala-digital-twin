# ============================================================
# BAGHEWALA DIGITAL TWIN
# PRODUCTION MODEL V2
# ============================================================

# Prototype defaults only.
# These are NOT calibrated Baghewala production parameters.


DEFAULT_BASE_PRODUCTION_BPD = 30.0
DEFAULT_REFERENCE_VISCOSITY_CP = 11500.0


def calculate_production_rate(
    viscosity_cp,
    pump_fillage_percent,
    pump_efficiency=1.0,
    base_production_bpd=DEFAULT_BASE_PRODUCTION_BPD,
    reference_viscosity_cp=DEFAULT_REFERENCE_VISCOSITY_CP
):
    """
    Estimate oil production rate.

    Prototype relationship:

        production =
        base production
        × viscosity mobility factor
        × pump fillage
        × pump efficiency

    This is a reduced-order prototype model.

    It is NOT calibrated to Baghewala production history.
    """

    if viscosity_cp <= 0:
        raise ValueError(
            "Viscosity must be positive."
        )

    if not 0 <= pump_fillage_percent <= 100:
        raise ValueError(
            "Pump fillage must be between 0 and 100%."
        )

    if not 0 < pump_efficiency <= 1:
        raise ValueError(
            "Pump efficiency must be between 0 and 1."
        )

    # --------------------------------------------------------
    # Viscosity mobility factor
    # --------------------------------------------------------

    mobility_factor = (
        reference_viscosity_cp
        / viscosity_cp
    )

    # Prevent unrealistic amplification.
    mobility_factor = min(
        mobility_factor,
        3.0
    )

    # --------------------------------------------------------
    # Pump fillage factor
    # --------------------------------------------------------

    fillage_factor = (
        pump_fillage_percent / 100.0
    )

    # --------------------------------------------------------
    # Production estimate
    # --------------------------------------------------------

    production_bpd = (
        base_production_bpd
        * mobility_factor
        * fillage_factor
        * pump_efficiency
    )

    return production_bpd


# ============================================================
# STEAM-OIL RATIO (SOR)
# ============================================================

BARREL_TO_M3 = 0.1589872949


def calculate_steam_oil_ratio(
    steam_volume_m3,
    oil_production_bpd,
    production_days
):
    """
    Calculate cumulative Steam-Oil Ratio (SOR).

    SOR = steam volume / cumulative oil volume

    Steam volume is in m³.
    Oil production is supplied as BPD and converted to m³
    over the specified production period.

    This is a prototype performance metric and does not
    represent a field-calibrated Baghewala SOR.
    """

    if steam_volume_m3 < 0:
        raise ValueError("Steam volume cannot be negative.")

    if oil_production_bpd <= 0:
        raise ValueError("Oil production must be positive.")

    if production_days <= 0:
        raise ValueError("Production days must be positive.")

    cumulative_oil_m3 = (
        oil_production_bpd
        * production_days
        * BARREL_TO_M3
    )

    return steam_volume_m3 / cumulative_oil_m3


if __name__ == "__main__":

    print("================================================")
    print("       BAGHEWALA PRODUCTION MODEL V2")
    print("================================================")

    viscosity = 7758.94

    test_fillages = [
        50.0,
        60.0,
        75.0,
        80.0,
        90.0
    ]

    print("\nINPUT")
    print("-----")
    print(
        f"Viscosity: {viscosity:.2f} cP"
    )

    print("\nPRODUCTION ESTIMATES")
    print("--------------------")

    for fillage in test_fillages:

        production = calculate_production_rate(
            viscosity_cp=viscosity,
            pump_fillage_percent=fillage
        )

        print(
            f"Fillage {fillage:>5.1f}%"
            f" -> "
            f"{production:>7.2f} BPD"
        )

    print("\nMODEL PARAMETERS")
    print("----------------")
    print(
        f"Base production: "
        f"{DEFAULT_BASE_PRODUCTION_BPD:.2f} BPD"
    )

    print(
        f"Reference viscosity: "
        f"{DEFAULT_REFERENCE_VISCOSITY_CP:.2f} cP"
    )

    print("\nNOTE")
    print("----")
    print(
        "This is a prototype production model."
    )

    print(
        "It must be calibrated using actual "
        "Baghewala production history before "
        "field-level use."
    )

    print("\n================================================")
    print("       PRODUCTION MODEL V2 COMPLETE")
    print("================================================")
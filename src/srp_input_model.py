# ============================================================
# BAGHEWALA DIGITAL TWIN
# SRP INPUT MODEL
# ============================================================

def estimate_srp_operating_condition(viscosity_cp):
    """
    Estimate a starting SRP operating condition based on
    oil viscosity.

    This is a prototype decision-support rule.
    It is NOT a field-calibrated Baghewala operating limit.
    """

    if viscosity_cp >= 10000:
        condition = "VERY HIGH VISCOSITY"
        recommended_spm = 3.0

    elif viscosity_cp >= 7000:
        condition = "HIGH VISCOSITY"
        recommended_spm = 4.0

    elif viscosity_cp >= 4000:
        condition = "MODERATE VISCOSITY"
        recommended_spm = 5.0

    else:
        condition = "LOWER VISCOSITY"
        recommended_spm = 6.0

    return {
        "viscosity_cp": viscosity_cp,
        "condition": condition,
        "starting_spm": recommended_spm
    }


if __name__ == "__main__":

    print("================================================")
    print("       SRP INPUT MODEL")
    print("================================================")

    test_viscosities = [
        13690.99,
        7758.94,
        4000.0,
        2000.0
    ]

    for viscosity in test_viscosities:

        result = estimate_srp_operating_condition(
            viscosity
        )

        print(
            f"\nViscosity: {result['viscosity_cp']:.2f} cP"
        )

        print(
            f"Condition: {result['condition']}"
        )

        print(
            f"Starting SPM: {result['starting_spm']:.1f}"
        )

    print("\n================================================")
    print("       SRP INPUT MODEL COMPLETE")
    print("================================================")
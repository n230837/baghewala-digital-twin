# --------------------------------------------------
# BAGHEWALA SRP PERFORMANCE MODEL
# --------------------------------------------------

# Prototype reference values
REFERENCE_SPM = 6.0
REFERENCE_STROKE_M = 2.5

# Base pump efficiency
BASE_PUMP_EFFICIENCY = 0.75


def calculate_srp_efficiency(
    spm,
    stroke_length_m,
    viscosity_cp
):
    """
    Estimate SRP pump efficiency.

    This is a simplified prototype model.
    It will later be replaced/calibrated using
    real SRP operating data and physics.
    """

    # Effect of pumping speed
    speed_ratio = spm / REFERENCE_SPM

    # Effect of stroke length
    stroke_ratio = stroke_length_m / REFERENCE_STROKE_M

    # Higher viscosity makes pumping more difficult
    viscosity_factor = (
        5000.0 / viscosity_cp
    )

    # Limit viscosity effect
    viscosity_factor = max(
        0.4,
        min(viscosity_factor, 1.2)
    )

    efficiency = (
        BASE_PUMP_EFFICIENCY
        * viscosity_factor
    )

    # Very high SPM can reduce efficiency
    if speed_ratio > 1.3:
        efficiency *= 0.90

    # Very low SPM can also reduce throughput
    if speed_ratio < 0.6:
        efficiency *= 0.90

    # Stroke effect
    efficiency *= (
        0.9 + 0.1 * min(stroke_ratio, 1.2)
    )

    # Keep efficiency within physical bounds
    efficiency = max(
        0.1,
        min(efficiency, 0.95)
    )

    return efficiency


def calculate_srp_production_factor(
    spm,
    stroke_length_m,
    viscosity_cp
):
    """
    Estimate the relative SRP production factor.

    This represents the effect of SRP settings on
    the production potential predicted by our
    thermal/viscosity model.
    """

    efficiency = calculate_srp_efficiency(
        spm,
        stroke_length_m,
        viscosity_cp
    )

    # Relative pumping volume
    pumping_factor = (
        spm
        * stroke_length_m
        / (
            REFERENCE_SPM
            * REFERENCE_STROKE_M
        )
    )

    production_factor = (
        pumping_factor
        * efficiency
        / BASE_PUMP_EFFICIENCY
    )

    return production_factor


if __name__ == "__main__":

    viscosity = 5000.0

    spm_values = [4, 6, 8, 10]

    stroke = 2.5

    print("Baghewala SRP Performance Model")
    print("--------------------------------")

    for spm in spm_values:

        efficiency = calculate_srp_efficiency(
            spm,
            stroke,
            viscosity
        )

        production_factor = calculate_srp_production_factor(
            spm,
            stroke,
            viscosity
        )

        print(
            f"SPM: {spm:>2} | "
            f"Efficiency: {efficiency:.3f} | "
            f"Production factor: "
            f"{production_factor:.2f}"
        )
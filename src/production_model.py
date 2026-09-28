# --------------------------------------------------
# BAGHEWALA PRODUCTION RESPONSE MODEL
# --------------------------------------------------

# Prototype reference production rate.
# This is NOT real Baghewala field production data.
BASE_PRODUCTION_BPD = 30.0

# Reference viscosity corresponding to our baseline condition.
REFERENCE_VISCOSITY_CP = 11500.0


def calculate_production_rate(
    viscosity_cp,
    pump_efficiency=1.0
):
    """
    Estimate production response from oil viscosity.

    This is a simplified prototype relationship.
    It will later be replaced/calibrated using
    actual production data.
    """

    # Relative mobility:
    # lower viscosity -> higher mobility
    mobility_ratio = (
        REFERENCE_VISCOSITY_CP / viscosity_cp
    )

    # Prevent unrealistic growth in this first prototype
    mobility_ratio = min(mobility_ratio, 3.0)

    production = (
        BASE_PRODUCTION_BPD
        * mobility_ratio
        * pump_efficiency
    )

    return production


if __name__ == "__main__":

    viscosities = [
        11500,
        7000,
        5000,
        3000,
        2000
    ]

    print("Baghewala Production Response Model")
    print("------------------------------------")

    for viscosity in viscosities:

        production = calculate_production_rate(
            viscosity
        )

        print(
            f"Viscosity: {viscosity:>6.0f} cP "
            f"→ Production: {production:.2f} BPD"
        )
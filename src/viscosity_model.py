import numpy as np


# --------------------------------------------------
# Baghewala Heavy-Oil Viscosity Model
# --------------------------------------------------

# Reference condition
REFERENCE_TEMPERATURE_C = 50.0

# Oil India reports approximately 10,000–13,000 cP
# at around 50°C for Baghewala crude.
# We use the midpoint for our initial prototype.
REFERENCE_VISCOSITY_CP = 11500.0

# Initial model parameter.
# This is a prototype assumption and will later be
# calibrated using real data if available.
ACTIVATION_ENERGY = 50000.0

# Universal gas constant
R = 8.314


def viscosity_arrhenius(temperature_c):
    """
    Estimate heavy-oil viscosity at a given temperature.

    Parameters
    ----------
    temperature_c : float
        Oil temperature in Celsius.

    Returns
    -------
    float
        Estimated viscosity in cP.
    """

    # Convert Celsius to Kelvin
    temperature_k = temperature_c + 273.15
    reference_temperature_k = REFERENCE_TEMPERATURE_C + 273.15

    # Arrhenius-type temperature-viscosity relationship
    viscosity = (
        REFERENCE_VISCOSITY_CP
        * np.exp(
            (ACTIVATION_ENERGY / R)
            * (
                1 / temperature_k
                - 1 / reference_temperature_k
            )
        )
    )

    return viscosity


# --------------------------------------------------
# Simple test
# --------------------------------------------------

if __name__ == "__main__":

    temperatures = [40, 45, 50, 55, 60, 70, 80, 100]

    print("Baghewala Heavy-Oil Viscosity")
    print("--------------------------------")

    for temperature in temperatures:

        viscosity = viscosity_arrhenius(temperature)

        print(
            f"{temperature:>3} °C  →  "
            f"{viscosity:,.2f} cP"
        )
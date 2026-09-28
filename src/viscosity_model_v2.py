import numpy as np


# ============================================================
# BAGHEWALA HEAVY-OIL VISCOSITY MODEL V2
# Calibration-ready Arrhenius model
# ============================================================

# ------------------------------------------------------------
# PROTOTYPE DEFAULT PARAMETERS
# These are NOT field-calibrated values.
# They can later be replaced with PVT/lab/field data.
# ------------------------------------------------------------

DEFAULT_REFERENCE_TEMPERATURE_C = 50.0
DEFAULT_REFERENCE_VISCOSITY_CP = 11500.0
DEFAULT_ACTIVATION_ENERGY_J_MOL = 50000.0

GAS_CONSTANT = 8.314  # J/(mol·K)


def calculate_viscosity(
    temperature_c,
    reference_temperature_c=DEFAULT_REFERENCE_TEMPERATURE_C,
    reference_viscosity_cp=DEFAULT_REFERENCE_VISCOSITY_CP,
    activation_energy_j_mol=DEFAULT_ACTIVATION_ENERGY_J_MOL
):
    """
    Estimate heavy-oil viscosity using an Arrhenius-type model.

    Parameters
    ----------
    temperature_c : float or array
        Oil temperature in °C.

    reference_temperature_c : float
        Temperature at which reference viscosity is known.

    reference_viscosity_cp : float
        Reference viscosity in cP.

    activation_energy_j_mol : float
        Activation energy in J/mol.

    Returns
    -------
    float or numpy.ndarray
        Estimated viscosity in cP.
    """

    temperature_k = np.asarray(temperature_c) + 273.15
    reference_temperature_k = reference_temperature_c + 273.15

    if np.any(temperature_k <= 0):
        raise ValueError("Temperature must be above absolute zero.")

    if reference_viscosity_cp <= 0:
        raise ValueError("Reference viscosity must be positive.")

    if activation_energy_j_mol <= 0:
        raise ValueError("Activation energy must be positive.")

    viscosity_cp = (
        reference_viscosity_cp
        * np.exp(
            (activation_energy_j_mol / GAS_CONSTANT)
            * (
                1.0 / temperature_k
                - 1.0 / reference_temperature_k
            )
        )
    )

    return viscosity_cp


def calibrate_viscosity_model(
    temperature_c,
    measured_viscosity_cp,
    reference_temperature_c=DEFAULT_REFERENCE_TEMPERATURE_C
):
    """
    Estimate model parameters from measured viscosity-temperature data.

    Uses linear regression on:

        ln(mu) = ln(mu_ref)
                 + (Ea/R) * (1/T - 1/T_ref)

    This is intended for future laboratory/PVT calibration.
    """

    temperature_c = np.asarray(temperature_c, dtype=float)
    measured_viscosity_cp = np.asarray(
        measured_viscosity_cp,
        dtype=float
    )

    if len(temperature_c) != len(measured_viscosity_cp):
        raise ValueError(
            "Temperature and viscosity arrays must have the same length."
        )

    if len(temperature_c) < 2:
        raise ValueError(
            "At least two temperature-viscosity measurements are required."
        )

    if np.any(measured_viscosity_cp <= 0):
        raise ValueError(
            "Measured viscosity values must be positive."
        )

    temperature_k = temperature_c + 273.15
    reference_temperature_k = (
        reference_temperature_c + 273.15
    )

    x = (
        1.0 / temperature_k
        - 1.0 / reference_temperature_k
    )

    y = np.log(measured_viscosity_cp)

    slope, intercept = np.polyfit(x, y, 1)

    activation_energy = slope * GAS_CONSTANT

    reference_viscosity = np.exp(intercept)

    return {
        "reference_temperature_c": reference_temperature_c,
        "reference_viscosity_cp": reference_viscosity,
        "activation_energy_j_mol": activation_energy
    }


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    print("================================================")
    print("       BAGHEWALA VISCOSITY MODEL V2")
    print("================================================")

    temperatures = [47, 60, 80, 100]

    print("\nPROTOTYPE VISCOSITY ESTIMATES")
    print("------------------------------")

    for temperature in temperatures:

        viscosity = calculate_viscosity(temperature)

        print(
            f"{temperature:>5.1f} °C  ->  "
            f"{viscosity:>10.2f} cP"
        )

    print("\nMODEL PARAMETERS")
    print("----------------")
    print(
        f"Reference temperature: "
        f"{DEFAULT_REFERENCE_TEMPERATURE_C:.1f} °C"
    )

    print(
        f"Reference viscosity: "
        f"{DEFAULT_REFERENCE_VISCOSITY_CP:.1f} cP"
    )

    print(
        f"Activation energy: "
        f"{DEFAULT_ACTIVATION_ENERGY_J_MOL:.1f} J/mol"
    )

    print("\nNOTE")
    print("----")
    print(
        "These are prototype defaults and are not "
        "field-calibrated Baghewala PVT parameters."
    )

    print("\n================================================")
    print("       VISCOSITY MODEL V2 COMPLETE")
    print("================================================")
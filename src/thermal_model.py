import numpy as np


# ============================================================
# BAGHEWALA CSS THERMAL MODEL V2
# ============================================================

INITIAL_RESERVOIR_TEMP_C = 47.0

DEFAULT_STEAM_TEMPERATURE_C = 285.0

MIN_STEAM_TEMPERATURE_C = 250.0
MAX_STEAM_TEMPERATURE_C = 320.0

MIN_INJECTION_DAYS = 14.0
MAX_INJECTION_DAYS = 21.0


# Prototype thermal parameters.
# These are calibration parameters, NOT measured Baghewala values.

DEFAULT_HEAT_TRANSFER_EFFICIENCY = 0.25
DEFAULT_HEAT_LOSS_FACTOR = 0.10

REFERENCE_STEAM_VOLUME_M3 = 500.0
REFERENCE_INJECTION_DAYS = 14.0


def calculate_reservoir_temperature(
    initial_temperature_c,
    steam_temperature_c,
    steam_volume_m3,
    injection_days,
    heat_transfer_efficiency=
        DEFAULT_HEAT_TRANSFER_EFFICIENCY,
    heat_loss_factor=
        DEFAULT_HEAT_LOSS_FACTOR
):
    """
    Estimate reservoir temperature after CSS steam injection.

    Injection duration now affects the effective heat input.

    IMPORTANT:
    This is a reduced-order prototype model.
    Parameters must eventually be calibrated using
    Baghewala field/PVT/thermal data.
    """

    if steam_volume_m3 < 0:
        raise ValueError(
            "Steam volume cannot be negative."
        )

    if not (
        MIN_STEAM_TEMPERATURE_C
        <= steam_temperature_c
        <= MAX_STEAM_TEMPERATURE_C
    ):
        raise ValueError(
            f"Steam temperature should be between "
            f"{MIN_STEAM_TEMPERATURE_C} and "
            f"{MAX_STEAM_TEMPERATURE_C} °C."
        )

    if not (
        MIN_INJECTION_DAYS
        <= injection_days
        <= MAX_INJECTION_DAYS
    ):
        raise ValueError(
            f"Injection duration should be between "
            f"{MIN_INJECTION_DAYS} and "
            f"{MAX_INJECTION_DAYS} days."
        )

    # --------------------------------------------------------
    # Normalize steam volume
    # --------------------------------------------------------

    volume_factor = (
        steam_volume_m3
        / REFERENCE_STEAM_VOLUME_M3
    )

    # --------------------------------------------------------
    # Normalize injection duration
    # --------------------------------------------------------

    duration_factor = (
        injection_days
        / REFERENCE_INJECTION_DAYS
    )

    # --------------------------------------------------------
    # Effective heat input
    # --------------------------------------------------------

    steam_effect = (
        volume_factor
        * duration_factor
    )

    temperature_difference = (
        steam_temperature_c
        - initial_temperature_c
    )

    heat_added = (
        temperature_difference
        * heat_transfer_efficiency
        * steam_effect
    )

    # --------------------------------------------------------
    # Account for thermal losses
    # --------------------------------------------------------

    heat_added *= (
        1.0 - heat_loss_factor
    )

    final_temperature = (
        initial_temperature_c
        + heat_added
    )

    # Reservoir cannot exceed steam temperature
    final_temperature = min(
        final_temperature,
        steam_temperature_c
    )

    return final_temperature


def calculate_cooling_temperature(
    heated_temperature_c,
    initial_temperature_c,
    cooling_hours,
    cooling_rate=0.01
):
    """
    Estimate temperature decline during soak/cooling.
    """

    if cooling_hours < 0:
        raise ValueError(
            "Cooling time cannot be negative."
        )

    temperature_difference = (
        heated_temperature_c
        - initial_temperature_c
    )

    temperature = (
        initial_temperature_c
        + temperature_difference
        * np.exp(
            -cooling_rate * cooling_hours
        )
    )

    return temperature


def simulate_css_cycle(
    initial_temperature_c=INITIAL_RESERVOIR_TEMP_C,
    steam_temperature_c=DEFAULT_STEAM_TEMPERATURE_C,
    steam_volume_m3=500.0,
    injection_days=14.0,
    soak_days=7.0,
    cooling_rate=0.01
):
    """
    Simulate one CSS cycle.
    """

    heated_temperature = (
        calculate_reservoir_temperature(
            initial_temperature_c=
                initial_temperature_c,

            steam_temperature_c=
                steam_temperature_c,

            steam_volume_m3=
                steam_volume_m3,

            injection_days=
                injection_days
        )
    )

    soak_hours = soak_days * 24.0

    production_start_temperature = (
        calculate_cooling_temperature(
            heated_temperature,
            initial_temperature_c,
            soak_hours,
            cooling_rate
        )
    )

    return {
        "initial_temperature_c":
            initial_temperature_c,

        "steam_temperature_c":
            steam_temperature_c,

        "heated_temperature_c":
            heated_temperature,

        "production_start_temperature_c":
            production_start_temperature,

        "injection_days":
            injection_days,

        "soak_days":
            soak_days,

        "steam_volume_m3":
            steam_volume_m3
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("================================================")
    print("       BAGHEWALA CSS THERMAL MODEL V2")
    print("================================================")

    injection_days_list = [
        14.0,
        17.0,
        21.0
    ]

    for days in injection_days_list:

        result = simulate_css_cycle(
            initial_temperature_c=47.0,
            steam_temperature_c=285.0,
            steam_volume_m3=500.0,
            injection_days=days,
            soak_days=7.0
        )

        print(
            f"\nInjection: {days:.0f} days"
        )

        print(
            f"Heated temperature: "
            f"{result['heated_temperature_c']:.2f} °C"
        )

        print(
            f"Production temperature: "
            f"{result['production_start_temperature_c']:.2f} °C"
        )

    print("\n================================================")
    print("       THERMAL MODEL V2 COMPLETE")
    print("================================================")
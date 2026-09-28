import numpy as np


# ============================================================
# VFD / SRP SPEED MODEL
# ============================================================

# Typical prototype operating range
MIN_VFD_FREQUENCY_HZ = 20.0
MAX_VFD_FREQUENCY_HZ = 60.0

# Reference relationship
REFERENCE_VFD_FREQUENCY_HZ = 50.0
REFERENCE_SPM = 5.0


def calculate_spm_from_vfd(
    vfd_frequency_hz,
    reference_frequency_hz=REFERENCE_VFD_FREQUENCY_HZ,
    reference_spm=REFERENCE_SPM
):
    """
    Convert VFD frequency to SRP pumping speed.

    Prototype assumption:
        SPM changes approximately linearly with VFD frequency.

    Example:
        50 Hz -> 5.0 SPM
        40 Hz -> 4.0 SPM
        60 Hz -> 6.0 SPM
    """

    if vfd_frequency_hz < MIN_VFD_FREQUENCY_HZ:
        raise ValueError(
            f"VFD frequency cannot be below "
            f"{MIN_VFD_FREQUENCY_HZ} Hz."
        )

    if vfd_frequency_hz > MAX_VFD_FREQUENCY_HZ:
        raise ValueError(
            f"VFD frequency cannot exceed "
            f"{MAX_VFD_FREQUENCY_HZ} Hz."
        )

    if reference_frequency_hz <= 0:
        raise ValueError(
            "Reference VFD frequency must be positive."
        )

    if reference_spm <= 0:
        raise ValueError(
            "Reference SPM must be positive."
        )

    spm = (
        vfd_frequency_hz
        / reference_frequency_hz
        * reference_spm
    )

    return float(spm)


def calculate_vfd_frequency_from_spm(
    spm,
    reference_frequency_hz=REFERENCE_VFD_FREQUENCY_HZ,
    reference_spm=REFERENCE_SPM
):
    """
    Convert desired SRP speed (SPM) back to VFD frequency.
    """

    if spm < 0:
        raise ValueError(
            "SPM cannot be negative."
        )

    if reference_frequency_hz <= 0:
        raise ValueError(
            "Reference VFD frequency must be positive."
        )

    if reference_spm <= 0:
        raise ValueError(
            "Reference SPM must be positive."
        )

    vfd_frequency_hz = (
        spm
        / reference_spm
        * reference_frequency_hz
    )

    if not (
        MIN_VFD_FREQUENCY_HZ
        <= vfd_frequency_hz
        <= MAX_VFD_FREQUENCY_HZ
    ):
        raise ValueError(
            "Calculated VFD frequency is outside "
            "the supported operating range."
        )

    return float(vfd_frequency_hz)


def calculate_vfd_power_factor(
    vfd_frequency_hz
):
    """
    Prototype normalized VFD energy factor.

    Higher pumping speed requires more motor/pumping energy.
    This is an engineering proxy, not measured electrical power.
    """

    if not (
        MIN_VFD_FREQUENCY_HZ
        <= vfd_frequency_hz
        <= MAX_VFD_FREQUENCY_HZ
    ):
        raise ValueError(
            "VFD frequency is outside the supported range."
        )

    normalized_frequency = (
        vfd_frequency_hz
        / REFERENCE_VFD_FREQUENCY_HZ
    )

    # Approximate cubic relationship for rotating equipment
    power_factor = normalized_frequency ** 3

    return float(power_factor)


def evaluate_vfd_setting(
    vfd_frequency_hz
):
    """
    Return the complete VFD operating state.
    """

    spm = calculate_spm_from_vfd(
        vfd_frequency_hz
    )

    power_factor = calculate_vfd_power_factor(
        vfd_frequency_hz
    )

    return {
        "vfd_frequency_hz": float(vfd_frequency_hz),
        "spm": spm,
        "power_factor": power_factor
    }
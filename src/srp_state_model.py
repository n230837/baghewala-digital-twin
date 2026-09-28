# ============================================================
# BAGHEWALA DIGITAL TWIN
# SRP OPERATING STATE MODEL V3
# ============================================================
#
# SRP state estimation using:
#
#   1. Observed external SRP SPM envelope
#   2. Moderate viscosity adjustment
#
# IMPORTANT:
# The observed envelope is from an external SRP dataset.
# It is NOT Baghewala field data.
#
# Therefore this is an observationally constrained
# prototype model, NOT a Baghewala field calibration.
# ============================================================


# ============================================================
# REFERENCE PARAMETERS
# ============================================================

REFERENCE_VISCOSITY_CP = 5000.0

REFERENCE_AVERAGE_ROD_WEIGHT_KG = 4000.0

DYNAMOMETER_SCALE = 12.0

MIN_LOAD_RANGE_KG = 100.0

MAX_LOAD_RANGE_KG = 8000.0


# ============================================================
# OBSERVED SRP LOAD ENVELOPE
# ============================================================
#
# Median rod-load range from the external SRP dataset.
#
# These values are observational references, NOT Baghewala
# operating limits.
# ============================================================

OBSERVED_LOAD_MEDIANS = {

    "0-2": 4510.20,

    "2-3": 493.51,

    "3-4": 390.58,

    "4-5": 1342.95,

    "5-6": 1279.52,

    "6-7": 1002.51,

    "7-8": 856.38
}


# ============================================================
# FIND SPM BIN
# ============================================================

def get_spm_bin(spm):
    """
    Determine the observed SPM bin.
    """

    if 0 <= spm < 2:
        return "0-2"

    elif 2 <= spm < 3:
        return "2-3"

    elif 3 <= spm < 4:
        return "3-4"

    elif 4 <= spm < 5:
        return "4-5"

    elif 5 <= spm < 6:
        return "5-6"

    elif 6 <= spm < 7:
        return "6-7"

    elif 7 <= spm < 8:
        return "7-8"

    return None


# ============================================================
# ESTIMATE SRP STATE
# ============================================================

def estimate_srp_state(
    viscosity_cp,
    spm
):
    """
    Estimate a prototype SRP operating state.

    The model starts from the observed external SRP
    load behavior for the candidate SPM range.

    A moderated viscosity adjustment is then applied.

    This avoids assuming that rod load increases
    linearly with SPM.
    """

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if viscosity_cp <= 0:
        raise ValueError(
            "Viscosity must be positive."
        )

    if spm <= 0:
        raise ValueError(
            "SPM must be positive."
        )

    # --------------------------------------------------------
    # FIND OBSERVED SPM BIN
    # --------------------------------------------------------

    spm_bin = get_spm_bin(spm)

    if spm_bin is None:

        raise ValueError(
            "SPM is outside the observed "
            "0-8 SPM reference envelope."
        )

    # --------------------------------------------------------
    # OBSERVED BASELINE
    # --------------------------------------------------------

    baseline_load_range = (
        OBSERVED_LOAD_MEDIANS[spm_bin]
    )

    # --------------------------------------------------------
    # VISCOSITY FACTOR
    # --------------------------------------------------------
    #
    # Instead of:
    #
    #     load ∝ viscosity
    #
    # we use a square-root relationship.
    #
    # This makes viscosity influence the estimate
    # without dominating the observed SPM behavior.
    # --------------------------------------------------------

    viscosity_ratio = (
        viscosity_cp
        / REFERENCE_VISCOSITY_CP
    )

    viscosity_factor = (
        viscosity_ratio ** 0.5
    )

    # --------------------------------------------------------
    # ESTIMATED LOAD
    # --------------------------------------------------------

    estimated_load_range = (
        baseline_load_range
        * viscosity_factor
    )

    # --------------------------------------------------------
    # BOUNDS
    # --------------------------------------------------------

    estimated_load_range = max(
        MIN_LOAD_RANGE_KG,
        min(
            estimated_load_range,
            MAX_LOAD_RANGE_KG
        )
    )

    # --------------------------------------------------------
    # ROD WEIGHTS
    # --------------------------------------------------------

    average_rod_weight = (
        REFERENCE_AVERAGE_ROD_WEIGHT_KG
    )

    min_rod_weight = (
        average_rod_weight
        - estimated_load_range / 2.0
    )

    max_rod_weight = (
        average_rod_weight
        + estimated_load_range / 2.0
    )

    # --------------------------------------------------------
    # DYNAMOMETER AREA
    # --------------------------------------------------------

    dynamometer_area = (
        estimated_load_range
        * DYNAMOMETER_SCALE
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "viscosity_cp":
            viscosity_cp,

        "spm":
            spm,

        "spm_bin":
            spm_bin,

        "baseline_load_range":
            baseline_load_range,

        "viscosity_ratio":
            viscosity_ratio,

        "viscosity_factor":
            viscosity_factor,

        "estimated_load_range":
            estimated_load_range,

        "estimated_min_rod_weight":
            min_rod_weight,

        "estimated_max_rod_weight":
            max_rod_weight,

        "estimated_dynamometer_area":
            dynamometer_area
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("================================================")
    print("       SRP OPERATING STATE MODEL V3")
    print("================================================")

    test_viscosity = 7758.94

    test_spm_values = [
        3.5,
        4.0,
        4.5,
        5.0,
        5.5,
        6.0,
        6.5,
        7.0,
        7.5
    ]

    print(
        f"\nTest viscosity: "
        f"{test_viscosity:.2f} cP"
    )

    print(
        "\nSPM    BIN     BASELINE     "
        "ESTIMATED LOAD"
    )

    print(
        "-------------------------------------------"
    )

    for spm in test_spm_values:

        result = estimate_srp_state(
            viscosity_cp=test_viscosity,
            spm=spm
        )

        print(
            f"{spm:<6.1f}"
            f"{result['spm_bin']:<8}"
            f"{result['baseline_load_range']:<13.2f}"
            f"{result['estimated_load_range']:.2f} kg"
        )

    print("\n================================================")
    print("       SRP STATE MODEL V3 COMPLETE")
    print("================================================")
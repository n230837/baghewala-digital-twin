# ============================================================
# BAGHEWALA DIGITAL TWIN
# SRP CALIBRATION / CONSTRAINT LAYER
# ============================================================
#
# Purpose:
# Constrain the physics-informed SRP state estimate using
# an external observed SRP operating envelope.
#
# IMPORTANT:
# The calibration dataset is NOT Baghewala data.
# It is an external SRP observational dataset.
#
# This layer is therefore a prototype constraint mechanism,
# not a Baghewala field calibration.
# ============================================================


import pandas as pd


# ============================================================
# DATA
# ============================================================

DATA_PATH = "data/srp_operating_envelope.csv"


# ============================================================
# LOAD OBSERVED ENVELOPE
# ============================================================

def load_srp_envelope():

    envelope = pd.read_csv(
        DATA_PATH
    )

    return envelope


# ============================================================
# FIND SPM RANGE
# ============================================================

def find_spm_range(
    spm,
    envelope
):
    """
    Find the observed SPM range containing the
    requested pumping speed.
    """

    for _, row in envelope.iterrows():

        lower, upper = (
            str(row["SPM_range"])
            .split("-")
        )

        lower = float(lower)
        upper = float(upper)

        if lower <= spm < upper:

            return row

    return None


# ============================================================
# CONSTRAIN LOAD RANGE
# ============================================================

def constrain_load_range(
    estimated_load_range,
    spm,
    envelope
):
    """
    Compare the prototype estimated rod-load range
    against the observed SRP envelope.

    We do NOT directly replace the model prediction.

    Instead, the observed envelope is used to identify
    whether the estimate is inside or outside the
    observed operating behavior.
    """

    row = find_spm_range(
        spm,
        envelope
    )

    if row is None:

        return {
            "original_load_range": estimated_load_range,
            "reference_load_range": None,
            "load_deviation_percent": None,
            "constraint_status": "OUTSIDE OBSERVED SPM RANGE"
        }

    reference_load_range = float(
        row["median_rod_load_range"]
    )

    if reference_load_range <= 0:

        return {
            "original_load_range": estimated_load_range,
            "reference_load_range": reference_load_range,
            "load_deviation_percent": None,
            "constraint_status": "INVALID REFERENCE"
        }

    deviation_percent = (
        (
            estimated_load_range
            - reference_load_range
        )
        / reference_load_range
    ) * 100.0

    # --------------------------------------------------------
    # Prototype constraint classification
    # --------------------------------------------------------

    absolute_deviation = abs(
        deviation_percent
    )

    if absolute_deviation <= 50:

        status = "CONSISTENT WITH OBSERVED ENVELOPE"

    elif absolute_deviation <= 100:

        status = "MODERATE DEVIATION"

    else:

        status = "LARGE DEVIATION"

    return {

        "original_load_range":
            estimated_load_range,

        "reference_load_range":
            reference_load_range,

        "load_deviation_percent":
            deviation_percent,

        "constraint_status":
            status
    }


# ============================================================
# FULL CALIBRATION CHECK
# ============================================================

def calibrate_srp_state(
    viscosity_cp,
    spm,
    estimated_load_range
):
    """
    Perform a calibration/constraint check on an
    estimated SRP operating state.
    """

    envelope = load_srp_envelope()

    constraint = constrain_load_range(
        estimated_load_range=
            estimated_load_range,

        spm=spm,

        envelope=envelope
    )

    return {

        "viscosity_cp":
            viscosity_cp,

        "spm":
            spm,

        **constraint
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("================================================")
    print("       SRP CALIBRATION / CONSTRAINT")
    print("================================================")

    envelope = load_srp_envelope()

    print("\nObserved SRP envelope loaded.")

    print(
        f"SPM ranges available: "
        f"{len(envelope)}"
    )

    # --------------------------------------------------------
    # Test cases
    # --------------------------------------------------------

    test_cases = [

        {
            "viscosity_cp": 7758.94,
            "spm": 4.0,
            "load_range": 1939.73
        },

        {
            "viscosity_cp": 5000.0,
            "spm": 4.0,
            "load_range": 1250.0
        },

        {
            "viscosity_cp": 3000.0,
            "spm": 3.5,
            "load_range": 656.25
        },

        {
            "viscosity_cp": 1800.0,
            "spm": 3.5,
            "load_range": 393.75
        }
    ]

    for case in test_cases:

        result = calibrate_srp_state(
            viscosity_cp=
                case["viscosity_cp"],

            spm=
                case["spm"],

            estimated_load_range=
                case["load_range"]
        )

        print("\n--------------------------------")
        print(
            f"Viscosity : "
            f"{result['viscosity_cp']:.2f} cP"
        )

        print(
            f"SPM       : "
            f"{result['spm']:.2f}"
        )

        print(
            f"Estimated load : "
            f"{result['original_load_range']:.2f} kg"
        )

        if result["reference_load_range"] is not None:

            print(
                f"Observed median : "
                f"{result['reference_load_range']:.2f} kg"
            )

            print(
                f"Deviation : "
                f"{result['load_deviation_percent']:.2f}%"
            )

        print(
            f"Status : "
            f"{result['constraint_status']}"
        )

    print("\n================================================")
    print("       SRP CALIBRATION COMPLETE")
    print("================================================")
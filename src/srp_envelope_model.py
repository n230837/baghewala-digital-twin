# ============================================================
# BAGHEWALA DIGITAL TWIN
# SRP OPERATING ENVELOPE MODEL
# ============================================================

import pandas as pd


DATA_PATH = "data/srp_operating_envelope.csv"


def load_operating_envelope():
    """
    Load the SRP operating envelope derived from
    the external NK Field SRP dataset.
    """

    return pd.read_csv(DATA_PATH)


def evaluate_spm(spm, envelope):
    """
    Evaluate an SPM value against the observed SRP envelope.

    IMPORTANT:
    This is an observational constraint from the external
    NK Field dataset.

    It is NOT a Baghewala operating limit.
    """

    selected_row = None

    for _, row in envelope.iterrows():

        # Example:
        # "4-5" -> lower = 4, upper = 5

        lower, upper = str(
            row["SPM_range"]
        ).split("-")

        lower = float(lower)
        upper = float(upper)

        if lower <= spm < upper:
            selected_row = row
            break

    if selected_row is None:

        return {
            "spm": spm,
            "status": "OUTSIDE OBSERVED ENVELOPE"
        }

    return {
        "spm": spm,
        "status": "INSIDE OBSERVED ENVELOPE",

        "spm_range": str(
            selected_row["SPM_range"]
        ),

        "observations": int(
            selected_row["observations"]
        ),

        "average_pump_fillage": float(
            selected_row["avg_pump_fillage"]
        ),

        "high_load_rate": float(
            selected_row["high_load_rate"]
        ),

        "low_fillage_rate": float(
            selected_row["low_fillage_rate"]
        )
    }


if __name__ == "__main__":

    print("================================================")
    print("       SRP OPERATING ENVELOPE")
    print("================================================")

    envelope = load_operating_envelope()

    test_spm = [
        3.5,
        4.0,
        4.5,
        5.5,
        6.5,
        7.2
    ]

    for spm in test_spm:

        result = evaluate_spm(
            spm,
            envelope
        )

        print("\nSPM:", spm)
        print("Status:", result["status"])

        if "spm_range" in result:

            print(
                "Observed range:",
                result["spm_range"]
            )

            print(
                "Observations:",
                result["observations"]
            )

            print(
                f"Average pump fillage: "
                f"{result['average_pump_fillage']:.2f}%"
            )

            print(
                f"High-load rate: "
                f"{result['high_load_rate']:.2f}%"
            )

            print(
                f"Low-fillage rate: "
                f"{result['low_fillage_rate']:.2f}%"
            )

    print("\n================================================")
    print("       SRP ENVELOPE MODEL COMPLETE")
    print("================================================")
    
# ============================================================
# BAGHEWALA DIGITAL TWIN
# SRP CANDIDATE OPERATING SCORE
# ============================================================

from srp_envelope_model import (
    load_operating_envelope,
    evaluate_spm
)


def calculate_candidate_score(
    predicted_fillage,
    high_load_rate,
    low_fillage_rate
):
    """
    Calculate a transparent SRP candidate score.

    This is a prototype decision-support score.
    It is NOT a physical failure probability and is
    NOT calibrated to Baghewala.

    Higher score = better balance between:
        - pump fillage
        - lower high-load observations
        - lower low-fillage observations
    """

    fillage_component = predicted_fillage / 100.0

    load_component = (
        1.0 - high_load_rate / 100.0
    )

    low_fillage_component = (
        1.0 - low_fillage_rate / 100.0
    )

    score = (
        0.50 * fillage_component
        + 0.25 * load_component
        + 0.25 * low_fillage_component
    )

    return max(0.0, min(score, 1.0))


def evaluate_candidate(
    spm,
    predicted_fillage,
    envelope
):
    """
    Evaluate one candidate SPM.
    """

    envelope_result = evaluate_spm(
        spm,
        envelope
    )

    if envelope_result["status"] != (
        "INSIDE OBSERVED ENVELOPE"
    ):
        return {
            "spm": spm,
            "status": "OUTSIDE OBSERVED ENVELOPE"
        }

    score = calculate_candidate_score(
        predicted_fillage=predicted_fillage,
        high_load_rate=envelope_result[
            "high_load_rate"
        ],
        low_fillage_rate=envelope_result[
            "low_fillage_rate"
        ]
    )

    return {
        "spm": spm,
        "status": envelope_result["status"],
        "observed_range": envelope_result["spm_range"],
        "predicted_fillage": predicted_fillage,
        "high_load_rate": envelope_result[
            "high_load_rate"
        ],
        "low_fillage_rate": envelope_result[
            "low_fillage_rate"
        ],
        "score": score
    }


if __name__ == "__main__":

    print("================================================")
    print("       SRP CANDIDATE SCORE")
    print("================================================")

    envelope = load_operating_envelope()

    candidates = [
        (3.5, 45.0),
        (4.0, 75.0),
        (4.5, 78.0),
        (5.0, 70.0),
        (5.5, 60.0),
        (6.0, 45.0),
        (6.5, 35.0)
    ]

    for spm, fillage in candidates:

        result = evaluate_candidate(
            spm=spm,
            predicted_fillage=fillage,
            envelope=envelope
        )

        print(f"\nSPM: {spm:.1f}")

        if result["status"] == (
            "INSIDE OBSERVED ENVELOPE"
        ):

            print(
                f"Predicted fillage : "
                f"{result['predicted_fillage']:.2f}%"
            )

            print(
                f"High-load rate    : "
                f"{result['high_load_rate']:.2f}%"
            )

            print(
                f"Low-fillage rate  : "
                f"{result['low_fillage_rate']:.2f}%"
            )

            print(
                f"Operating score   : "
                f"{result['score']:.3f}"
            )

        else:

            print(
                "Outside observed envelope"
            )

    print("\n================================================")
    print("       SRP CANDIDATE SCORE COMPLETE")
    print("================================================")
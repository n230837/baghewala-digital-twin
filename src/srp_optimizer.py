# ============================================================
# BAGHEWALA DIGITAL TWIN
# SRP OPTIMIZER V4
# ============================================================

from srp_envelope_model import load_operating_envelope
from srp_envelope_model import evaluate_spm
from srp_candidate_predictor import predict_candidate


def optimize_srp(
    well_id,
    viscosity_cp,
    candidate_spm_values
):

    envelope = load_operating_envelope()

    results = []

    for spm in candidate_spm_values:

        # Predict SRP operating state
        prediction = predict_candidate(
            well_id=well_id,
            viscosity_cp=viscosity_cp,
            spm=spm
        )

        # Check observed operating envelope
        envelope_result = evaluate_spm(
            spm,
            envelope
        )

        if envelope_result["status"] != "INSIDE OBSERVED ENVELOPE":
            continue

        # ====================================================
        # SCORE
        # ====================================================

        fillage_score = (
            prediction["predicted_pump_fillage"]
            / 100.0
        )

        load_score = (
            1.0
            - envelope_result["high_load_rate"]
            / 100.0
        )

        low_fillage_score = (
            1.0
            - envelope_result["low_fillage_rate"]
            / 100.0
        )

        score = (
            0.50 * fillage_score
            + 0.25 * load_score
            + 0.25 * low_fillage_score
        )

        # ====================================================
        # STORE RESULT
        # ====================================================

        result = {
            "spm": spm,

            # ML prediction
            "predicted_fillage":
                prediction["predicted_pump_fillage"],

            # SRP state estimate
            "state_load_range":
                prediction["state_load_range"],

            # Compatibility key for downstream reliability
            "rod_load_range":
                prediction["state_load_range"],

            "estimated_min_rod_weight":
                prediction["estimated_min_rod_weight"],

            "estimated_max_rod_weight":
                prediction["estimated_max_rod_weight"],

            "estimated_dynamometer_area":
                prediction["estimated_dynamometer_area"],

            # Observed envelope
            "high_load_rate":
                envelope_result["high_load_rate"],

            "low_fillage_rate":
                envelope_result["low_fillage_rate"],

            "envelope_observations":
                envelope_result["observations"],

            # Calibration
            "reference_load_range":
                prediction["reference_load_range"],

            "load_deviation_percent":
                prediction["load_deviation_percent"],

            "calibration_status":
                prediction["calibration_status"],

            # Model validation
            "model_mae_percent":
                prediction["model_mae_percent"],

            "model_r2":
                prediction["model_r2"],

            "model_confidence":
                prediction["model_confidence"],

            # Final score
            "score": score
        }

        results.append(result)

    # Sort highest score first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("================================================")
    print("          BAGHEWALA SRP OPTIMIZER")
    print("================================================")

    viscosity = 7758.94

    candidates = [
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

    results = optimize_srp(
        well_id="NK-68",
        viscosity_cp=viscosity,
        candidate_spm_values=candidates
    )

    print()
    print(f"Viscosity: {viscosity:.2f} cP")
    print()

    if not results:

        print("No valid SRP candidates found.")

    else:

        print(
            f"{'SPM':<8}"
            f"{'Fillage':<12}"
            f"{'Load':<12}"
            f"{'HighLoad':<12}"
            f"{'LowFill':<12}"
            f"{'Score':<10}"
        )

        print("-" * 66)

        for result in results:

            print(
                f"{result['spm']:<8.2f}"
                f"{result['predicted_fillage']:<12.2f}"
                f"{result['state_load_range']:<12.2f}"
                f"{result['high_load_rate']:<12.2f}"
                f"{result['low_fillage_rate']:<12.2f}"
                f"{result['score']:<10.3f}"
            )

        # ====================================================
        # TOP CANDIDATE
        # ====================================================

        best = results[0]

        print()
        print("================================================")
        print("              TOP SRP CANDIDATE")
        print("================================================")

        print(
            f"SPM:                 {best['spm']:.2f}"
        )

        print(
            f"Predicted fillage:   "
            f"{best['predicted_fillage']:.2f}%"
        )

        print(
            f"State load range:    "
            f"{best['state_load_range']:.2f} kg"
        )

        print(
            f"Reference load:      "
            f"{best['reference_load_range']:.2f} kg"
        )

        print(
            f"Load deviation:      "
            f"{best['load_deviation_percent']:.2f}%"
        )

        print(
            f"Calibration:         "
            f"{best['calibration_status']}"
        )

        print(
            f"High-load rate:      "
            f"{best['high_load_rate']:.2f}%"
        )

        print(
            f"Low-fillage rate:    "
            f"{best['low_fillage_rate']:.2f}%"
        )

        print(
            f"Operating score:     "
            f"{best['score']:.3f}"
        )

        print(
            f"Model MAE:           "
            f"{best['model_mae_percent']:.2f} "
            f"percentage points"
        )

        print(
            f"Model R²:            "
            f"{best['model_r2']:.3f}"
        )

        print(
            f"Model confidence:    "
            f"{best['model_confidence']}"
        )

    print()
    print("================================================")
    print("             SRP OPTIMIZER COMPLETE")
    print("================================================")
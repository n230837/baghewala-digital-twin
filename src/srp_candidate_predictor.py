# ============================================================
# BAGHEWALA DIGITAL TWIN
# SRP CANDIDATE PREDICTOR V4
# ============================================================
#
# Pipeline:
#
# Viscosity
#     ↓
# SRP state model
#     ↓
# ML pump-fillage prediction
#     ↓
# External SRP envelope calibration
#     ↓
# Model validation metadata
#
# IMPORTANT:
# The external SRP dataset is NOT Baghewala data.
# It is used as an observational reference.
# ============================================================


from srp_state_model import estimate_srp_state

from srp_predictor import predict_srp

from srp_calibration import calibrate_srp_state


# ============================================================
# MODEL VALIDATION METADATA
# ============================================================

MODEL_MAE_PERCENT = 18.06

MODEL_R2 = 0.473

MODEL_CONFIDENCE = "MODERATE / PROTOTYPE"

MODEL_VALIDATION_TYPE = (
    "Chronological held-out test"
)


# ============================================================
# PREDICT CANDIDATE
# ============================================================

def predict_candidate(
    well_id,
    viscosity_cp,
    spm
):
    """
    Generate a complete SRP candidate state.

    ML prediction:
        Pump fillage

    Prototype state:
        Rod load
        Rod weights
        Dynamometer signal

    Calibration:
        Comparison with external SRP envelope

    Validation:
        Chronological ML model performance
    """

    # ========================================================
    # 1. SRP STATE MODEL
    # ========================================================

    state = estimate_srp_state(
        viscosity_cp=viscosity_cp,
        spm=spm
    )

    # ========================================================
    # 2. ML PUMP-FILLAGE PREDICTION
    # ========================================================

    prediction = predict_srp(

        well_id=well_id,

        spm=spm,

        min_rod_weight=
            state[
                "estimated_min_rod_weight"
            ],

        max_rod_weight=
            state[
                "estimated_max_rod_weight"
            ],

        dynamometer_area=
            state[
                "estimated_dynamometer_area"
            ]
    )

    # ========================================================
    # 3. CALIBRATION
    # ========================================================

    calibration = calibrate_srp_state(

        viscosity_cp=viscosity_cp,

        spm=spm,

        estimated_load_range=
            state[
                "estimated_load_range"
            ]
    )

    # ========================================================
    # 4. COMBINED RESULT
    # ========================================================

    result = {

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        "well_id":
            well_id,

        "viscosity_cp":
            viscosity_cp,

        "spm":
            spm,

        # ----------------------------------------------------
        # SRP STATE
        # ----------------------------------------------------

        "spm_bin":
            state[
                "spm_bin"
            ],

        "baseline_load_range":
            state[
                "baseline_load_range"
            ],

        "viscosity_factor":
            state[
                "viscosity_factor"
            ],

        "state_load_range":
            state[
                "estimated_load_range"
            ],

        "estimated_min_rod_weight":
            state[
                "estimated_min_rod_weight"
            ],

        "estimated_max_rod_weight":
            state[
                "estimated_max_rod_weight"
            ],

        "estimated_dynamometer_area":
            state[
                "estimated_dynamometer_area"
            ],

        # ----------------------------------------------------
        # ACTUAL ML OUTPUT
        # ----------------------------------------------------

        "predicted_pump_fillage":
            prediction[
                "predicted_pump_fillage"
            ],

        # ----------------------------------------------------
        # CALIBRATION
        # ----------------------------------------------------

        "reference_load_range":
            calibration[
                "reference_load_range"
            ],

        "load_deviation_percent":
            calibration[
                "load_deviation_percent"
            ],

        "calibration_status":
            calibration[
                "constraint_status"
            ],

        # ----------------------------------------------------
        # MODEL VALIDATION
        # ----------------------------------------------------

        "model_mae_percent":
            MODEL_MAE_PERCENT,

        "model_r2":
            MODEL_R2,

        "model_confidence":
            MODEL_CONFIDENCE,

        "model_validation_type":
            MODEL_VALIDATION_TYPE
    }

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("================================================")
    print("       SRP CANDIDATE PREDICTOR V4")
    print("================================================")

    result = predict_candidate(

        well_id="NK-68",

        viscosity_cp=7758.94,

        spm=4.0
    )

    # ========================================================
    # INPUT
    # ========================================================

    print("\nINPUT")
    print("--------------------------------")

    print(
        f"Well ID       : "
        f"{result['well_id']}"
    )

    print(
        f"Viscosity     : "
        f"{result['viscosity_cp']:.2f} cP"
    )

    print(
        f"SPM           : "
        f"{result['spm']:.2f}"
    )

    # ========================================================
    # SRP STATE
    # ========================================================

    print("\nSRP STATE")
    print("--------------------------------")

    print(
        f"SPM bin              : "
        f"{result['spm_bin']}"
    )

    print(
        f"Observed baseline    : "
        f"{result['baseline_load_range']:.2f} kg"
    )

    print(
        f"State load range     : "
        f"{result['state_load_range']:.2f} kg"
    )

    print(
        f"Minimum rod weight  : "
        f"{result['estimated_min_rod_weight']:.2f} kg"
    )

    print(
        f"Maximum rod weight  : "
        f"{result['estimated_max_rod_weight']:.2f} kg"
    )

    print(
        f"Dynamometer area    : "
        f"{result['estimated_dynamometer_area']:.2f}"
    )

    # ========================================================
    # ML OUTPUT
    # ========================================================

    print("\nML OUTPUT")
    print("--------------------------------")

    print(
        f"Predicted pump fillage : "
        f"{result['predicted_pump_fillage']:.2f}%"
    )

    # ========================================================
    # CALIBRATION
    # ========================================================

    print("\nCALIBRATION")
    print("--------------------------------")

    print(
        f"Reference load      : "
        f"{result['reference_load_range']:.2f} kg"
    )

    print(
        f"Load deviation      : "
        f"{result['load_deviation_percent']:.2f}%"
    )

    print(
        f"Calibration status   : "
        f"{result['calibration_status']}"
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    print("\nMODEL VALIDATION")
    print("--------------------------------")

    print(
        f"Validation type : "
        f"{result['model_validation_type']}"
    )

    print(
        f"MAE             : "
        f"{result['model_mae_percent']:.2f} "
        f"percentage points"
    )

    print(
        f"R²              : "
        f"{result['model_r2']:.3f}"
    )

    print(
        f"Confidence      : "
        f"{result['model_confidence']}"
    )

    print("\n================================================")
    print("       SRP CANDIDATE PREDICTOR COMPLETE")
    print("================================================")
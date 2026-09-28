# ============================================================
# BAGHEWALA DIGITAL TWIN
# INTEGRATED CSS + SRP OPTIMIZER V2
# ============================================================

from css_optimizer import generate_css_candidates
from viscosity_model_v2 import calculate_viscosity
from srp_optimizer import optimize_srp
from production_model_v2 import calculate_production_rate


def run_integrated_optimization(
    well_id,
    candidate_spm_values
):
    """
    Integrated CSS + SRP optimization.

    CSS:
        Steam parameters
             ↓
        Thermal response
             ↓
        Production temperature
             ↓
        Oil viscosity

    SRP:
        Viscosity
             ↓
        Candidate SPM
             ↓
        Pump fillage
             ↓
        SRP operating state

    Production:
        Viscosity + pump fillage
             ↓
        Predicted production

    IMPORTANT:
    This is a prototype digital-twin integration.
    It is NOT calibrated for field deployment.
    """

    # ========================================================
    # 1. GENERATE CSS CANDIDATES
    # ========================================================

    css_candidates = generate_css_candidates()

    results = []

    # ========================================================
    # 2. LOOP THROUGH CSS SCENARIOS
    # ========================================================

    for css in css_candidates:

        # ----------------------------------------------------
        # Production-start temperature
        # ----------------------------------------------------

        production_temperature = (
            css["production_start_temperature_c"]
        )

        # ----------------------------------------------------
        # Temperature → viscosity
        # ----------------------------------------------------

        viscosity = calculate_viscosity(
            production_temperature
        )

        # ----------------------------------------------------
        # Optimize SRP at this viscosity
        # ----------------------------------------------------

        srp_results = optimize_srp(
            well_id=well_id,
            viscosity_cp=viscosity,
            candidate_spm_values=candidate_spm_values
        )

        if not srp_results:
            continue

        # ====================================================
        # 3. LOOP THROUGH SRP CANDIDATES
        # ====================================================

        for srp in srp_results:

            # ------------------------------------------------
            # Viscosity + pump fillage → production
            # ------------------------------------------------

            production = calculate_production_rate(
                viscosity_cp=viscosity,
                pump_fillage_percent=
                    srp["predicted_fillage"]
            )

            # ------------------------------------------------
            # Store complete integrated result
            # ------------------------------------------------

            results.append({

                # ============================================
                # CSS PARAMETERS
                # ============================================

                "steam_temperature_c":
                    css["steam_temperature_c"],

                "steam_volume_m3":
                    css["steam_volume_m3"],

                "injection_days":
                    css["injection_days"],

                "soak_days":
                    css["soak_days"],

                # ============================================
                # THERMAL RESPONSE
                # ============================================

                "heated_temperature_c":
                    css["heated_temperature_c"],

                "production_temperature_c":
                    production_temperature,

                # ============================================
                # FLUID RESPONSE
                # ============================================

                "viscosity_cp":
                    viscosity,

                # ============================================
                # SRP OPERATING POINT
                # ============================================

                "spm":
                    srp["spm"],

                "pump_fillage_percent":
                    srp["predicted_fillage"],

                # State-model estimate
                "state_load_range":
                    srp["state_load_range"],

                # Compatibility key for downstream modules
                "rod_load_range":
                    srp["rod_load_range"],

                "estimated_min_rod_weight":
                    srp["estimated_min_rod_weight"],

                "estimated_max_rod_weight":
                    srp["estimated_max_rod_weight"],

                "estimated_dynamometer_area":
                    srp["estimated_dynamometer_area"],

                # ============================================
                # SRP CALIBRATION
                # ============================================

                "reference_load_range":
                    srp["reference_load_range"],

                "load_deviation_percent":
                    srp["load_deviation_percent"],

                "calibration_status":
                    srp["calibration_status"],

                # ============================================
                # SRP OPERATING ENVELOPE
                # ============================================

                "high_load_rate":
                    srp["high_load_rate"],

                "low_fillage_rate":
                    srp["low_fillage_rate"],

                "envelope_observations":
                    srp["envelope_observations"],

                # ============================================
                # SRP OPERATING SCORE
                # ============================================

                "operating_score":
                    srp["score"],

                # ============================================
                # ML VALIDATION
                # ============================================

                "model_mae_percent":
                    srp["model_mae_percent"],

                "model_r2":
                    srp["model_r2"],

                "model_confidence":
                    srp["model_confidence"],

                # ============================================
                # PRODUCTION
                # ============================================

                "predicted_production_bpd":
                    production
            })

    # ========================================================
    # 4. SORT BY PREDICTED PRODUCTION
    # ========================================================

    results.sort(
        key=lambda x:
            x["predicted_production_bpd"],
        reverse=True
    )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("================================================")
    print("       INTEGRATED CSS + SRP OPTIMIZER")
    print("================================================")

    # --------------------------------------------------------
    # Candidate SPM values
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Run integrated optimization
    # --------------------------------------------------------

    results = run_integrated_optimization(
        well_id="NK-68",
        candidate_spm_values=candidates
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print(
        f"Total evaluated combinations: "
        f"{len(results)}"
    )

    print()
    print("TOP 10 COMBINATIONS")
    print("-------------------")

    # ========================================================
    # DISPLAY TOP 10
    # ========================================================

    for i, result in enumerate(
        results[:10],
        start=1
    ):

        print()
        print(f"#{i}")

        print(
            f"Steam temperature : "
            f"{result['steam_temperature_c']:.0f} °C"
        )

        print(
            f"Steam volume      : "
            f"{result['steam_volume_m3']:.0f} m³"
        )

        print(
            f"Injection         : "
            f"{result['injection_days']:.0f} days"
        )

        print(
            f"Soak              : "
            f"{result['soak_days']:.0f} days"
        )

        print(
            f"Heated temp.      : "
            f"{result['heated_temperature_c']:.2f} °C"
        )

        print(
            f"Production temp.  : "
            f"{result['production_temperature_c']:.2f} °C"
        )

        print(
            f"Viscosity         : "
            f"{result['viscosity_cp']:.2f} cP"
        )

        print(
            f"SPM               : "
            f"{result['spm']:.1f}"
        )

        print(
            f"Pump fillage      : "
            f"{result['pump_fillage_percent']:.2f}%"
        )

        print(
            f"State load range  : "
            f"{result['state_load_range']:.2f} kg"
        )

        print(
            f"Reference load    : "
            f"{result['reference_load_range']:.2f} kg"
        )

        print(
            f"Load deviation    : "
            f"{result['load_deviation_percent']:.2f}%"
        )

        print(
            f"Calibration       : "
            f"{result['calibration_status']}"
        )

        print(
            f"Operating score   : "
            f"{result['operating_score']:.3f}"
        )

        print(
            f"Production        : "
            f"{result['predicted_production_bpd']:.2f} BPD"
        )

    print()
    print("================================================")
    print("       INTEGRATED OPTIMIZATION COMPLETE")
    print("================================================")
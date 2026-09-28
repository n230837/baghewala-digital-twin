# ============================================================
# BAGHEWALA DIGITAL TWIN
# PRODUCTION OPTIMIZER
# ============================================================

from srp_optimizer import optimize_srp
from production_model_v2 import calculate_production_rate


def optimize_production(
    well_id,
    viscosity_cp,
    candidate_spm_values
):
    """
    Evaluate SRP candidates using predicted pump fillage
    and estimate production for each candidate.

    NOTE:
    Production model is currently a prototype and is NOT
    calibrated to Baghewala field production history.
    """

    # --------------------------------------------------------
    # 1. Run SRP optimizer
    # --------------------------------------------------------

    srp_results = optimize_srp(
        well_id=well_id,
        viscosity_cp=viscosity_cp,
        candidate_spm_values=candidate_spm_values
    )

    results = []

    # --------------------------------------------------------
    # 2. Convert pump fillage → production
    # --------------------------------------------------------

    for result in srp_results:

        production = calculate_production_rate(
            viscosity_cp=viscosity_cp,
            pump_fillage_percent=result[
                "predicted_fillage"
            ]
        )

        result_with_production = result.copy()

        result_with_production[
            "predicted_production_bpd"
        ] = production

        results.append(
            result_with_production
        )

    # --------------------------------------------------------
    # 3. Sort by predicted production
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x[
            "predicted_production_bpd"
        ],
        reverse=True
    )

    return results


if __name__ == "__main__":

    print("================================================")
    print("       PRODUCTION OPTIMIZER")
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

    results = optimize_production(
        well_id="NK-68",
        viscosity_cp=viscosity,
        candidate_spm_values=candidates
    )

    print("\nCANDIDATE RESULTS")
    print("-----------------")

    for result in results:

        print(
            f"\nSPM: "
            f"{result['spm']:.1f}"
        )

        print(
            f"Predicted pump fillage: "
            f"{result['predicted_fillage']:.2f}%"
        )

        print(
            f"Rod load range: "
            f"{result['rod_load_range']:.2f} kg"
        )

        print(
            f"Operating score: "
            f"{result['score']:.3f}"
        )

        print(
            f"Predicted production: "
            f"{result['predicted_production_bpd']:.2f} BPD"
        )

    print("\n================================================")
    print("       PRODUCTION OPTIMIZATION COMPLETE")
    print("================================================")
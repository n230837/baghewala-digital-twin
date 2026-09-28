# ============================================================
# BAGHEWALA DIGITAL TWIN
# MULTI-OBJECTIVE OPTIMIZER
# ============================================================

from production_optimizer import optimize_production


def calculate_total_score(
    production_bpd,
    operating_score,
    max_production_bpd
):
    """
    Combine production potential and SRP operating behavior.

    Prototype weights only.

    This is NOT a field-calibrated optimization objective.
    """

    if max_production_bpd <= 0:
        raise ValueError(
            "Maximum production must be positive."
        )

    # Normalize production
    production_score = (
        production_bpd / max_production_bpd
    )

    # Combined objective
    total_score = (
        0.60 * production_score
        + 0.40 * operating_score
    )

    return max(
        0.0,
        min(total_score, 1.0)
    )


def optimize_multi_objective(
    well_id,
    viscosity_cp,
    candidate_spm_values
):
    """
    Evaluate SRP candidates using both production
    and operating behavior.
    """

    results = optimize_production(
        well_id=well_id,
        viscosity_cp=viscosity_cp,
        candidate_spm_values=candidate_spm_values
    )

    if not results:
        return []

    max_production = max(
        result["predicted_production_bpd"]
        for result in results
    )

    for result in results:

        result["production_score"] = (
            result["predicted_production_bpd"]
            / max_production
        )

        result["total_score"] = (
            calculate_total_score(
                production_bpd=
                    result[
                        "predicted_production_bpd"
                    ],
                operating_score=
                    result["score"],
                max_production_bpd=
                    max_production
            )
        )

    results.sort(
        key=lambda x: x["total_score"],
        reverse=True
    )

    return results


if __name__ == "__main__":

    print("================================================")
    print("       MULTI-OBJECTIVE SRP OPTIMIZER")
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

    results = optimize_multi_objective(
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
            f"Production: "
            f"{result['predicted_production_bpd']:.2f} BPD"
        )

        print(
            f"Pump fillage: "
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
            f"Production score: "
            f"{result['production_score']:.3f}"
        )

        print(
            f"Total score: "
            f"{result['total_score']:.3f}"
        )

    print("\n================================================")
    print("       MULTI-OBJECTIVE OPTIMIZATION COMPLETE")
    print("================================================")
from integrated_reliability_optimizer import (
    run_reliability_optimization
)


# ============================================================
# THREE-OBJECTIVE PARETO OPTIMIZER
# ============================================================
#
# Objectives:
#
# 1. MAXIMIZE production
# 2. MINIMIZE steam energy
# 3. MINIMIZE SRP reliability risk
#
# No arbitrary weighting is used.
#
# IMPORTANT:
# Reliability risk is a prototype indicator,
# NOT a measured failure probability.
# ============================================================


# ============================================================
# RISK CLASS
# ============================================================

def classify_risk(risk):

    if risk < 30:
        return "LOW"

    elif risk < 60:
        return "MEDIUM"

    else:
        return "HIGH"


# ============================================================
# DOMINANCE CHECK
# ============================================================

def is_dominated(candidate, other):

    production_better_or_equal = (
        other["predicted_production_bpd"]
        >= candidate["predicted_production_bpd"]
    )

    energy_better_or_equal = (
        other["steam_energy_kwh"]
        <= candidate["steam_energy_kwh"]
    )

    risk_better_or_equal = (
        other["reliability_risk"]
        <= candidate["reliability_risk"]
    )

    strictly_better = (
        other["predicted_production_bpd"]
        > candidate["predicted_production_bpd"]
        or
        other["steam_energy_kwh"]
        < candidate["steam_energy_kwh"]
        or
        other["reliability_risk"]
        < candidate["reliability_risk"]
    )

    return (
        production_better_or_equal
        and energy_better_or_equal
        and risk_better_or_equal
        and strictly_better
    )


# ============================================================
# FIND PARETO FRONT
# ============================================================

def find_three_objective_pareto_front(results):

    pareto_results = []

    for candidate in results:

        dominated = False

        for other in results:

            if candidate is other:
                continue

            if is_dominated(candidate, other):

                dominated = True
                break

        if not dominated:

            pareto_results.append(candidate)

    return pareto_results


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("================================================")
    print("      THREE-OBJECTIVE PARETO OPTIMIZER")
    print("================================================")

    # --------------------------------------------------------
    # SPM candidates
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
    # RUN DIGITAL TWIN
    # --------------------------------------------------------

    results = run_reliability_optimization(
        well_id="NK-68",
        candidate_spm_values=candidates
    )

    print(
        f"\nTotal combinations evaluated: "
        f"{len(results)}"
    )

    # --------------------------------------------------------
    # FIND PARETO FRONT
    # --------------------------------------------------------

    pareto_results = find_three_objective_pareto_front(
        results
    )

    # Sort by production

    pareto_results.sort(
        key=lambda x:
        x["predicted_production_bpd"]
    )

    print("\nTHREE-OBJECTIVE PARETO FRONT")
    print("----------------------------")

    print(
        f"Number of Pareto scenarios: "
        f"{len(pareto_results)}"
    )

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    for i, result in enumerate(
        pareto_results,
        start=1
    ):

        risk = result["reliability_risk"]

        print(f"\n#{i}")

        print(
            f"Steam temperature : "
            f"{result['steam_temperature_c']:.1f} °C"
        )

        print(
            f"Steam volume      : "
            f"{result['steam_volume_m3']:.1f} m³"
        )

        print(
            f"Injection         : "
            f"{result['injection_days']:.1f} days"
        )

        print(
            f"Soak              : "
            f"{result['soak_days']:.1f} days"
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
            f"Rod load range    : "
            f"{result['rod_load_range']:.2f} kg"
        )

        print(
            f"Production        : "
            f"{result['predicted_production_bpd']:.2f} BPD"
        )

        print(
            f"Steam energy      : "
            f"{result['steam_energy_kwh']:.0f} kWh"
        )

        print(
            f"Production/Energy : "
            f"{result['production_per_energy']:.8f}"
        )

        print(
            f"Risk score        : "
            f"{risk:.2f}/100"
        )

        print(
            f"Risk class        : "
            f"{classify_risk(risk)}"
        )

    print("\n================================================")
    print("    THREE-OBJECTIVE OPTIMIZATION COMPLETE")
    print("================================================")
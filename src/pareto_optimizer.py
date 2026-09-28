from integrated_energy_optimizer import run_energy_optimization


# ============================================================
# CHECK WHETHER A SCENARIO IS DOMINATED
# ============================================================

def is_dominated(candidate, other):

    better_or_equal_production = (
        other["predicted_production_bpd"]
        >= candidate["predicted_production_bpd"]
    )

    lower_or_equal_energy = (
        other["steam_energy_kwh"]
        <= candidate["steam_energy_kwh"]
    )

    strictly_better = (
        other["predicted_production_bpd"]
        > candidate["predicted_production_bpd"]
        or
        other["steam_energy_kwh"]
        < candidate["steam_energy_kwh"]
    )

    return (
        better_or_equal_production
        and lower_or_equal_energy
        and strictly_better
    )


# ============================================================
# FIND PARETO FRONT
# ============================================================

def find_pareto_front(results):

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
# GET VALUE FROM POSSIBLE KEY NAMES
# ============================================================

def get_value(result, possible_keys, default=None):

    for key in possible_keys:

        if key in result:
            return result[key]

    return default


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("================================================")
    print("           PARETO OPTIMIZATION")
    print("================================================")

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

    results = run_energy_optimization(
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

    pareto_results = find_pareto_front(results)

    pareto_results.sort(
        key=lambda x: x["predicted_production_bpd"]
    )

    print("\nPARETO FRONT")
    print("------------")

    print(
        f"Number of Pareto scenarios: "
        f"{len(pareto_results)}"
    )

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    for i, result in enumerate(
        pareto_results,
        start=1
    ):

        print(f"\n#{i}")

        # ----------------------------------------------------
        # CSS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # THERMAL STATE
        # ----------------------------------------------------

        production_temperature = get_value(
            result,
            [
                "production_start_temperature_c",
                "production_temperature_c",
                "production_temp_c"
            ]
        )

        if production_temperature is not None:

            print(
                f"Production temp.  : "
                f"{production_temperature:.2f} °C"
            )

        # ----------------------------------------------------
        # VISCOSITY
        # ----------------------------------------------------

        viscosity = get_value(
            result,
            [
                "viscosity_cp"
            ]
        )

        if viscosity is not None:

            print(
                f"Viscosity         : "
                f"{viscosity:.2f} cP"
            )

        # ----------------------------------------------------
        # SRP
        # ----------------------------------------------------

        spm = get_value(
            result,
            [
                "spm"
            ]
        )

        print(
            f"SPM               : "
            f"{spm}"
        )

        pump_fillage = get_value(
            result,
            [
                "predicted_pump_fillage",
                "pump_fillage",
                "predicted_fillage"
            ]
        )

        if pump_fillage is not None:

            print(
                f"Pump fillage      : "
                f"{pump_fillage:.2f}%"
            )

        # ----------------------------------------------------
        # PRODUCTION
        # ----------------------------------------------------

        production = result[
            "predicted_production_bpd"
        ]

        print(
            f"Production        : "
            f"{production:.2f} BPD"
        )

        # ----------------------------------------------------
        # ENERGY
        # ----------------------------------------------------

        energy = result[
            "steam_energy_kwh"
        ]

        print(
            f"Steam energy      : "
            f"{energy:.0f} kWh"
        )

        # ----------------------------------------------------
        # EFFICIENCY
        # ----------------------------------------------------

        efficiency = result[
            "production_per_energy"
        ]

        print(
            f"Production/Energy : "
            f"{efficiency:.8f}"
        )

    print("\n================================================")
    print("        PARETO OPTIMIZATION COMPLETE")
    print("================================================")
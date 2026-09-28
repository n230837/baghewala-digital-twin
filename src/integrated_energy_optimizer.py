# ============================================================
# BAGHEWALA DIGITAL TWIN
# INTEGRATED ENERGY OPTIMIZER
# ============================================================

from integrated_optimizer import run_integrated_optimization
from steam_energy_model import calculate_steam_energy


def run_energy_optimization(
    well_id,
    candidate_spm_values
):

    integrated_results = run_integrated_optimization(
        well_id=well_id,
        candidate_spm_values=candidate_spm_values
    )

    results = []

    for result in integrated_results:

        energy_kwh = calculate_steam_energy(
            steam_volume_m3=result["steam_volume_m3"],
            steam_temperature_c=result["steam_temperature_c"],
            injection_days=result["injection_days"]
        )

        production = result[
            "predicted_production_bpd"
        ]

        # Production per unit steam energy
        efficiency = (
            production / energy_kwh
            if energy_kwh > 0
            else 0
        )

        results.append({

            # CSS
            "steam_temperature_c":
                result["steam_temperature_c"],

            "steam_volume_m3":
                result["steam_volume_m3"],

            "injection_days":
                result["injection_days"],

            "soak_days":
                result["soak_days"],

            # Thermal
            "production_temperature_c":
                result["production_temperature_c"],

            "viscosity_cp":
                result["viscosity_cp"],

            # SRP
            "spm":
                result["spm"],

            "pump_fillage_percent":
                result["pump_fillage_percent"],

            "rod_load_range":
                result["rod_load_range"],

            # Production
            "predicted_production_bpd":
                production,

            # Energy
            "steam_energy_kwh":
                energy_kwh,

            "production_per_energy":
                efficiency,

            # Existing score
            "operating_score":
                result["operating_score"]
        })

    # Highest production/energy efficiency first
    results.sort(
        key=lambda x: x["production_per_energy"],
        reverse=True
    )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("================================================")
    print("        INTEGRATED ENERGY OPTIMIZER")
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

    print()
    print(
        f"Total combinations: {len(results)}"
    )

    print()
    print("TOP 10 ENERGY-EFFICIENT SCENARIOS")
    print("----------------------------------")

    for i, result in enumerate(
        results[:10],
        start=1
    ):

        print()
        print(f"#{i}")

        print(
            f"Steam: "
            f"{result['steam_temperature_c']:.0f} °C | "
            f"{result['steam_volume_m3']:.0f} m³ | "
            f"{result['injection_days']:.0f} days"
        )

        print(
            f"SPM: "
            f"{result['spm']:.1f}"
        )

        print(
            f"Fillage: "
            f"{result['pump_fillage_percent']:.2f}%"
        )

        print(
            f"Production: "
            f"{result['predicted_production_bpd']:.2f} BPD"
        )

        print(
            f"Steam energy: "
            f"{result['steam_energy_kwh']:.0f} kWh"
        )

        print(
            f"Production / energy: "
            f"{result['production_per_energy']:.8f}"
        )

    print()
    print("================================================")
    print("        ENERGY OPTIMIZATION COMPLETE")
    print("================================================")
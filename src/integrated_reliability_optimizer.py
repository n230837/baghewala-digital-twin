# ============================================================
# BAGHEWALA DIGITAL TWIN
# INTEGRATED RELIABILITY OPTIMIZER
# VFD-AWARE VERSION
# ============================================================

import numpy as np

from integrated_energy_optimizer import run_energy_optimization

from srp_reliability_model import (
    calculate_reliability_score
)

from vfd_model import (
    calculate_spm_from_vfd,
    calculate_vfd_frequency_from_spm,
    calculate_vfd_power_factor
)


# ============================================================
# VFD OPTIMIZATION RANGE
# ============================================================

MIN_VFD_FREQUENCY_HZ = 35.0
MAX_VFD_FREQUENCY_HZ = 60.0
NUMBER_OF_VFD_CANDIDATES = 9


# ============================================================
# GENERATE VFD CANDIDATES
# ============================================================

def generate_vfd_candidates():

    return [
        round(float(value), 3)
        for value in np.linspace(
            MIN_VFD_FREQUENCY_HZ,
            MAX_VFD_FREQUENCY_HZ,
            NUMBER_OF_VFD_CANDIDATES
        )
    ]


# ============================================================
# VFD-AWARE RELIABILITY OPTIMIZATION
# ============================================================

def run_reliability_optimization(
    well_id,
    candidate_vfd_values=None,
    candidate_spm_values=None
):

    # --------------------------------------------------------
    # Backward compatibility
    # --------------------------------------------------------
    # If old SPM values are supplied, convert them to VFD.
    # This allows existing parts of the project to continue
    # working during the VFD transition.
    # --------------------------------------------------------

    if candidate_vfd_values is None:

        if candidate_spm_values is not None:

            candidate_vfd_values = [
                calculate_vfd_frequency_from_spm(spm)
                for spm in candidate_spm_values
            ]

        else:

            candidate_vfd_values = generate_vfd_candidates()

    # --------------------------------------------------------
    # Convert VFD → SPM
    # --------------------------------------------------------

    candidate_spm_values = [
        calculate_spm_from_vfd(vfd)
        for vfd in candidate_vfd_values
    ]

    # --------------------------------------------------------
    # Existing energy optimizer still receives SPM.
    # We are not changing that model in this step.
    # --------------------------------------------------------

    energy_results = run_energy_optimization(
        well_id=well_id,
        candidate_spm_values=candidate_spm_values
    )

    results = []

    # --------------------------------------------------------
    # Process every generated scenario
    # --------------------------------------------------------

    for result in energy_results:

        spm = float(result["spm"])

        # ----------------------------------------------------
        # IMPORTANT:
        # Match VFD to the ACTUAL SPM returned by the optimizer.
        #
        # We do NOT use the result index because the energy
        # optimizer may reorder/process scenarios differently.
        # ----------------------------------------------------

        vfd_frequency = min(
            candidate_vfd_values,
            key=lambda vfd: abs(
                calculate_spm_from_vfd(vfd) - spm
            )
        )

        # ----------------------------------------------------
        # VFD power factor
        # ----------------------------------------------------

        vfd_power_factor = calculate_vfd_power_factor(
            vfd_frequency
        )

        # ----------------------------------------------------
        # Reliability risk
        # ----------------------------------------------------

        risk = calculate_reliability_score(
            viscosity_cp=result["viscosity_cp"],
            spm=spm,
            rod_load_range=result["rod_load_range"],
            pump_fillage=result["pump_fillage_percent"]
        )

        # ----------------------------------------------------
        # Store complete scenario
        # ----------------------------------------------------

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

            # Fluid
            "production_temperature_c":
                result["production_temperature_c"],

            "viscosity_cp":
                result["viscosity_cp"],

            # VFD / SRP
            "vfd_frequency_hz":
                float(vfd_frequency),

            "vfd_power_factor":
                float(vfd_power_factor),

            "spm":
                spm,

            "pump_fillage_percent":
                result["pump_fillage_percent"],

            "rod_load_range":
                result["rod_load_range"],

            # Production
            "predicted_production_bpd":
                result["predicted_production_bpd"],

            # Energy
            "steam_energy_kwh":
                result["steam_energy_kwh"],

            "production_per_energy":
                result["production_per_energy"],

            # Reliability
            "reliability_risk":
                risk,

            # Existing score
            "operating_score":
                result["operating_score"]
        })

    # --------------------------------------------------------
    # Sort:
    # 1. Lower reliability risk
    # 2. Higher production
    # --------------------------------------------------------

    results.sort(
        key=lambda x: (
            x["reliability_risk"],
            -x["predicted_production_bpd"]
        )
    )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("================================================")
    print("       VFD-AWARE RELIABILITY OPTIMIZER")
    print("================================================")

    # --------------------------------------------------------
    # Generate VFD candidates
    # --------------------------------------------------------

    candidates = generate_vfd_candidates()

    print()
    print("VFD candidates:")
    print("----------------")

    for vfd in candidates:

        spm = calculate_spm_from_vfd(vfd)

        print(
            f"VFD: {vfd:.3f} Hz"
            f"  ->  "
            f"SPM: {spm:.2f}"
        )

    # --------------------------------------------------------
    # Run optimization
    # --------------------------------------------------------

    results = run_reliability_optimization(
        well_id="NK-68",
        candidate_vfd_values=candidates
    )

    print()
    print(
        f"Total combinations: {len(results)}"
    )

    # --------------------------------------------------------
    # Display top scenarios
    # --------------------------------------------------------

    print()
    print("TOP 10 LOW-RISK SCENARIOS")
    print("-------------------------")

    for i, result in enumerate(
        results[:10],
        start=1
    ):

        print()
        print(f"#{i}")

        print(
            f"Steam: "
            f"{result['steam_temperature_c']:.0f} °C | "
            f"{result['steam_volume_m3']:.0f} m³"
        )

        print(
            f"VFD: "
            f"{result['vfd_frequency_hz']:.3f} Hz | "
            f"SPM: "
            f"{result['spm']:.2f}"
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
            f"Energy: "
            f"{result['steam_energy_kwh']:.0f} kWh"
        )

        print(
            f"Reliability risk: "
            f"{result['reliability_risk']:.2f}/100"
        )

    print()
    print("================================================")
    print("       VFD OPTIMIZATION COMPLETE")
    print("================================================")
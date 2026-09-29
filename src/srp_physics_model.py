
# ============================================================
# BAGHEWALA DIGITAL TWIN
# SRP PHYSICS MODEL V1
# ============================================================
#
# Purpose:
#   Physics-informed SRP load estimation layer that can sit
#   underneath the existing SRP state / ML fillage models.
#
# IMPORTANT:
#   This is a prototype engineering model. The default geometry,
#   fluid properties and operating assumptions are configurable
#   and are NOT Baghewala field calibration data.
#
# Effects represented:
#   1. Rod-string mass
#   2. Hydrostatic load
#   3. Buoyancy correction
#   4. Inertial load from reciprocating motion
#   5. Viscous resistance proxy
#   6. Upstroke/downstroke load range
#
# ============================================================

import math


# ============================================================
# PROTOTYPE DEFAULT PARAMETERS
# ============================================================

DEFAULT_ROD_LENGTH_M = 1100.0
DEFAULT_ROD_DIAMETER_M = 0.0254       # 1 inch
DEFAULT_STROKE_LENGTH_M = 2.5
DEFAULT_PLUNGER_DIAMETER_M = 0.04445  # 1.75 inch

STEEL_DENSITY_KG_M3 = 7850.0
OIL_DENSITY_KG_M3 = 900.0

GRAVITY_M_S2 = 9.81

# Pressure values are explicit inputs/default assumptions.
DEFAULT_PUMP_PRESSURE_PA = 1600.0 * 6894.757293168
DEFAULT_TUBING_PRESSURE_PA = 0.0

# Empirical prototype coefficient for viscous resistance.
# This is deliberately exposed as a parameter and is NOT
# presented as a field-calibrated constant.
DEFAULT_VISCOUS_COEFFICIENT = 0.015

MIN_LOAD_RANGE_KG = 100.0
MAX_LOAD_RANGE_KG = 15000.0


# ============================================================
# BASIC GEOMETRY
# ============================================================

def circular_area(diameter_m):
    """Return cross-sectional area in m²."""
    if diameter_m <= 0:
        raise ValueError("Diameter must be positive.")

    return math.pi * diameter_m ** 2 / 4.0


def calculate_rod_string_mass(
    rod_length_m=DEFAULT_ROD_LENGTH_M,
    rod_diameter_m=DEFAULT_ROD_DIAMETER_M,
    rod_density_kg_m3=STEEL_DENSITY_KG_M3,
):
    """Estimate total rod-string mass."""
    if rod_length_m <= 0:
        raise ValueError("Rod length must be positive.")

    rod_area = circular_area(rod_diameter_m)
    rod_volume = rod_area * rod_length_m

    return rod_volume * rod_density_kg_m3


# ============================================================
# BUOYANCY
# ============================================================

def calculate_buoyancy_force(
    rod_length_m=DEFAULT_ROD_LENGTH_M,
    rod_diameter_m=DEFAULT_ROD_DIAMETER_M,
    fluid_density_kg_m3=OIL_DENSITY_KG_M3,
):
    """
    Archimedes buoyancy force acting on the immersed rod string.
    """
    if fluid_density_kg_m3 < 0:
        raise ValueError("Fluid density cannot be negative.")

    rod_area = circular_area(rod_diameter_m)
    displaced_volume = rod_area * rod_length_m

    return (
        fluid_density_kg_m3
        * GRAVITY_M_S2
        * displaced_volume
    )


# ============================================================
# HYDROSTATIC LOAD
# ============================================================

def calculate_hydrostatic_load(
    pressure_pa=DEFAULT_PUMP_PRESSURE_PA,
    plunger_diameter_m=DEFAULT_PLUNGER_DIAMETER_M,
):
    """
    Pressure force on the pump/plunger area.

    This is a simplified surface-load contribution, not a full
    API RP 11L dynamometer-card calculation.
    """
    if pressure_pa < 0:
        raise ValueError("Pressure cannot be negative.")

    plunger_area = circular_area(plunger_diameter_m)

    return pressure_pa * plunger_area


# ============================================================
# RECIPROCATING KINEMATICS
# ============================================================

def calculate_peak_acceleration(
    spm,
    stroke_length_m=DEFAULT_STROKE_LENGTH_M,
):
    """
    Peak sinusoidal acceleration approximation.

    stroke_length = 2 * crank radius.
    """
    if spm <= 0:
        raise ValueError("SPM must be positive.")

    if stroke_length_m <= 0:
        raise ValueError("Stroke length must be positive.")

    crank_radius_m = stroke_length_m / 2.0
    angular_velocity = 2.0 * math.pi * spm / 60.0

    return crank_radius_m * angular_velocity ** 2


def calculate_inertial_force(
    spm,
    rod_length_m=DEFAULT_ROD_LENGTH_M,
    rod_diameter_m=DEFAULT_ROD_DIAMETER_M,
    rod_density_kg_m3=STEEL_DENSITY_KG_M3,
    fluid_density_kg_m3=OIL_DENSITY_KG_M3,
    stroke_length_m=DEFAULT_STROKE_LENGTH_M,
):
    """
    Estimate peak reciprocating inertial force using buoyancy-
    corrected rod mass.
    """
    rod_mass = calculate_rod_string_mass(
        rod_length_m=rod_length_m,
        rod_diameter_m=rod_diameter_m,
        rod_density_kg_m3=rod_density_kg_m3,
    )

    rod_volume = (
        circular_area(rod_diameter_m)
        * rod_length_m
    )

    displaced_fluid_mass = (
        fluid_density_kg_m3
        * rod_volume
    )

    effective_mass = max(
        rod_mass - displaced_fluid_mass,
        0.0,
    )

    acceleration = calculate_peak_acceleration(
        spm=spm,
        stroke_length_m=stroke_length_m,
    )

    return effective_mass * acceleration


# ============================================================
# VISCOUS RESISTANCE
# ============================================================

def calculate_viscous_resistance(
    viscosity_cp,
    spm,
    rod_diameter_m=DEFAULT_ROD_DIAMETER_M,
    rod_length_m=DEFAULT_ROD_LENGTH_M,
    stroke_length_m=DEFAULT_STROKE_LENGTH_M,
    coefficient=DEFAULT_VISCOUS_COEFFICIENT,
):
    """
    Prototype viscous-resistance proxy.

    The viscosity is converted from cP to Pa·s. The dependence
    is intentionally sub-linear so that viscosity does not
    dominate the other load components.

    This coefficient must be calibrated against field
    dynamometer data before operational use.
    """
    if viscosity_cp <= 0:
        raise ValueError("Viscosity must be positive.")

    if spm <= 0:
        raise ValueError("SPM must be positive.")

    if rod_diameter_m <= 0:
        raise ValueError("Rod diameter must be positive.")

    if rod_length_m <= 0:
        raise ValueError("Rod length must be positive.")

    if coefficient < 0:
        raise ValueError("Viscous coefficient cannot be negative.")

    viscosity_pa_s = viscosity_cp / 1000.0

    rod_area = circular_area(rod_diameter_m)

    if stroke_length_m <= 0:
        raise ValueError("Stroke length must be positive.")

    linear_speed = (
        2.0
        * (stroke_length_m / 2.0)
        * spm
        / 60.0
    )

    # A bounded proxy for viscous drag.
    # sqrt(viscosity) prevents unrealistically large growth.
    resistance_n = (
        coefficient
        * math.sqrt(viscosity_pa_s)
        * rod_length_m
        * rod_area
        * linear_speed
        * 1e5
    )

    return max(resistance_n, 0.0)


# ============================================================
# LOAD STATE
# ============================================================

def estimate_srp_physics_state(
    viscosity_cp,
    spm,
    rod_length_m=DEFAULT_ROD_LENGTH_M,
    rod_diameter_m=DEFAULT_ROD_DIAMETER_M,
    stroke_length_m=DEFAULT_STROKE_LENGTH_M,
    plunger_diameter_m=DEFAULT_PLUNGER_DIAMETER_M,
    pump_pressure_pa=DEFAULT_PUMP_PRESSURE_PA,
    tubing_pressure_pa=DEFAULT_TUBING_PRESSURE_PA,
    rod_density_kg_m3=STEEL_DENSITY_KG_M3,
    fluid_density_kg_m3=OIL_DENSITY_KG_M3,
    viscous_coefficient=DEFAULT_VISCOUS_COEFFICIENT,
):
    """
    Return a physics-informed SRP operating state.

    The output is intentionally compatible with the existing
    project's rod-load terminology:
        load_range_kg
        min_rod_load_kg
        max_rod_load_kg
    """
    if viscosity_cp <= 0:
        raise ValueError("Viscosity must be positive.")

    if spm <= 0:
        raise ValueError("SPM must be positive.")

    if stroke_length_m <= 0:
        raise ValueError("Stroke length must be positive.")

    if pump_pressure_pa < tubing_pressure_pa:
        raise ValueError(
            "Pump pressure must be >= tubing pressure."
        )

    rod_mass = calculate_rod_string_mass(
        rod_length_m=rod_length_m,
        rod_diameter_m=rod_diameter_m,
        rod_density_kg_m3=rod_density_kg_m3,
    )

    buoyancy_n = calculate_buoyancy_force(
        rod_length_m=rod_length_m,
        rod_diameter_m=rod_diameter_m,
        fluid_density_kg_m3=fluid_density_kg_m3,
    )

    rod_weight_n = rod_mass * GRAVITY_M_S2
    buoyancy_corrected_weight_n = max(
        rod_weight_n - buoyancy_n,
        0.0,
    )

    pressure_difference_pa = (
        pump_pressure_pa - tubing_pressure_pa
    )

    hydrostatic_load_n = calculate_hydrostatic_load(
        pressure_pa=pressure_difference_pa,
        plunger_diameter_m=plunger_diameter_m,
    )

    inertial_force_n = calculate_inertial_force(
        spm=spm,
        rod_length_m=rod_length_m,
        rod_diameter_m=rod_diameter_m,
        rod_density_kg_m3=rod_density_kg_m3,
        fluid_density_kg_m3=fluid_density_kg_m3,
        stroke_length_m=stroke_length_m,
    )

    viscous_force_n = calculate_viscous_resistance(
        viscosity_cp=viscosity_cp,
        spm=spm,
        rod_diameter_m=rod_diameter_m,
        rod_length_m=rod_length_m,
        stroke_length_m=stroke_length_m,
        coefficient=viscous_coefficient,
    )

    # Simplified upstroke/downstroke envelope.
    #
    # Upstroke:
    #   buoyancy-corrected rod weight
    #   + pressure load
    #   + inertia
    #   + viscous resistance
    #
    # Downstroke:
    #   buoyancy-corrected rod weight
    #   - pressure load
    #   - inertia
    #   - viscous resistance
    #
    # The absolute values are used for a load envelope rather
    # than interpreting the downstroke as a tensile negative load.
    max_load_n = (
        buoyancy_corrected_weight_n
        + hydrostatic_load_n
        + inertial_force_n
        + viscous_force_n
    )

    min_load_n = (
        buoyancy_corrected_weight_n
        - hydrostatic_load_n
        - inertial_force_n
        - viscous_force_n
    )

    max_load_kg = max_load_n / GRAVITY_M_S2
    min_load_kg = min_load_n / GRAVITY_M_S2

    load_range_kg = abs(
        max_load_kg - min_load_kg
    )

    load_range_kg = max(
        MIN_LOAD_RANGE_KG,
        min(load_range_kg, MAX_LOAD_RANGE_KG),
    )

    return {
        "viscosity_cp": float(viscosity_cp),
        "spm": float(spm),
        "stroke_length_m": float(stroke_length_m),

        "rod_mass_kg": float(rod_mass),
        "rod_weight_kg": float(
            rod_weight_n / GRAVITY_M_S2
        ),
        "buoyancy_force_kg": float(
            buoyancy_n / GRAVITY_M_S2
        ),

        "hydrostatic_load_kg": float(
            hydrostatic_load_n / GRAVITY_M_S2
        ),

        "peak_acceleration_m_s2": float(
            calculate_peak_acceleration(
                spm=spm,
                stroke_length_m=stroke_length_m,
            )
        ),

        "inertial_force_kg": float(
            inertial_force_n / GRAVITY_M_S2
        ),

        "viscous_resistance_kg": float(
            viscous_force_n / GRAVITY_M_S2
        ),

        "min_rod_load_kg": float(min_load_kg),
        "max_rod_load_kg": float(max_load_kg),
        "load_range_kg": float(load_range_kg),

        "model_type": (
            "Physics-informed SRP prototype "
            "(not field calibrated)"
        ),
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("        SRP PHYSICS MODEL V1")
    print("=" * 60)

    test_viscosity = 7758.94

    for test_spm in [3.5, 4.0, 4.5, 5.0, 5.5, 6.0]:
        state = estimate_srp_physics_state(
            viscosity_cp=test_viscosity,
            spm=test_spm,
        )

        print(
            f"SPM {test_spm:.1f} | "
            f"Load range {state['load_range_kg']:.1f} kg | "
            f"Min {state['min_rod_load_kg']:.1f} kg | "
            f"Max {state['max_rod_load_kg']:.1f} kg | "
            f"Inertia {state['inertial_force_kg']:.1f} kg"
        )

    print("=" * 60)
    print("        SRP PHYSICS MODEL TEST COMPLETE")
    print("=" * 60)

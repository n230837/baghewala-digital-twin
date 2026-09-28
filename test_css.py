from src.thermal_model import (
    calculate_reservoir_temperature,
    calculate_cooling_temperature
)

from src.viscosity_model import viscosity_arrhenius

from src.production_model import calculate_production_rate

from src.srp_model import calculate_srp_efficiency

from src.srp_risk_model import (
    calculate_rod_floating_risk,
    classify_risk
)


# --------------------------------------------------
# BAGHEWALA WELL-TO-SURFACE DIGITAL TWIN
# --------------------------------------------------

INITIAL_TEMPERATURE = 47.0
STEAM_VOLUME = 500.0

# SRP settings
SPM = 6.0
STROKE_LENGTH = 2.5


print("==========================================================")
print("       BAGHEWALA WELL-TO-SURFACE DIGITAL TWIN")
print("==========================================================")


# --------------------------------------------------
# CSS HEATING
# --------------------------------------------------

heated_temperature = calculate_reservoir_temperature(
    INITIAL_TEMPERATURE,
    STEAM_VOLUME
)


# --------------------------------------------------
# COOLING + SRP + PRODUCTION
# --------------------------------------------------

cooling_hours = [0, 12, 24, 48, 72, 96]


print("\nCSS + SRP CYCLE")
print("---------------")

print(
    "Time | Temp | Viscosity | SRP Eff. | "
    "Risk | Production"
)

print(
    " h   | °C   | cP        |          | "
    "     | BPD"
)

print("-" * 65)


for hours in cooling_hours:

    # ----------------------------------------------
    # Reservoir temperature
    # ----------------------------------------------

    temperature = calculate_cooling_temperature(
        heated_temperature,
        INITIAL_TEMPERATURE,
        hours
    )

    # ----------------------------------------------
    # Oil viscosity
    # ----------------------------------------------

    viscosity = viscosity_arrhenius(
        temperature
    )

    # ----------------------------------------------
    # SRP efficiency
    # ----------------------------------------------

    srp_efficiency = calculate_srp_efficiency(
        SPM,
        STROKE_LENGTH,
        viscosity
    )

    # ----------------------------------------------
    # SRP rod-floating risk
    # ----------------------------------------------

    risk_score = calculate_rod_floating_risk(
        viscosity,
        SPM,
        STROKE_LENGTH
    )

    risk_level = classify_risk(
        risk_score
    )

    # ----------------------------------------------
    # Production
    # ----------------------------------------------

    production = calculate_production_rate(
        viscosity,
        srp_efficiency
    )

    # ----------------------------------------------
    # Display
    # ----------------------------------------------

    print(
        f"{hours:>3} | "
        f"{temperature:>5.2f} | "
        f"{viscosity:>9.2f} | "
        f"{srp_efficiency:>8.3f} | "
        f"{risk_level:>6} | "
        f"{production:>10.2f}"
    )
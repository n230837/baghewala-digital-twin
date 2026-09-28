from thermal_model import (
    simulate_css_cycle
)

from viscosity_model import (
    viscosity_arrhenius
)


# ============================================================
# THERMAL → VISCOSITY TEST
# ============================================================

print("================================================")
print("       THERMAL → VISCOSITY CONNECTION")
print("================================================")


# ============================================================
# SIMULATE BAGHEWALA CSS CYCLE
# ============================================================

result = simulate_css_cycle(
    initial_temperature_c=47.0,
    steam_temperature_c=285.0,
    steam_volume_m3=500.0,
    injection_days=14.0,
    soak_days=7.0
)


# ============================================================
# EXTRACT TEMPERATURES
# ============================================================

initial_temperature = (
    result["initial_temperature_c"]
)

heated_temperature = (
    result["heated_temperature_c"]
)

production_temperature = (
    result["production_start_temperature_c"]
)


# ============================================================
# CALCULATE VISCOSITIES
# ============================================================

initial_viscosity = viscosity_arrhenius(
    initial_temperature
)

heated_viscosity = viscosity_arrhenius(
    heated_temperature
)

production_viscosity = viscosity_arrhenius(
    production_temperature
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nCSS THERMAL RESULTS")
print("-------------------")

print(
    f"Initial temperature: "
    f"{initial_temperature:.2f} °C"
)

print(
    f"Heated temperature: "
    f"{heated_temperature:.2f} °C"
)

print(
    f"Production temperature: "
    f"{production_temperature:.2f} °C"
)


print("\nVISCOSITY RESULTS")
print("-----------------")

print(
    f"Initial viscosity: "
    f"{initial_viscosity:.2f} cP"
)

print(
    f"Heated viscosity: "
    f"{heated_viscosity:.2f} cP"
)

print(
    f"Production viscosity: "
    f"{production_viscosity:.2f} cP"
)


# ============================================================
# VISCOSITY REDUCTION
# ============================================================

heated_reduction = (
    1 -
    heated_viscosity / initial_viscosity
) * 100

production_reduction = (
    1 -
    production_viscosity / initial_viscosity
) * 100


print("\nVISCOSITY REDUCTION")
print("-------------------")

print(
    f"During heating: "
    f"{heated_reduction:.2f}%"
)

print(
    f"At production start: "
    f"{production_reduction:.2f}%"
)


# ============================================================
# END
# ============================================================

print("\n================================================")
print("       THERMAL → VISCOSITY TEST COMPLETE")
print("================================================")
from thermal_model import simulate_css_cycle
from viscosity_model_v2 import calculate_viscosity
from srp_input_model import estimate_srp_operating_condition


print("================================================")
print("       CSS → THERMAL → VISCOSITY → SRP")
print("================================================")


# ------------------------------------------------
# 1. CSS / thermal simulation
# ------------------------------------------------

css = simulate_css_cycle(
    initial_temperature_c=47.0,
    steam_temperature_c=285.0,
    steam_volume_m3=500.0,
    injection_days=14.0,
    soak_days=7.0
)


# ------------------------------------------------
# 2. Production-start temperature
# ------------------------------------------------

production_temperature = (
    css["production_start_temperature_c"]
)


# ------------------------------------------------
# 3. Calculate viscosity
# ------------------------------------------------

viscosity = calculate_viscosity(
    production_temperature
)


# ------------------------------------------------
# 4. Estimate SRP starting condition
# ------------------------------------------------

srp = estimate_srp_operating_condition(
    viscosity
)


# ------------------------------------------------
# 5. Display complete chain
# ------------------------------------------------

print("\nCSS")
print("---")
print(
    f"Steam temperature : "
    f"{css['steam_temperature_c']:.2f} °C"
)

print(
    f"Steam volume      : "
    f"500.00 m³"
)

print(
    f"Injection         : "
    f"{css['injection_days']:.1f} days"
)

print(
    f"Soak              : "
    f"{css['soak_days']:.1f} days"
)


print("\nTHERMAL RESPONSE")
print("----------------")
print(
    f"Initial temperature : "
    f"{css['initial_temperature_c']:.2f} °C"
)

print(
    f"Heated temperature  : "
    f"{css['heated_temperature_c']:.2f} °C"
)

print(
    f"Production temp.    : "
    f"{production_temperature:.2f} °C"
)


print("\nVISCOSITY")
print("---------")
print(
    f"Production viscosity : "
    f"{viscosity:.2f} cP"
)


print("\nSRP RESPONSE")
print("------------")
print(
    f"Viscosity condition : "
    f"{srp['condition']}"
)

print(
    f"Starting SPM        : "
    f"{srp['starting_spm']:.1f}"
)


print("\n================================================")
print("       WELL-TO-SURFACE CHAIN COMPLETE")
print("================================================")
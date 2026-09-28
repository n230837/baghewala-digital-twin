from thermal_model import simulate_css_cycle
from viscosity_model_v2 import calculate_viscosity


print("================================================")
print("       CSS → THERMAL → VISCOSITY")
print("================================================")


# ------------------------------------------------
# 1. Simulate CSS thermal cycle
# ------------------------------------------------

result = simulate_css_cycle(
    initial_temperature_c=47.0,
    steam_temperature_c=285.0,
    steam_volume_m3=500.0,
    injection_days=14.0,
    soak_days=7.0
)


# ------------------------------------------------
# 2. Extract temperatures
# ------------------------------------------------

initial_temperature = result["initial_temperature_c"]
heated_temperature = result["heated_temperature_c"]
production_temperature = result["production_start_temperature_c"]


# ------------------------------------------------
# 3. Calculate viscosity at each stage
# ------------------------------------------------

initial_viscosity = calculate_viscosity(
    initial_temperature
)

heated_viscosity = calculate_viscosity(
    heated_temperature
)

production_viscosity = calculate_viscosity(
    production_temperature
)


# ------------------------------------------------
# 4. Calculate viscosity reduction
# ------------------------------------------------

heated_reduction = (
    1 - heated_viscosity / initial_viscosity
) * 100

production_reduction = (
    1 - production_viscosity / initial_viscosity
) * 100


# ------------------------------------------------
# 5. Display digital-twin chain
# ------------------------------------------------

print("\nCSS INPUT")
print("---------")
print(f"Steam temperature       : {result['steam_temperature_c']:.2f} °C")
print(f"Steam volume            : 500.00 m³")
print(f"Injection duration      : {result['injection_days']:.1f} days")
print(f"Soak duration           : {result['soak_days']:.1f} days")


print("\nTHERMAL MODEL")
print("-------------")
print(f"Initial reservoir temp  : {initial_temperature:.2f} °C")
print(f"After steam heating     : {heated_temperature:.2f} °C")
print(f"At production start     : {production_temperature:.2f} °C")


print("\nVISCOSITY MODEL")
print("---------------")
print(f"Initial viscosity       : {initial_viscosity:.2f} cP")
print(f"After heating           : {heated_viscosity:.2f} cP")
print(f"At production start     : {production_viscosity:.2f} cP")


print("\nVISCOSITY REDUCTION")
print("-------------------")
print(f"During heating          : {heated_reduction:.2f}%")
print(f"At production start     : {production_reduction:.2f}%")


print("\n================================================")
print("       CSS → VISCOSITY CONNECTION COMPLETE")
print("================================================")
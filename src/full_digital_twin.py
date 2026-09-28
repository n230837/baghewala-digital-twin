from thermal_model import simulate_css_cycle
from viscosity_model_v2 import calculate_viscosity
from srp_input_model import estimate_srp_operating_condition
from srp_state_model import estimate_srp_state
from srp_predictor import predict_srp


print("================================================")
print("        BAGHEWALA DIGITAL TWIN")
print("        END-TO-END SIMULATION")
print("================================================")


# ============================================================
# STEP 1 — CSS
# ============================================================

css = simulate_css_cycle(
    initial_temperature_c=47.0,
    steam_temperature_c=285.0,
    steam_volume_m3=500.0,
    injection_days=14.0,
    soak_days=7.0
)


# ============================================================
# STEP 2 — PRODUCTION TEMPERATURE
# ============================================================

production_temperature = (
    css["production_start_temperature_c"]
)


# ============================================================
# STEP 3 — VISCOSITY
# ============================================================

viscosity = calculate_viscosity(
    production_temperature
)


# ============================================================
# STEP 4 — INITIAL SRP OPERATING CONDITION
# ============================================================

srp_condition = estimate_srp_operating_condition(
    viscosity
)

spm = srp_condition["starting_spm"]


# ============================================================
# STEP 5 — ESTIMATE SRP OPERATING STATE
# ============================================================

srp_state = estimate_srp_state(
    viscosity_cp=viscosity,
    spm=spm
)


# ============================================================
# STEP 6 — SRP ML PREDICTION
# ============================================================

prediction = predict_srp(
    well_id="NK-68",
    spm=spm,
    min_rod_weight=srp_state[
        "estimated_min_rod_weight"
    ],
    max_rod_weight=srp_state[
        "estimated_max_rod_weight"
    ],
    dynamometer_area=srp_state[
        "estimated_dynamometer_area"
    ]
)


# ============================================================
# FINAL DIGITAL-TWIN OUTPUT
# ============================================================

print("\n1. CSS INPUT")
print("------------")

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


print("\n2. THERMAL RESPONSE")
print("--------------------")

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


print("\n3. VISCOSITY RESPONSE")
print("---------------------")

print(
    f"Oil viscosity       : "
    f"{viscosity:.2f} cP"
)


print("\n4. SRP OPERATING CONDITION")
print("--------------------------")

print(
    f"Condition           : "
    f"{srp_condition['condition']}"
)

print(
    f"Starting SPM        : "
    f"{spm:.2f}"
)


print("\n5. SRP OPERATING STATE")
print("----------------------")

print(
    f"Estimated load range : "
    f"{srp_state['estimated_load_range']:.2f} kg"
)

print(
    f"Minimum rod weight   : "
    f"{srp_state['estimated_min_rod_weight']:.2f} kg"
)

print(
    f"Maximum rod weight   : "
    f"{srp_state['estimated_max_rod_weight']:.2f} kg"
)

print(
    f"Dynamometer area     : "
    f"{srp_state['estimated_dynamometer_area']:.2f}"
)


print("\n6. SRP ML PREDICTION")
print("--------------------")

print(
    f"Predicted pump fillage : "
    f"{prediction['predicted_pump_fillage']:.2f}%"
)

print(
    f"Rod load range         : "
    f"{prediction['rod_load_range']:.2f} kg"
)


print("\n================================================")
print("        DIGITAL TWIN PIPELINE COMPLETE")
print("================================================")
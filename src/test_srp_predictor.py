from srp_predictor import predict_srp


print("================================================")
print("       SRP ML PREDICTOR TEST")
print("================================================")


# Example operating condition
# These values are only a test input.
# They are NOT Baghewala measurements.

result = predict_srp(
    well_id="NK-68",
    spm=4.0,
    min_rod_weight=3500.0,
    max_rod_weight=4750.0,
    dynamometer_area=15000.0
)


print("\nINPUT")
print("-----")
print("Well ID             : NK-68")
print("SPM                 : 4.0")
print("Minimum rod weight : 3500.0 kg")
print("Maximum rod weight : 4750.0 kg")
print("Dynamometer area   : 15000.0")


print("\nMODEL OUTPUT")
print("------------")
print(
    f"Predicted pump fillage : "
    f"{result['predicted_pump_fillage']:.2f}%"
)

print(
    f"Rod load range         : "
    f"{result['rod_load_range']:.2f} kg"
)


print("\n================================================")
print("       SRP ML PREDICTOR TEST COMPLETE")
print("================================================")
import pandas as pd


# ============================================================
# LOAD REAL SRP DATA
# ============================================================

df = pd.read_csv(
    "data/srp_clean.csv",
    parse_dates=["timestamp"]
)

print("================================================")
print("       BUILDING SRP OPERATING FEATURES")
print("================================================")

print("\nRows:", len(df))
print("Wells:", df["well_id"].nunique())


# ============================================================
# DERIVED SRP FEATURES
# ============================================================

# Difference between maximum and minimum rod load
df["rod_load_range"] = (
    df["max_rod_weight"] -
    df["min_rod_weight"]
)


# Average rod load
df["average_rod_weight"] = (
    df["max_rod_weight"] +
    df["min_rod_weight"]
) / 2


# Normalize load range relative to average rod load
df["normalized_load_range"] = (
    df["rod_load_range"] /
    df["average_rod_weight"].replace(0, pd.NA)
)


# ============================================================
# DATA QUALITY FLAGS
# ============================================================

# Known problematic dynamometer readings
df["negative_dynamometer_area"] = (
    df["dynamometer_area"] < 0
).astype(int)


# Physically suspicious derived load range
df["negative_load_range"] = (
    df["rod_load_range"] < 0
).astype(int)


# Zero-speed operating state
df["zero_spm"] = (
    df["SPM"] == 0
).astype(int)


# Very low pump fillage
df["low_pump_fillage"] = (
    df["pump_fillage"] < 40
).astype(int)


# ============================================================
# HIGH LOAD FLAG
# ============================================================

load_threshold = df["rod_load_range"].quantile(0.95)

df["high_rod_load"] = (
    df["rod_load_range"] > load_threshold
).astype(int)


print("\nDERIVED FEATURES")
print("----------------")

print("Rod load threshold (95th percentile):")
print(f"{load_threshold:.2f} kg")

print(
    "\nHigh rod-load observations:",
    df["high_rod_load"].sum()
)

print(
    "Low pump-fillage observations:",
    df["low_pump_fillage"].sum()
)

print(
    "Zero-SPM observations:",
    df["zero_spm"].sum()
)

print(
    "Negative dynamometer-area observations:",
    df["negative_dynamometer_area"].sum()
)

print(
    "Negative load-range observations:",
    df["negative_load_range"].sum()
)


# ============================================================
# SAVE FEATURE DATASET
# ============================================================

output_file = "data/srp_features.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nSaved:")
print(output_file)


# ============================================================
# SUMMARY
# ============================================================

print("\nFEATURE COLUMNS")
print("----------------")

new_features = [
    "rod_load_range",
    "average_rod_weight",
    "normalized_load_range",
    "negative_dynamometer_area",
    "negative_load_range",
    "zero_spm",
    "low_pump_fillage",
    "high_rod_load"
]

print(new_features)

print("\n================================================")
print("       SRP FEATURE BUILD COMPLETE")
print("================================================")
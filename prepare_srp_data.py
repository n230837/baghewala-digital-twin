import pandas as pd

# ==========================================================
# 1. LOAD ORIGINAL DATASET
# ==========================================================

df = pd.read_csv("data/wells_dataset.csv")

print("Original dataset")
print("----------------")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ==========================================================
# 2. KEEP ONLY SUCKER-ROD-PUMP WELLS
# ==========================================================

df = df[df["well_type"] == "sucker_rod_pump"].copy()

print("\nSRP data")
print("--------")
print(f"Rows: {len(df)}")
print(f"Wells: {df['well_id'].nunique()}")


# ==========================================================
# 3. CONVERT TIMESTAMP
# ==========================================================

df["timestamp"] = pd.to_datetime(df["timestamp"])


# ==========================================================
# 4. SELECT SRP PARAMETERS
# ==========================================================

parameters = [
    "SPM",
    "min_rod_weight",
    "max_rod_weight",
    "dynamometer_area",
    "pump_fillage",
    "tubing_pressure",
    "casing_pressure",
    "line_pressure"
]

df = df[df["parameter"].isin(parameters)].copy()


# ==========================================================
# 5. CONVERT LONG FORMAT → WIDE FORMAT
# ==========================================================

srp = df.pivot_table(
    index=["well_id", "timestamp"],
    columns="parameter",
    values="value",
    aggfunc="first"
).reset_index()


# Remove the column-name label created by pivot_table
srp.columns.name = None


# ==========================================================
# 6. SORT DATA
# ==========================================================

srp = srp.sort_values(
    ["well_id", "timestamp"]
).reset_index(drop=True)


# ==========================================================
# 7. SAVE PROCESSED SRP DATA
# ==========================================================

srp.to_csv(
    "data/srp_timeseries.csv",
    index=False
)


# ==========================================================
# 8. DISPLAY PROCESSED DATA
# ==========================================================

print("\nSRP time-series dataset")
print("-----------------------")
print(f"Rows: {len(srp)}")
print(f"Columns: {len(srp.columns)}")

print("\nColumns:")
print(srp.columns.tolist())


# ==========================================================
# 9. CHECK MISSING VALUES
# ==========================================================

print("\nMissing values:")
print(srp.isna().sum())


# ==========================================================
# 10. CREATE CLEAN CORE SRP DATASET
# ==========================================================

core_parameters = [
    "SPM",
    "min_rod_weight",
    "max_rod_weight",
    "dynamometer_area",
    "pump_fillage"
]

srp_clean = srp.dropna(
    subset=core_parameters
).copy()


# ==========================================================
# 11. SAVE CLEAN DATASET
# ==========================================================

srp_clean.to_csv(
    "data/srp_clean.csv",
    index=False
)


# ==========================================================
# 12. DISPLAY CLEAN DATASET
# ==========================================================

print("\nClean SRP dataset")
print("-----------------")
print(f"Rows: {len(srp_clean)}")
print(f"Columns: {len(srp_clean.columns)}")

print("\nMissing values in core parameters:")
print(
    srp_clean[core_parameters].isna().sum()
)


# ==========================================================
# 13. RECORDS PER WELL
# ==========================================================

print("\nRecords per well:")
print(
    srp_clean["well_id"]
    .value_counts()
    .sort_index()
)


# ==========================================================
# 14. SHOW FIRST 5 ROWS
# ==========================================================

print("\nFirst 5 clean rows:")
print(
    srp_clean.head().to_string(index=False)
)


print("\n================================================")
print("SRP DATA PREPARATION COMPLETE")
print("================================================")
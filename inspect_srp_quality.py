
import pandas as pd

df = pd.read_csv("data/srp_clean.csv")

print("================================================")
print("          SRP DATA QUALITY CHECK")
print("================================================")

# ------------------------------------------------
# 1. Negative rod-load ranges
# ------------------------------------------------

df["rod_load_range"] = (
    df["max_rod_weight"] -
    df["min_rod_weight"]
)

negative_load = df[df["rod_load_range"] < 0]

print("\nNegative rod-load ranges")
print("------------------------")
print("Count:", len(negative_load))

if len(negative_load) > 0:
    print("\nExamples:")
    print(
        negative_load[
            [
                "well_id",
                "timestamp",
                "min_rod_weight",
                "max_rod_weight",
                "rod_load_range"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


# ------------------------------------------------
# 2. Zero rod weights
# ------------------------------------------------

zero_weights = df[
    (df["min_rod_weight"] == 0) |
    (df["max_rod_weight"] == 0)
]

print("\n\nZero rod-weight observations")
print("----------------------------")
print("Count:", len(zero_weights))


# ------------------------------------------------
# 3. Negative dynamometer area
# ------------------------------------------------

negative_area = df[
    df["dynamometer_area"] < 0
]

print("\n\nNegative dynamometer area")
print("-------------------------")
print("Count:", len(negative_area))

if len(negative_area) > 0:
    print("\nExamples:")
    print(
        negative_area[
            [
                "well_id",
                "timestamp",
                "dynamometer_area",
                "SPM",
                "pump_fillage"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


# ------------------------------------------------
# 4. Zero SPM
# ------------------------------------------------

zero_spm = df[df["SPM"] == 0]

print("\n\nZero SPM")
print("--------")
print("Count:", len(zero_spm))

if len(zero_spm) > 0:
    print(
        zero_spm[
            [
                "well_id",
                "timestamp",
                "SPM",
                "pump_fillage"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


# ------------------------------------------------
# 5. Pump fillage extremes
# ------------------------------------------------

print("\n\nPump fillage = 0%")
print("-----------------")
print(
    len(df[df["pump_fillage"] == 0])
)

print("\nPump fillage = 100%")
print("-------------------")
print(
    len(df[df["pump_fillage"] >= 99.99])
)


print("\n================================================")
print("          QUALITY CHECK COMPLETE")
print("================================================")
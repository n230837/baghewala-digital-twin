import pandas as pd
import numpy as np

# ==========================================================
# 1. LOAD CLEAN REAL SRP DATA
# ==========================================================

df = pd.read_csv("data/srp_clean.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

print("================================================")
print("        REAL SRP DATA ANALYSIS")
print("================================================")

print(f"\nRows: {len(df)}")
print(f"Wells: {df['well_id'].nunique()}")

# ==========================================================
# 2. BASIC STATISTICS
# ==========================================================

parameters = [
    "SPM",
    "min_rod_weight",
    "max_rod_weight",
    "dynamometer_area",
    "pump_fillage"
]

print("\n\nBASIC STATISTICS")
print("----------------")

print(
    df[parameters]
    .describe()
    .round(2)
    .to_string()
)


# ==========================================================
# 3. STATISTICS BY WELL
# ==========================================================

print("\n\nAVERAGE VALUES BY WELL")
print("----------------------")

well_stats = (
    df.groupby("well_id")[parameters]
    .mean()
    .round(2)
)

print(well_stats.to_string())


# ==========================================================
# 4. CORRELATION MATRIX
# ==========================================================

print("\n\nCORRELATION MATRIX")
print("------------------")

correlation = (
    df[parameters]
    .corr()
    .round(3)
)

print(correlation.to_string())


# ==========================================================
# 5. SPM VS PUMP FILLAGE
# ==========================================================

print("\n\nSPM VS PUMP FILLAGE")
print("-------------------")

print(
    "Correlation:",
    round(
        df["SPM"].corr(df["pump_fillage"]),
        3
    )
)


# ==========================================================
# 6. SPM VS ROD LOAD
# ==========================================================

df["rod_load_range"] = (
    df["max_rod_weight"]
    - df["min_rod_weight"]
)

print("\n\nROD LOAD RANGE")
print("--------------")

print(
    df["rod_load_range"]
    .describe()
    .round(2)
    .to_string()
)

print(
    "\nSPM vs Rod Load Range correlation:",
    round(
        df["SPM"].corr(df["rod_load_range"]),
        3
    )
)


# ==========================================================
# 7. PUMP FILLAGE BY SPM RANGE
# ==========================================================

df["SPM_group"] = pd.cut(
    df["SPM"],
    bins=[0, 2, 3, 4, 5, 6, 7, 8],
    labels=[
        "0-2",
        "2-3",
        "3-4",
        "4-5",
        "5-6",
        "6-7",
        "7-8"
    ],
    include_lowest=True
)

spm_analysis = (
    df.groupby("SPM_group", observed=True)
    .agg(
        observations=("SPM", "count"),
        avg_SPM=("SPM", "mean"),
        avg_pump_fillage=("pump_fillage", "mean"),
        avg_rod_load_range=("rod_load_range", "mean"),
        avg_dynamometer_area=("dynamometer_area", "mean")
    )
    .round(2)
)

print("\n\nPERFORMANCE BY SPM RANGE")
print("------------------------")

print(spm_analysis.to_string())


# ==========================================================
# 8. LOW PUMP-FILLAGE OBSERVATIONS
# ==========================================================

print("\n\nLOW PUMP-FILLAGE ANALYSIS")
print("-------------------------")

low_fillage = df[df["pump_fillage"] < 40]

print(
    f"Observations with pump fillage < 40%: "
    f"{len(low_fillage)}"
)

if len(low_fillage) > 0:

    print(
        "\nAverage conditions during low fillage:"
    )

    print(
        low_fillage[
            [
                "SPM",
                "min_rod_weight",
                "max_rod_weight",
                "dynamometer_area",
                "pump_fillage"
            ]
        ]
        .mean()
        .round(2)
        .to_string()
    )


# ==========================================================
# 9. HIGH ROD-LOAD RANGE
# ==========================================================

threshold = df["rod_load_range"].quantile(0.95)

high_load = df[
    df["rod_load_range"] >= threshold
]

print("\n\nHIGH ROD-LOAD ANALYSIS")
print("----------------------")

print(
    f"95th percentile load range: "
    f"{threshold:.2f} kg"
)

print(
    f"Observations above threshold: "
    f"{len(high_load)}"
)

print(
    "\nAverage conditions during high rod loading:"
)

print(
    high_load[
        [
            "SPM",
            "min_rod_weight",
            "max_rod_weight",
            "pump_fillage",
            "rod_load_range"
        ]
    ]
    .mean()
    .round(2)
    .to_string()
)


# ==========================================================
# 10. WELL-LEVEL PUMP FILLAGE
# ==========================================================

print("\n\nPUMP FILLAGE BY WELL")
print("--------------------")

well_fillage = (
    df.groupby("well_id")["pump_fillage"]
    .agg(["count", "mean", "min", "max"])
    .round(2)
)

print(well_fillage.to_string())


# ==========================================================
# 11. COMPLETE
# ==========================================================

print("\n================================================")
print("          SRP ANALYSIS COMPLETE")
print("================================================")
import pandas as pd


# ============================================================
# LOAD SRP FEATURE DATA
# ============================================================

df = pd.read_csv(
    "data/srp_features.csv",
    parse_dates=["timestamp"]
)

print("================================================")
print("          SRP OPERATING ENVELOPE")
print("================================================")

print("\nRows:", len(df))
print("Wells:", df["well_id"].nunique())


# ============================================================
# CREATE SPM BINS
# ============================================================

bins = [0, 2, 3, 4, 5, 6, 7, 8]

labels = [
    "0-2",
    "2-3",
    "3-4",
    "4-5",
    "5-6",
    "6-7",
    "7-8"
]

df["SPM_range"] = pd.cut(
    df["SPM"],
    bins=bins,
    labels=labels,
    include_lowest=True
)


# ============================================================
# OPERATING ENVELOPE BY SPM
# ============================================================

envelope = df.groupby(
    "SPM_range",
    observed=False
).agg(
    observations=("SPM", "count"),
    avg_spm=("SPM", "mean"),
    avg_pump_fillage=("pump_fillage", "mean"),
    avg_rod_load_range=("rod_load_range", "mean"),
    median_rod_load_range=("rod_load_range", "median"),
    avg_normalized_load=("normalized_load_range", "mean"),
    high_load_rate=("high_rod_load", "mean"),
    low_fillage_rate=("low_pump_fillage", "mean")
)


# Convert rates to percentages

envelope["high_load_rate"] *= 100
envelope["low_fillage_rate"] *= 100


print("\nOPERATING ENVELOPE BY SPM")
print("-------------------------")

print(
    envelope.round(2).to_string()
)


# ============================================================
# FIND BEST OBSERVED SPM REGION
# ============================================================

valid = envelope[
    envelope["observations"] >= 100
].copy()

best_fillage_range = valid[
    "avg_pump_fillage"
].idxmax()

lowest_load_range = valid[
    "avg_rod_load_range"
].idxmin()


print("\nKEY OBSERVATIONS")
print("-----------------")

print(
    "Highest average pump fillage:",
    best_fillage_range
)

print(
    f"Average pump fillage: "
    f"{valid.loc[best_fillage_range, 'avg_pump_fillage']:.2f}%"
)

print(
    "\nLowest average rod-load range:",
    lowest_load_range
)

print(
    f"Average rod-load range: "
    f"{valid.loc[lowest_load_range, 'avg_rod_load_range']:.2f} kg"
)


# ============================================================
# HIGH LOAD / LOW FILLAGE CONDITIONS
# ============================================================

print("\nHIGH-LOAD CONDITIONS")
print("--------------------")

high_load = df[
    df["high_rod_load"] == 1
]

print(
    "Observations:",
    len(high_load)
)

print(
    f"Average SPM: "
    f"{high_load['SPM'].mean():.2f}"
)

print(
    f"Average pump fillage: "
    f"{high_load['pump_fillage'].mean():.2f}%"
)

print(
    f"Average rod-load range: "
    f"{high_load['rod_load_range'].mean():.2f} kg"
)


print("\nLOW-FILLAGE CONDITIONS")
print("----------------------")

low_fillage = df[
    df["low_pump_fillage"] == 1
]

print(
    "Observations:",
    len(low_fillage)
)

print(
    f"Average SPM: "
    f"{low_fillage['SPM'].mean():.2f}"
)

print(
    f"Average pump fillage: "
    f"{low_fillage['pump_fillage'].mean():.2f}%"
)

print(
    f"Average rod-load range: "
    f"{low_fillage['rod_load_range'].mean():.2f} kg"
)


# ============================================================
# SAVE ENVELOPE
# ============================================================

output_file = "data/srp_operating_envelope.csv"

envelope.to_csv(
    output_file
)

print("\nSaved:")
print(output_file)


# ============================================================
# END
# ============================================================

print("\n================================================")
print("       SRP ENVELOPE ANALYSIS COMPLETE")
print("================================================")
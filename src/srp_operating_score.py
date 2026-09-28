import pandas as pd


# ============================================================
# LOAD SRP OPERATING ENVELOPE
# ============================================================

df = pd.read_csv(
    "data/srp_features.csv"
)

print("================================================")
print("          SRP OPERATING SCORE")
print("================================================")


# ============================================================
# REFERENCE VALUES FROM REAL SRP DATA
# ============================================================

# 95th percentile rod-load threshold
HIGH_LOAD_THRESHOLD = df["rod_load_range"].quantile(0.95)

# Maximum observed load range
MAX_LOAD = df["rod_load_range"].quantile(0.99)

# Maximum pump fillage
MAX_FILLAGE = 100.0


# ============================================================
# SCORE FUNCTION
# ============================================================

def calculate_srp_score(
    pump_fillage,
    rod_load_range
):
    """
    Calculate a simple SRP operating score.

    Higher score = more desirable operating condition.

    This is a prototype decision-support score,
    not a physical failure probability.
    """

    # --------------------------------------------------------
    # Pump fillage component
    # --------------------------------------------------------

    fillage_score = (
        pump_fillage / MAX_FILLAGE
    )

    fillage_score = max(
        0.0,
        min(fillage_score, 1.0)
    )


    # --------------------------------------------------------
    # Rod loading component
    # --------------------------------------------------------

    normalized_load = (
        rod_load_range / MAX_LOAD
    )

    normalized_load = max(
        0.0,
        min(normalized_load, 1.0)
    )

    load_score = 1.0 - normalized_load


    # --------------------------------------------------------
    # High-load penalty
    # --------------------------------------------------------

    if rod_load_range > HIGH_LOAD_THRESHOLD:
        high_load_penalty = 0.30
    else:
        high_load_penalty = 0.0


    # --------------------------------------------------------
    # Combined score
    # --------------------------------------------------------

    score = (
        0.60 * fillage_score
        + 0.40 * load_score
        - high_load_penalty
    )


    # Keep score between 0 and 1

    score = max(
        0.0,
        min(score, 1.0)
    )

    return score


# ============================================================
# TEST OPERATING POINTS
# ============================================================

test_points = [
    {
        "SPM": 3.5,
        "pump_fillage": 41.0,
        "rod_load_range": 800
    },
    {
        "SPM": 4.5,
        "pump_fillage": 59.0,
        "rod_load_range": 1250
    },
    {
        "SPM": 5.5,
        "pump_fillage": 51.0,
        "rod_load_range": 1250
    },
    {
        "SPM": 6.5,
        "pump_fillage": 39.0,
        "rod_load_range": 1125
    },
    {
        "SPM": 7.2,
        "pump_fillage": 20.0,
        "rod_load_range": 930
    }
]


print("\nTEST OPERATING POINTS")
print("---------------------")

for point in test_points:

    score = calculate_srp_score(
        point["pump_fillage"],
        point["rod_load_range"]
    )

    print(
        f"SPM: {point['SPM']:.1f} | "
        f"Fillage: {point['pump_fillage']:.1f}% | "
        f"Load range: {point['rod_load_range']:.0f} kg | "
        f"Score: {score:.3f}"
    )


# ============================================================
# END
# ============================================================

print("\n================================================")
print("       SRP OPERATING SCORE COMPLETE")
print("================================================")
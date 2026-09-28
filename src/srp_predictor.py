import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = "data/srp_clean.csv"
SPLIT_DATE = "2026-06-10"


# ============================================================
# FEATURES
# ============================================================

NUMERIC_FEATURES = [
    "SPM",
    "min_rod_weight",
    "max_rod_weight",
    "dynamometer_area"
]

CATEGORICAL_FEATURES = [
    "well_id"
]

TARGET = "pump_fillage"


# ============================================================
# LOAD DATA
# ============================================================

def load_srp_data():

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["timestamp"]
    )

    df = df.sort_values(
        ["timestamp", "well_id"]
    ).reset_index(drop=True)

    return df


# ============================================================
# TRAIN SRP MODEL ONCE
# ============================================================

def train_srp_model():

    print("================================================")
    print("          TRAINING SRP PREDICTOR")
    print("================================================")

    df = load_srp_data()

    train_df = df[
        df["timestamp"] < SPLIT_DATE
    ].copy()

    X_train = train_df[
        NUMERIC_FEATURES + CATEGORICAL_FEATURES
    ]

    y_train = train_df[TARGET]

    # --------------------------------------------------------
    # ENCODER
    # --------------------------------------------------------

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "well",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                ),
                CATEGORICAL_FEATURES
            )
        ],
        remainder="passthrough"
    )

    X_train_encoded = preprocessor.fit_transform(
        X_train
    )

    # --------------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------------

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train_encoded,
        y_train
    )

    print(
        f"Training samples: {len(train_df)}"
    )

    print("SRP model trained successfully.")

    return model, preprocessor, df


# ============================================================
# TRAIN ONCE
# ============================================================

model, preprocessor, df = train_srp_model()


# ============================================================
# REFERENCE LOAD DATA
# ============================================================

df["rod_load_range"] = (
    df["max_rod_weight"]
    - df["min_rod_weight"]
)

df["SPM_range"] = pd.cut(
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

load_reference = (
    df.groupby(
        "SPM_range",
        observed=False
    )["rod_load_range"]
    .median()
)


# ============================================================
# SRP PREDICTOR
# ============================================================

def predict_srp(
    well_id,
    spm,
    min_rod_weight,
    max_rod_weight,
    dynamometer_area
):

    sample = pd.DataFrame({
        "SPM": [spm],
        "min_rod_weight": [min_rod_weight],
        "max_rod_weight": [max_rod_weight],
        "dynamometer_area": [dynamometer_area],
        "well_id": [well_id]
    })

    # Encode new sample
    encoded_sample = preprocessor.transform(
        sample
    )

    # Predict using already-trained model
    predicted_fillage = model.predict(
        encoded_sample
    )[0]

    actual_load_range = (
        max_rod_weight -
        min_rod_weight
    )

    return {
        "predicted_pump_fillage": predicted_fillage,
        "rod_load_range": actual_load_range
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n================================================")
    print("             TEST PREDICTION")
    print("================================================")

    result = predict_srp(
        well_id="NK-68",
        spm=4.5,
        min_rod_weight=3500,
        max_rod_weight=4750,
        dynamometer_area=15000
    )

    print(f"Well: NK-68")
    print(f"SPM: 4.5")

    print(
        f"Predicted pump fillage: "
        f"{result['predicted_pump_fillage']:.2f}%"
    )

    print(
        f"Rod load range: "
        f"{result['rod_load_range']:.2f} kg"
    )

    print("\n================================================")
    print("          SRP PREDICTOR COMPLETE")
    print("================================================")
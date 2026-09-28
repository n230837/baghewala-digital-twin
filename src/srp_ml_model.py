import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# LOAD REAL SRP DATA
# ============================================================

df = pd.read_csv(
    "data/srp_clean.csv",
    parse_dates=["timestamp"]
)

print("================================================")
print("     SRP PUMP FILLAGE ML MODEL - WELL AWARE")
print("================================================")

print("\nDataset loaded")
print("----------------")
print("Rows:", len(df))
print("Wells:", df["well_id"].nunique())


# ============================================================
# SORT CHRONOLOGICALLY
# ============================================================

df = df.sort_values(
    ["timestamp", "well_id"]
).reset_index(drop=True)


# ============================================================
# FEATURES AND TARGET
# ============================================================

numeric_features = [
    "SPM",
    "min_rod_weight",
    "max_rod_weight",
    "dynamometer_area"
]

categorical_features = [
    "well_id"
]

target = "pump_fillage"


# ============================================================
# CHRONOLOGICAL TRAIN / TEST SPLIT
# ============================================================

split_date = "2026-06-10"

train_df = df[df["timestamp"] < split_date].copy()
test_df = df[df["timestamp"] >= split_date].copy()

X_train = train_df[numeric_features + categorical_features]
y_train = train_df[target]

X_test = test_df[numeric_features + categorical_features]
y_test = test_df[target]


print("\nCHRONOLOGICAL SPLIT")
print("-------------------")

print("Training rows:", len(train_df))
print("Testing rows :", len(test_df))

print(
    "Train period:",
    train_df["timestamp"].min(),
    "to",
    train_df["timestamp"].max()
)

print(
    "Test period :",
    test_df["timestamp"].min(),
    "to",
    test_df["timestamp"].max()
)


# ============================================================
# ONE-HOT ENCODE WELL ID
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "well",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# ============================================================
# TRANSFORM FEATURES
# ============================================================

X_train_encoded = preprocessor.fit_transform(X_train)
X_test_encoded = preprocessor.transform(X_test)


# ============================================================
# GET FEATURE NAMES
# ============================================================

well_names = list(
    preprocessor
    .named_transformers_["well"]
    .get_feature_names_out(categorical_features)
)

feature_names = well_names + numeric_features


# ============================================================
# TRAIN RANDOM FOREST
# ============================================================

print("\nTraining Random Forest...")

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train_encoded,
    y_train
)


# ============================================================
# PREDICTIONS
# ============================================================

predictions = model.predict(
    X_test_encoded
)


# ============================================================
# MODEL PERFORMANCE
# ============================================================

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)

print("\nMODEL PERFORMANCE")
print("-----------------")

print(f"MAE: {mae:.2f}%")
print(f"R² : {r2:.3f}")


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

importance = pd.Series(
    model.feature_importances_,
    index=feature_names
).sort_values(
    ascending=False
)

print("\nTOP FEATURE IMPORTANCE")
print("----------------------")

print(
    importance.head(10)
)


# ============================================================
# SAMPLE PREDICTION
# ============================================================

sample = pd.DataFrame({
    "SPM": [5.0],
    "min_rod_weight": [3500],
    "max_rod_weight": [4500],
    "dynamometer_area": [15000],
    "well_id": ["NK-68"]
})

sample_encoded = preprocessor.transform(sample)

predicted_fillage = model.predict(
    sample_encoded
)[0]

print("\nSAMPLE PREDICTION")
print("-----------------")

print("Well: NK-68")
print("SPM: 5.0")
print("Minimum rod weight: 3500 kg")
print("Maximum rod weight: 4500 kg")
print("Dynamometer area: 15000")

print(
    f"Predicted pump fillage: "
    f"{predicted_fillage:.2f}%"
)


# ============================================================
# TRAIN vs TEST AVERAGES
# ============================================================

print("\nTRAIN vs TEST AVERAGES")
print("----------------------")

comparison_features = numeric_features + [target]

comparison = pd.DataFrame({
    "Train": train_df[comparison_features].mean(),
    "Test": test_df[comparison_features].mean()
})

print(comparison)


# ============================================================
# END
# ============================================================

print("\n================================================")
print("      WELL-AWARE SRP MODEL COMPLETE")
print("================================================")
import pandas as pd
import numpy as np
import psycopg2
import joblib
import time
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

# -----------------------------
# START TIMER
# -----------------------------
start_time = time.time()

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="springdb",  # make sure this matches your DB
    user="myuser",
    password="mypassword",
    port="5432"
)

print("📥 Loading data from PostgreSQL...")
query = "SELECT * FROM pedestrian_with_weather"
df = pd.read_sql(query, conn)
df = df.fillna(0)
conn.close()

print("Initial dataset size:", len(df))

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
print("🧠 Performing feature engineering...")

# Sort correctly for time-series
df = df.sort_values(by=["location_id", "sensing_date", "hour_day"])

# Create datetime column
df["datetime"] = pd.to_datetime(df["sensing_date"]) + pd.to_timedelta(df["hour_day"], unit="h")

# Lag Features
df["lag_1"] = df.groupby("location_id")["total_count"].shift(1)
df["lag_3"] = df.groupby("location_id")["total_count"].shift(3)

# Rolling Mean (safe version)
df["rolling_mean_3"] = (
    df.groupby("location_id")["total_count"]
      .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
)

# Peak hour indicator
df["is_peak_hour"] = ((df["hour_day"] >= 17) & (df["hour_day"] <= 20)).astype(int)

# Weekend flag
df["is_weekend"] = (df["weekday"] >= 5).astype(int)

# Fill lag NaNs instead of dropping entire dataset
df["lag_1"] = df["lag_1"].fillna(df["total_count"])
df["lag_3"] = df["lag_3"].fillna(df["total_count"])

print("Dataset size after feature engineering:", len(df))

# -----------------------------
# FEATURE SELECTION
# -----------------------------
features = [
    "hour_day",
    "weekday",
    "month",
    "lag_1",
    "lag_3",
    "rolling_mean_3",
    "is_peak_hour",
    "is_weekend",
    "temperature",
    "rainfall",
    "humidity",
    "windspeed",
    "cloudcover"
]

X = df[features]
y = df["total_count"]

# -----------------------------
# TIME-SERIES SPLIT (IMPORTANT)
# -----------------------------
print("📊 Splitting data (time-based split)...")

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training size:", len(X_train))
print("Testing size:", len(X_test))

# -----------------------------
# TRAIN MODEL
# -----------------------------
print("🚀 Training XGBoost Model...")

model = XGBRegressor(
    n_estimators=400,
    max_depth=10,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    tree_method="hist"  # faster for large datasets
)

model.fit(X_train, y_train)

# -----------------------------
# EVALUATION
# -----------------------------
print("📈 Evaluating model...")

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"📊 MAE: {mae:.4f}")
print(f"📊 R2 Score: {r2:.4f}")

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------
print("\n🔍 Feature Importance:")
for feature, importance in zip(features, model.feature_importances_):
    print(f"{feature}: {importance:.4f}")

# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(model, "ml_models/xgboost_model.pkl")

print("\n✅ Model trained and saved successfully!")

end_time = time.time()
print(f"⏱ Training Time: {(end_time - start_time)/60:.2f} minutes")
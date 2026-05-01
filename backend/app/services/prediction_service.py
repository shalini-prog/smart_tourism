import os
import joblib
import pandas as pd
from app.database import SessionLocal

MODEL_PATH = "ml_models/xgboost_model.pkl"
model = None


# ==========================================================
# LOAD MODEL
# ==========================================================
def load_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print("✅ ML model loaded")
        else:
            raise FileNotFoundError("❌ Model not found")


# ==========================================================
# GET LOCATION CAPACITY (95th Percentile)
# ==========================================================
def get_location_capacity(location_id, db):
    query = f"""
    SELECT PERCENTILE_CONT(0.95)
    WITHIN GROUP (ORDER BY total_count) AS max_capacity
    FROM pedestrian_data
    WHERE location_id = {location_id}
    """
    df = pd.read_sql(query, db.bind)
    capacity = df["max_capacity"].iloc[0]
    return capacity if capacity and capacity > 0 else 1


# ==========================================================
# DYNAMIC RISK CLASSIFICATION
# ==========================================================
def classify_dynamic_risk(prediction, capacity):
    ratio = prediction / capacity

    if ratio < 0.4:
        return "Low", ratio
    elif ratio < 0.7:
        return "Medium", ratio
    elif ratio < 0.9:
        return "High", ratio
    else:
        return "Critical", ratio


# ==========================================================
# BUILD FEATURES
# ==========================================================
def build_features(hour, weekday, month, lag_1, lag_3, rolling_mean_3):
    return [[
        hour,
        weekday,
        month,
        lag_1,
        lag_3,
        rolling_mean_3,
        1 if 17 <= hour <= 20 else 0,
        1 if weekday >= 5 else 0,
        0, 0, 0, 0, 0
    ]]


# ==========================================================
# SINGLE LOCATION PREDICTION
# ==========================================================
def predict_crowd(location_id: int):
    load_model()
    db = SessionLocal()

    query = f"""
    SELECT *
    FROM pedestrian_data
    WHERE location_id = {location_id}
    ORDER BY sensing_date DESC, hour_day DESC
    LIMIT 5
    """

    df = pd.read_sql(query, db.bind)

    if len(df) < 3:
        db.close()
        return {"error": "Not enough historical data"}

    df = df.sort_values(by=["sensing_date", "hour_day"])
    latest = df.iloc[-1]

    lag_1 = latest["total_count"]
    lag_3 = df.iloc[-3]["total_count"]
    rolling_mean_3 = df["total_count"].tail(3).mean()

    features = build_features(
        latest["hour_day"],
        latest["weekday"],
        latest["month"],
        lag_1,
        lag_3,
        rolling_mean_3
    )

    prediction = max(0, float(model.predict(features)[0]))
    capacity = get_location_capacity(location_id, db)
    risk_level, ratio = classify_dynamic_risk(prediction, capacity)

    db.close()

    return {
        "location_id": location_id,
        "predicted_next_hour": prediction,
        "capacity": float(capacity),
        "utilization_ratio": round(ratio, 2),
        "risk_level": risk_level
    }


# ==========================================================
# 24-HOUR FORECAST
# ==========================================================
def multi_hour_forecast(location_id: int, hours: int = 24):
    load_model()
    db = SessionLocal()

    query = f"""
    SELECT *
    FROM pedestrian_data
    WHERE location_id = {location_id}
    ORDER BY sensing_date DESC, hour_day DESC
    LIMIT 3
    """

    df = pd.read_sql(query, db.bind)

    if len(df) < 3:
        db.close()
        return {"error": "Not enough historical data"}

    df = df.sort_values(by=["sensing_date", "hour_day"])

    history = df["total_count"].tolist()
    latest = df.iloc[-1]

    current_hour = int(latest["hour_day"])
    current_weekday = int(latest["weekday"])
    current_month = int(latest["month"])

    forecast = []

    for step in range(1, hours + 1):

        next_hour = (current_hour + 1) % 24

        if next_hour == 0:
            current_weekday = (current_weekday + 1) % 7

        lag_1 = history[-1]
        lag_3 = history[-3]
        rolling_mean_3 = sum(history[-3:]) / 3

        features = build_features(
            next_hour,
            current_weekday,
            current_month,
            lag_1,
            lag_3,
            rolling_mean_3
        )

        prediction = max(0, float(model.predict(features)[0]))
        history.append(prediction)

        forecast.append({
            "hour_ahead": step,
            "predicted_crowd": prediction
        })

        current_hour = next_hour

    db.close()
    return forecast


# ==========================================================
# CITY-WIDE PREDICTION (WITH GEO DATA)
# ==========================================================
def predict_all_locations():
    load_model()
    db = SessionLocal()

    # JOIN metadata to get coordinates
    query = """
    SELECT lm.location_id, lm.latitude, lm.longitude
    FROM location_metadata lm
    """

    locations_df = pd.read_sql(query, db.bind)

    results = []

    for _, row in locations_df.iterrows():

        location_id = row["location_id"]
        latitude = row["latitude"]
        longitude = row["longitude"]

        query_data = f"""
        SELECT *
        FROM pedestrian_data
        WHERE location_id = {location_id}
        ORDER BY sensing_date DESC, hour_day DESC
        LIMIT 5
        """

        df = pd.read_sql(query_data, db.bind)

        if len(df) < 3:
            continue

        df = df.sort_values(by=["sensing_date", "hour_day"])
        latest = df.iloc[-1]

        lag_1 = latest["total_count"]
        lag_3 = df.iloc[-3]["total_count"]
        rolling_mean_3 = df["total_count"].tail(3).mean()

        features = build_features(
            latest["hour_day"],
            latest["weekday"],
            latest["month"],
            lag_1,
            lag_3,
            rolling_mean_3
        )

        prediction = max(0, float(model.predict(features)[0]))
        capacity = get_location_capacity(location_id, db)
        risk_level, ratio = classify_dynamic_risk(prediction, capacity)

        results.append({
            "location_id": int(location_id),
            "latitude": float(latitude),
            "longitude": float(longitude),
            "predicted_next_hour": prediction,
            "capacity": float(capacity),
            "utilization_ratio": round(ratio, 2),
            "risk_level": risk_level
        })

    # SORT by utilization
    results = sorted(results, key=lambda x: x["utilization_ratio"], reverse=True)

    db.close()

    return {
        "locations": results
    }
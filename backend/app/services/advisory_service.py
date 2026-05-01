import math
import pandas as pd
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.services.prediction_service import (
    multi_hour_forecast,
    predict_crowd
)
from app.services.weather_service import get_24_hour_weather_forecast


# ============================================
# UTILITY — HAVERSINE DISTANCE
# ============================================

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ============================================
# LOAD LOCATION COORDINATES
# ============================================

def get_location_coordinates(db):
    query = """
        SELECT location_id, latitude, longitude
        FROM location_metadata
    """
    df = pd.read_sql(query, db.bind)

    coords = {}
    for _, row in df.iterrows():
        coords[row["location_id"]] = (
            float(row["latitude"]),
            float(row["longitude"])
        )

    return coords


# ============================================
# TREND DETECTION
# ============================================

def detect_trend(forecast):
    first_6 = [f["predicted_crowd"] for f in forecast[:6]]

    if first_6[-1] < first_6[0]:
        return "decreasing"
    elif first_6[-1] > first_6[0]:
        return "increasing"
    return "stable"


# ============================================
# COMFORT SCORE ENGINE
# ============================================

def calculate_comfort(utilization, weather):
    score = 10

    if utilization > 0.7:
        score -= 3
    elif utilization > 0.4:
        score -= 1

    if weather["rain"] > 0:
        score -= 3

    if weather["temperature"] < 15 or weather["temperature"] > 32:
        score -= 2

    if weather["windspeed"] > 20:
        score -= 1

    return round(max(score, 1), 1)


# ============================================
# BEST VISIT WINDOW (2-HOUR WINDOW)
# ============================================

def find_best_window(forecast, weather):
    best_score = float("inf")
    best_index = 0

    for i in range(len(forecast) - 1):
        crowd_avg = (
            forecast[i]["predicted_crowd"]
            + forecast[i + 1]["predicted_crowd"]
        ) / 2

        rain_penalty = (
            weather[i]["rain"] + weather[i + 1]["rain"]
        )

        score = crowd_avg + rain_penalty * 200

        if score < best_score:
            best_score = score
            best_index = i

    now = datetime.now()
    start_time = now + timedelta(hours=forecast[best_index]["hour_ahead"])
    end_time = start_time + timedelta(hours=2)

    return start_time.strftime("%H:%M") + " - " + end_time.strftime("%H:%M")


# ============================================
# SMART ALTERNATIVE RECOMMENDATION
# ============================================

def recommend_alternative(location_id):
    db = SessionLocal()

    coords = get_location_coordinates(db)
    current = predict_crowd(location_id)

    if location_id not in coords:
        db.close()
        return None

    current_lat, current_lon = coords[location_id]

    candidates = []

    for loc_id, (lat, lon) in coords.items():
        if loc_id == location_id:
            continue

        data = predict_crowd(loc_id)

        if data["utilization_ratio"] < 0.4:
            distance = haversine(current_lat, current_lon, lat, lon)

            candidates.append({
                "location_id": loc_id,
                "distance_km": round(distance, 2),
                "current_crowd": data["predicted_next_hour"]
            })

    db.close()

    if not candidates:
        return None

    candidates.sort(key=lambda x: x["distance_km"])
    return candidates[0]


# ============================================
# MAIN PRODUCTION ADVISORY
# ============================================

def generate_smart_advisory(location_id: int):

    crowd_now = predict_crowd(location_id)
    forecast = multi_hour_forecast(location_id, hours=24)
    weather = get_24_hour_weather_forecast(location_id)

    trend = detect_trend(forecast)

    best_window = find_best_window(forecast, weather)

    comfort = calculate_comfort(
        crowd_now["utilization_ratio"],
        weather[0]
    )

    # Human-readable status
    status = (
        f"{crowd_now['risk_level']} crowd "
        f"({round(crowd_now['utilization_ratio'] * 100)}% capacity)"
    )

    if trend == "decreasing":
        trend_msg = "Crowd expected to decrease over next few hours."
    elif trend == "increasing":
        trend_msg = "Crowd expected to increase."
    else:
        trend_msg = "Crowd expected to remain stable."

    weather_summary = (
        f"Temperature around {weather[0]['temperature']}°C, "
        f"Cloud cover {weather[0]['cloudcover']}%, "
        f"No rainfall expected."
    )

    alternative = None

    if (
        crowd_now["utilization_ratio"] > 0.6
        or comfort < 6
        or weather[0]["rain"] > 0
    ):
        alternative = recommend_alternative(location_id)

    return {
        "location_id": location_id,
        "current_status": status,
        "trend": trend_msg,
        "best_time_to_visit": best_window,
        "weather_summary": weather_summary,
        "comfort_score": comfort,
        "final_recommendation": (
            f"Visit during {best_window} for optimal experience."
        ),
        "alternative_option": alternative
    }
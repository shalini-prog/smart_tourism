import requests
from app.database import SessionLocal
import pandas as pd


# ============================================
# DEFAULT FALLBACK (Melbourne CBD)
# ============================================

DEFAULT_LAT = -37.8136
DEFAULT_LON = 144.9631


# ============================================
# GET LOCATION COORDINATES FROM DB
# ============================================

def get_location_coordinates(location_id: int):
    db = SessionLocal()

    query = f"""
        SELECT latitude, longitude
        FROM location_metadata
        WHERE location_id = {location_id}
    """

    df = pd.read_sql(query, db.bind)
    db.close()

    if len(df) == 0:
        return DEFAULT_LAT, DEFAULT_LON

    return float(df["latitude"].iloc[0]), float(df["longitude"].iloc[0])


# ============================================
# FETCH 24-HOUR WEATHER FORECAST
# ============================================

def get_24_hour_weather_forecast(location_id: int):

    lat, lon = get_location_coordinates(location_id)

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,precipitation,cloudcover,windspeed_10m"
        f"&forecast_days=2"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        hourly = data.get("hourly", {})

        weather = []

        for i in range(min(24, len(hourly.get("temperature_2m", [])))):

            weather.append({
                "hour_ahead": i + 1,
                "temperature": float(hourly["temperature_2m"][i]),
                "rain": float(hourly["precipitation"][i]),
                "cloudcover": float(hourly["cloudcover"][i]),
                "windspeed": float(hourly["windspeed_10m"][i])
            })

        return weather

    except Exception as e:
        print("⚠ Weather API failed:", str(e))

        # Fallback safe weather
        return [{
            "hour_ahead": i + 1,
            "temperature": 22.0,
            "rain": 0.0,
            "cloudcover": 30.0,
            "windspeed": 5.0
        } for i in range(24)]
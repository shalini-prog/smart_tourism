import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

LATITUDE = -37.8136
LONGITUDE = 144.9631

START_YEAR = 2024
END_YEAR = 2026

today = datetime.today().date()

print("🌦 Starting Melbourne weather data ingestion...")

all_data = []

for year in range(START_YEAR, END_YEAR + 1):

    start_date = f"{year}-01-01"

    # If current year → only fetch until today
    if year == today.year:
        end_date = str(today)
    else:
        end_date = f"{year}-12-31"

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=temperature_2m,relativehumidity_2m,rain,windspeed_10m,cloudcover"
        f"&timezone=Australia/Sydney"
    )

    print(f"Fetching weather for {year}...")

    response = requests.get(url)
    data = response.json()

    # 🔥 SAFE CHECK
    if "hourly" not in data:
        print("API Error:", data)
        continue

    hourly = data["hourly"]

    df = pd.DataFrame({
        "weather_datetime": hourly["time"],
        "temperature": hourly["temperature_2m"],
        "humidity": hourly["relativehumidity_2m"],
        "rainfall": hourly["rain"],
        "windspeed": hourly["windspeed_10m"],
        "cloudcover": hourly["cloudcover"]
    })

    df["weather_datetime"] = pd.to_datetime(df["weather_datetime"])

    all_data.append(df)

weather_df = pd.concat(all_data)

print("Total weather rows fetched:", len(weather_df))

# -----------------------------
# DATABASE INSERTION
# -----------------------------
conn = psycopg2.connect(
    host="localhost",
    database="springdb",
    user="myuser",
    password="mypassword",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    weather_datetime TIMESTAMP,
    temperature FLOAT,
    rainfall FLOAT,
    humidity FLOAT,
    windspeed FLOAT,
    cloudcover FLOAT
);
""")

conn.commit()

insert_query = """
INSERT INTO weather_data (
    weather_datetime,
    temperature,
    rainfall,
    humidity,
    windspeed,
    cloudcover
)
VALUES (%s,%s,%s,%s,%s,%s)
"""

records = weather_df.values.tolist()

execute_batch(cursor, insert_query, records, page_size=10000)

conn.commit()
cursor.close()
conn.close()

print("✅ Weather data inserted successfully!")
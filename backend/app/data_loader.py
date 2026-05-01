import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

# CSV Path
CSV_PATH = r"E:\pedestrian-counting-system-monthly-counts-per-hour.csv"

# DB Connection
conn = psycopg2.connect(
    host="localhost",
    database="springdb",
    user="myuser",
    password="mypassword",
    port="5432"
)

cursor = conn.cursor()

print("📂 Reading CSV...")
df = pd.read_csv("D:/pedestrian-counting-system-monthly-counts-per-hour.csv")

print("🔧 Cleaning & Feature Engineering...")

# Rename columns properly (adjust if needed)
df.columns = df.columns.str.strip()

df["Sensing_Date"] = pd.to_datetime(df["Sensing_Date"])

df["weekday"] = df["Sensing_Date"].dt.weekday
df["month"] = df["Sensing_Date"].dt.month

df = df.rename(columns={
    "Location_ID": "location_id",
    "HourDay": "hour_day",
    "Direction_1": "direction_1",
    "Direction_2": "direction_2",
    "Total_of_Directions": "total_count"
})

records = df[[
    "location_id",
    "Sensing_Date",
    "hour_day",
    "weekday",
    "month",
    "direction_1",
    "direction_2",
    "total_count"
]].values.tolist()

print("🚀 Inserting into PostgreSQL in batches...")

insert_query = """
INSERT INTO pedestrian_data (
    location_id,
    sensing_date,
    hour_day,
    weekday,
    month,
    direction_1,
    direction_2,
    total_count
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
"""

execute_batch(cursor, insert_query, records, page_size=10000)

conn.commit()
cursor.close()
conn.close()

print("✅ Data import completed successfully!")
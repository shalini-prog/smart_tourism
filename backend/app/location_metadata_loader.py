import pandas as pd
import psycopg2

CSV_PATH = r"D:\pedestrian-counting-system-monthly-counts-per-hour.csv"

DB_CONFIG = {
    "host": "localhost",
    "database": "springdb",
    "user": "myuser",
    "password": "mypassword",   # change this
    "port": "5432"
}

print("📥 Loading CSV...")
df = pd.read_csv(CSV_PATH)

# Extract unique metadata
meta = df[["Location_ID", "Sensor_Name", "Location"]].drop_duplicates()

# Split latitude & longitude
meta[["latitude", "longitude"]] = meta["Location"].str.split(",", expand=True)

meta["latitude"] = meta["latitude"].astype(float)
meta["longitude"] = meta["longitude"].astype(float)

# Rename columns to match DB table
meta = meta.rename(columns={
    "Location_ID": "location_id",
    "Sensor_Name": "sensor_name"
})

meta = meta[["location_id", "sensor_name", "latitude", "longitude"]]

print("🔌 Connecting to database...")
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

for _, row in meta.iterrows():
    cur.execute("""
        INSERT INTO location_metadata (location_id, latitude, longitude)
        VALUES (%s, %s, %s)
        ON CONFLICT (location_id) DO NOTHING;
    """, (
        int(row.location_id),
        float(row.latitude),
        float(row.longitude)
    ))

conn.commit()
cur.close()
conn.close()

print("✅ Location metadata inserted successfully!")
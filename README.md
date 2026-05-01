🚀 AI Smart Tourism System

An AI-powered crowd prediction and tourism optimization system that helps users make smarter travel decisions by analyzing crowd density, weather conditions, and historical trends.

📌 Project Overview

This system predicts crowd levels at tourist locations and provides:

📊 Next-hour crowd prediction
🌍 City-wide crowd insights
📅 24-hour crowd forecasting
🧠 Smart advisory (best time, comfort score, alternatives)

It combines Machine Learning + Weather Data + Real-time Intelligence to improve tourist experience and reduce overcrowding.

🧠 Key Features

🔮 Crowd Prediction

Predict next-hour crowd using ML model (XGBoost)
Uses historical pedestrian data

🌐 City-Wide Analysis

Compare crowd levels across all locations
Helps users choose less crowded places

⏳ 24-Hour Forecast

Predicts crowd trends for the next 24 hours

🤖 Smart Advisory System

Best time to visit
Comfort score (based on weather + crowd)
Trend detection (increasing/decreasing crowd)
Alternative location recommendation

🏗️ System Architecture

User Request
     ↓
FastAPI Backend
     ↓
Prediction Service (ML Model)
     ↓
Weather Service (Open-Meteo API)
     ↓
Advisory Engine (Decision Layer)
     ↓
Response (JSON)

⚙️ Tech Stack

Backend: FastAPI
Database: PostgreSQL
Machine Learning: XGBoost
Data Processing: Pandas, NumPy
API Integration: Open-Meteo Weather API
ORM: SQLAlchemy

📁 Project Structure

app/
│
├── routers/
│   └── crowd_routes.py
│
├── services/
│   ├── prediction_service.py
│   ├── advisory_service.py
│   └── weather_service.py
│
├── database.py
│
ml_models/
│   └── xgboost_model.pkl
│
data_scripts/
│   ├── load_pedestrian_data.py
│   ├── load_location_metadata.py
│   └── load_weather_data.py
│
main.py

📡 API Endpoints

🔹 1. Predict Crowd (Single Location)

GET /predict/{location_id}

🔹 2. City-Wide Prediction

GET /predict_all

🔹 3. 24-Hour Forecast

GET /forecast/{location_id}

🔹 4. Smart Advisory

GET /smart_advisory/{location_id}

🧠 Machine Learning Model

Model: XGBoost Regressor

Features used:

Hour of day
Weekday
Month
Lag features (lag_1, lag_3)
Rolling mean
Peak hour indicator
Weekend flag
Weather data

📊 Model Performance

MAE: Low error (good prediction accuracy)
R² Score: High (strong model fit)

🌦️ Weather Integration

Uses Open-Meteo API
Parameters:

Temperature
Rainfall
Cloud cover
Wind speed

Fallback system ensures reliability if API fails.

🧠 Smart Advisory Logic

The advisory engine provides:

📉 Trend detection (increasing/decreasing/stable)
🕒 Best 2-hour visit window
🌡️ Weather-based comfort score
🔄 Alternative recommendations (nearby low-crowd locations)

👉 Core logic implemented in:


🤖 Prediction Engine

Handles:

Crowd prediction
Multi-hour forecasting
Risk classification (Low → Critical)
Capacity estimation

👉 Core logic implemented in:


🗄️ Database Schema

pedestrian_data

location_id
sensing_date
hour_day
total_count
weekday
month

location_metadata

location_id
latitude
longitude

weather_data

datetime
temperature
rainfall
humidity
windspeed
cloudcover

🚀 Setup Instructions

1️⃣ Clone Repository

git clone https://github.com/your-username/ai-tourism-system.git
cd ai-tourism-system

2️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Setup Database

Install PostgreSQL

Create database:

CREATE DATABASE springdb;

Update credentials in:

app/database.py

5️⃣ Load Data

Run scripts:

python load_location_metadata.py
python load_pedestrian_data.py
python load_weather_data.py

6️⃣ Train Model

python train_model.py

7️⃣ Run Server

uvicorn main:app --reload

📊 Example Output (Smart Advisory)

{
  "location_id": 12,
  "current_status": "High crowd (82% capacity)",
  "trend": "Crowd expected to decrease",
  "best_time_to_visit": "16:00 - 18:00",
  "weather_summary": "Temperature around 28°C",
  "comfort_score": 7.5,
  "final_recommendation": "Visit during 16:00 - 18:00",
  "alternative_option": {
    "location_id": 5,
    "distance_km": 1.2,
    "current_crowd": 120
  }
}

🎯 Future Enhancements
📱 Mobile App Integration
🗺️ Real-time Map Visualization
🔔 Push Notifications for crowd alerts
📡 Live IoT sensor integration
🧠 Deep Learning models
👨‍💻 Author

Developed as part of an AI-based Smart Tourism Optimization Project

📜 License

This project is open-source and available under the MIT License.

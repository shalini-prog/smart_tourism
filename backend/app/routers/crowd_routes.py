from fastapi import APIRouter
from app.services.prediction_service import (
    predict_crowd,
    predict_all_locations,
    multi_hour_forecast
)
from app.services.advisory_service import generate_smart_advisory

router = APIRouter()


# ==========================================================
# SINGLE LOCATION NEXT-HOUR PREDICTION
# ==========================================================
@router.get("/predict/{location_id}")
def get_prediction(location_id: int):
    return predict_crowd(location_id)


# ==========================================================
# CITY-WIDE PREDICTION
# ==========================================================
@router.get("/predict_all")
def get_all_predictions():
    return predict_all_locations()


# ==========================================================
# 24-HOUR FORECAST
# ==========================================================
@router.get("/forecast/{location_id}")
def get_24_hour_forecast(location_id: int):
    forecast = multi_hour_forecast(location_id, hours=24)

    return {
        "location_id": location_id,
        "forecast_24_hours": forecast
    }


# ==========================================================
# SMART ADVISORY (FINAL INTELLIGENCE LAYER)
# ==========================================================
@router.get("/smart_advisory/{location_id}")
def smart_advisory(location_id: int):
    return generate_smart_advisory(location_id)
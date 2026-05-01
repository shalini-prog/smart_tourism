def recommend_alternative(current_location, predicted_density):

    nearby_locations = {
        "Marina Beach": [
            {"name": "Santhome Church", "crowd": 42},
            {"name": "Elliots Beach", "crowd": 55},
            {"name": "Fort St George", "crowd": 38}
        ]
    }

    if predicted_density > 80:
        return sorted(nearby_locations[current_location], key=lambda x: x["crowd"])

    return []
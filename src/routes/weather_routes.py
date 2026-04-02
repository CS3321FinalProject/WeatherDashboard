from flask import request, jsonify
import requests

# import the validators (if/else) logic from validators.py
from src.utils.validators import _validate_city, _validate_coords

from src.services.weather_service import (
    get_weather_by_city,
    get_weather_by_coords,
    get_forecast_by_city
)

def register_weather_routes(app):

    @app.route("/weather", methods=["GET"])
    def get_weather():
        city = request.args.get("city")

        error = _validate_city(city)
        if error:
            return jsonify({"error": error}), 400

        try:
            weather_data = get_weather_by_city(city.strip())

            if not weather_data or "currentConditions" not in weather_data:
                return jsonify({"error": "City not found"}), 404

            current = weather_data["currentConditions"]

            return jsonify({
                "city": weather_data["resolvedAddress"],
                "temperature": current["temp"],
                "conditions": current["conditions"],
                "humidity": current["humidity"],
                "wind_speed": current["windspeed"]
            })

        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500


    @app.route("/weather/coords", methods=["GET"])
    def get_weather_coords():
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        error = _validate_coords(lat, lon)
        if error:
            return jsonify({"error": error}), 400

        try:
            weather_data = get_weather_by_coords(float(lat), float(lon))

            if not weather_data or "currentConditions" not in weather_data:
                return jsonify({"error": "Location not found"}), 404

            current = weather_data["currentConditions"]

            return jsonify({
                "location": weather_data["resolvedAddress"],
                "latitude": weather_data["latitude"],
                "longitude": weather_data["longitude"],
                "temperature": current["temp"],
                "conditions": current["conditions"],
                "humidity": current["humidity"],
                "wind_speed": current["windspeed"]
            })

        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500


    @app.route("/forecast", methods=["GET"])
    def get_forecast():
        city = request.args.get("city")

        error = _validate_city(city)
        if error:
            return jsonify({"error": error}), 400

        try:
            forecast_data = get_forecast_by_city(city.strip())

            if not forecast_data or "days" not in forecast_data:
                return jsonify({"error": "City not found"}), 404

            days = forecast_data["days"][:5]

            cleaned = []
            for day in days:
                cleaned.append({
                    "date": day["datetime"],
                    "temp": day["temp"],
                    "temp_max": day["tempmax"],
                    "temp_min": day["tempmin"],
                    "conditions": day["conditions"]
                })

            return jsonify({
                "city": forecast_data["resolvedAddress"],
                "forecast": cleaned
            })

        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500
from flask import request, jsonify, abort
import requests

from WeatherDashboard.utils.validators import _validate_city, _validate_coords
from WeatherDashboard.services.http_cats_service import get_cat_url
from WeatherDashboard.services.weather_service import (
    get_weather_by_city,
    get_weather_by_coords,
    get_forecast_by_city
)

def register_weather_routes(app):

    # ---------------- WEATHER BY CITY ----------------
    @app.route("/weather", methods=["GET"])
    def get_weather():
        city = request.args.get("city")

        error = _validate_city(city)
        if error:
            abort(400, description=error)

        try:
            result = get_weather_by_city(city.strip())
            weather_data = result.get("data")

            if not weather_data or not weather_data.get("currentConditions"):
                abort(404, description="City not found")

            current = weather_data["currentConditions"]

            return jsonify({
                "city": weather_data.get("resolvedAddress"),
                "temperature": current.get("temp"),
                "conditions": current.get("conditions"),
                "humidity": current.get("humidity"),
                "wind_speed": current.get("windspeed"),
                "cat_url": get_cat_url(200)
            })

        except requests.exceptions.RequestException:
            abort(500, description="Internal server error")


    # ---------------- WEATHER BY COORDS ----------------
    @app.route("/weather/coords", methods=["GET"])
    def get_weather_coords():
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        error = _validate_coords(lat, lon)
        if error:
            abort(400, description=error)

        try:
            result = get_weather_by_coords(float(lat), float(lon))
            weather_data = result.get("data")

            if not weather_data or not weather_data.get("currentConditions"):
                abort(404, description="Location not found")

            current = weather_data["currentConditions"]

            return jsonify({
                "location": weather_data.get("resolvedAddress"),
                "latitude": weather_data.get("latitude"),
                "longitude": weather_data.get("longitude"),
                "temperature": current.get("temp"),
                "conditions": current.get("conditions"),
                "humidity": current.get("humidity"),
                "wind_speed": current.get("windspeed"),
                "cat_url": get_cat_url(200)
            })

        except requests.exceptions.RequestException:
            abort(500, description="Internal server error")


    # ---------------- FORECAST ----------------
    @app.route("/forecast", methods=["GET"])
    def get_forecast():
        city = request.args.get("city")

        error = _validate_city(city)
        if error:
            abort(400, description=error)

        try:
            result = get_forecast_by_city(city.strip())
            forecast_data = result.get("data")

            if not forecast_data or not forecast_data.get("days"):
                abort(404, description="City not found")

            days = forecast_data["days"][:5]

            cleaned = []
            for day in days:
                cleaned.append({
                    "date": day.get("datetime"),
                    "temp": day.get("temp"),
                    "temp_max": day.get("tempmax"),
                    "temp_min": day.get("tempmin"),
                    "conditions": day.get("conditions"),
                    "cat_url": get_cat_url(200)
                })

            return jsonify({
                "city": forecast_data.get("resolvedAddress"),
                "forecast": cleaned,
                "cat_url": get_cat_url(200)
            })

        except requests.exceptions.RequestException:
            abort(500, description="Internal server error")
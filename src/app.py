from flask import Flask, request, jsonify 
from dotenv import load_dotenv
from src.services.weather_service import (get_weather_by_city,get_weather_by_coords,get_forecast_by_city)
import os
import requests


load_dotenv()



def create_app():
#    load_dotenv()

    app = Flask(__name__)
    @app.route("/")
    def home():
        return {"message": "Weather Dashboard API is running"}
    

    @app.route("/weather", methods=["GET"]  )
    def get_weather():
        city = request.args.get("city")
        if not city:
            return jsonify({"error": "City parameter is required"}), 400
        if len(city) < 2:
            return jsonify({"error": "City name must be at least 2 characters long"}), 400
        if not city.replace(" ", "").isalpha():
            return jsonify({"error": "Invalid city name"}), 400
        try:
            weather_data = get_weather_by_city(city)
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

    @app.route("/weather/coords", methods=["GET"]   )
    def get_weather_coords():
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        if not lat or not lon:
            return jsonify({"error": "Latitude and longitude parameters are required"}), 400
        try:
            weather_data = get_weather_by_coords(lat, lon)

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

    @app.route("/forecast", methods=["GET"]  )
    def get_forecast():
        city = request.args.get("city")
        if not city:
            return jsonify({"error": "City parameter is required"}), 400
        if len(city) < 2:
            return jsonify({"error": "City name must be at least 2 characters long"}), 400
        try:
            forecast_data = get_forecast_by_city(city)

            days = forecast_data["days"][:5]  # 5-day forecast

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
        
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "message": "Weather API is alive"
        }), 200
        
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

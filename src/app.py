from flask import Flask
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={api_key}&unitGroup=us&include=current"
    response = requests.get(url)
    return response.json()

def create_app():
#    load_dotenv()

    app = Flask(__name__)
    @app.route("/")
    def home():
        return {"message": "Weather Dashboard API is running"}
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

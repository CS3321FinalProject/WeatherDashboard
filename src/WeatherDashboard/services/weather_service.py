import os
import requests
from WeatherDashboard.services.http_cats_service import get_cat_url

# Get the API key from environment variables
def get_api_key():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY not configured")
    return api_key

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"


# Get current weather for a city
def get_weather_by_city(city):
    api_key = get_api_key()

    url = f"{BASE_URL}/{city}"
    params = {
        "key": api_key,
        "unitGroup": "us",
        "include": "current"
    }

    response = requests.get(url, params=params)

    return {
        "status_code": response.status_code,
        "data": response.json()
    }


# Get current weather using latitude and longitude
def get_weather_by_coords(lat, lon):
    api_key = get_api_key()

    location = f"{lat},{lon}"
    url = f"{BASE_URL}/{location}"
    params = {
        "key": api_key,
        "unitGroup": "us",
        "include": "current"
    }

    response = requests.get(url, params=params)

    return {
        "status_code": response.status_code,
        "data": response.json()
    }

# Get forecast for a city
def get_forecast_by_city(city):
    api_key = get_api_key()

    url = f"{BASE_URL}/{city}"
    params = {
        "key": api_key,
        "unitGroup": "us",
        "include": "days"
    }

    response = requests.get(url, params=params)
    
    return {
        "status_code": response.status_code,
        "data": response.json()
    }
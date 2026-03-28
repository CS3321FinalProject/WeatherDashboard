import os
import requests

# Get the API key from environment variables
def get_api_key():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY not found. Please set it in your environment.")
    return api_key


# Get current weather for a city
# Example: get_weather_by_city("London")
def get_weather_by_city(city):
    api_key = get_api_key()

    # Call OpenWeatherMap API with the city name
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,         # city name
        "appid": api_key,  # our API key from environment
        "units": "imperial"  # fahrenheit, change to "metric" for celsius
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # throws error if something goes wrong
    return response.json()       # return weather data as JSON


# Get current weather using latitude and longitude
# Example: get_weather_by_coords(40.7128, -74.0060)
def get_weather_by_coords(lat, lon):
    api_key = get_api_key()

    # Call OpenWeatherMap API with coordinates instead of city name
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,        # latitude
        "lon": lon,        # longitude
        "appid": api_key,
        "units": "imperial"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


# Get 5-day weather forecast for a city
# Example: get_forecast_by_city("New York")
def get_forecast_by_city(city):
    api_key = get_api_key()

    # Call the forecast endpoint (gives forecast every 3 hours for 5 days)
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


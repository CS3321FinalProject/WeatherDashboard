import pytest# ---- TESTS ----
import os
from unittest.mock import patch, Mock
from src.services.weather_service import (
    get_weather_by_city,
    get_weather_by_coords,
    get_forecast_by_city
)

# ---- FAKE DATA (pretend API responses) ----

# Fake weather data (used for city and coords tests)
MOCK_WEATHER = {
    "name": "London",
    "main": {"temp": 43.2, "humidity": 65},
    "weather": [{"main": "Clouds", "description": "overcast clouds"}],
    "wind": {"speed": 13.94}
}

# Fake forecast data (used for forecast test)
MOCK_FORECAST = {
    "city": {"name": "London"},
    "list": [
        {
            "main": {"temp": 43.2, "humidity": 65},
            "weather": [{"main": "Clouds", "description": "overcast clouds"}]
        }
    ]
}


# ---- TESTS ----

# Test 1: get_weather_by_city()
@patch.dict(os.environ, {"WEATHER_API_KEY": "fake-key"})
@patch("src.services.weather_service.requests.get")
def test_get_weather_by_city(mock_get):
    # Fake the API response
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = MOCK_WEATHER

    result = get_weather_by_city("London")

    assert result["name"] == "London"
    assert result["main"]["temp"] == 43.2
    mock_get.assert_called_once()


# Test 2: get_weather_by_coords()
@patch.dict(os.environ, {"WEATHER_API_KEY": "fake-key"})
@patch("src.services.weather_service.requests.get")
def test_get_weather_by_coords(mock_get):
    # Fake the API response
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = MOCK_WEATHER

    result = get_weather_by_coords(51.5085, -0.1257)

    assert result["main"]["temp"] == 43.2
    assert result["weather"][0]["main"] == "Clouds"
    mock_get.assert_called_once()


# Test 3: get_forecast_by_city()
@patch.dict(os.environ, {"WEATHER_API_KEY": "fake-key"})
@patch("src.services.weather_service.requests.get")
def test_get_forecast_by_city(mock_get):
    # Fake the API response
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = MOCK_FORECAST

    result = get_forecast_by_city("London")

    assert result["city"]["name"] == "London"
    assert len(result["list"]) > 0
    mock_get.assert_called_once()

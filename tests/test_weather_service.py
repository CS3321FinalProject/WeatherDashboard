import pytest
import os
from unittest.mock import patch, Mock
from WeatherDashboard.services.weather_service import (
    get_weather_by_city,
    get_weather_by_coords,
    get_forecast_by_city
)

MOCK_API_RESPONSE = {
    "resolvedAddress": "London, UK",
    "currentConditions": {
        "temp": 43.2,
        "humidity": 65,
        "conditions": "Clouds",
        "windspeed": 13.94
    },
    "days": [
        {
            "datetime": "2024-01-01",
            "temp": 43.2
        }
    ]
}


# ---- CITY WEATHER ----

@patch.dict(os.environ, {"WEATHER_API_KEY": "fake-key"})
@patch("WeatherDashboard.services.weather_service.requests.get")
def test_get_weather_by_city(mock_get):
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = MOCK_API_RESPONSE

    result = get_weather_by_city("London")

    assert result["status_code"] == 200
    assert "resolvedAddress" in result["data"]
    assert "currentConditions" in result["data"]
    mock_get.assert_called_once()


# ---- COORDS WEATHER ----

@patch.dict(os.environ, {"WEATHER_API_KEY": "fake-key"})
@patch("WeatherDashboard.services.weather_service.requests.get")
def test_get_weather_by_coords(mock_get):
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = MOCK_API_RESPONSE

    result = get_weather_by_coords(51.5085, -0.1257)

    assert result["status_code"] == 200
    assert "currentConditions" in result["data"]
    mock_get.assert_called_once()


# ---- FORECAST ----

@patch.dict(os.environ, {"WEATHER_API_KEY": "fake-key"})
@patch("WeatherDashboard.services.weather_service.requests.get")
def test_get_forecast_by_city(mock_get):
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = MOCK_API_RESPONSE

    result = get_forecast_by_city("London")

    assert result["status_code"] == 200
    assert "days" in result["data"]
    mock_get.assert_called_once()


# ---- API KEY ERROR ----

def test_get_api_key_missing():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(EnvironmentError):
            get_weather_by_city("London")
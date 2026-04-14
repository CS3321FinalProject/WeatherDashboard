import pytest
from unittest.mock import patch
from src.app import create_app


# ---- SETUP ----

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

MOCK_WEATHER = {
    "resolvedAddress": "Denver, CO, United States",
    "currentConditions": {
        "temp": 72.5,
        "conditions": "Partially cloudy",
        "humidity": 30.0,
        "windspeed": 10.5
    }
}

MOCK_WEATHER_COORDS = {
    "resolvedAddress": "Denver, CO, United States",
    "latitude": 39.7,
    "longitude": -104.9,
    "currentConditions": {
        "temp": 72.5,
        "conditions": "Partially cloudy",
        "humidity": 30.0,
        "windspeed": 10.5
    }
}

MOCK_FORECAST = {
    "resolvedAddress": "Denver, CO, United States",
    "days": [
        {
            "datetime": "2024-01-01",
            "temp": 72.5,
            "tempmax": 80.0,
            "tempmin": 60.0,
            "conditions": "Partially cloudy"
        },
        {
            "datetime": "2024-01-02",
            "temp": 68.0,
            "tempmax": 75.0,
            "tempmin": 55.0,
            "conditions": "Clear"
        }
    ]
}


# ---- /health TESTS ----

def test_health_check(client):
    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["message"] == "Weather API is alive"


# ---- /weather TESTS ----

@patch("src.routes.weather_routes.get_weather_by_city")
def test_get_weather_success(mock_service, client):
    mock_service.return_value = MOCK_WEATHER

    response = client.get("/weather?city=Denver")
    data = response.get_json()

    assert response.status_code == 200
    assert data["city"] == "Denver, CO, United States"
    assert data["temperature"] == 72.5
    assert data["conditions"] == "Partially cloudy"
    assert data["humidity"] == 30.0
    assert data["wind_speed"] == 10.5
    mock_service.assert_called_once_with("Denver")


def test_get_weather_missing_city(client):
    response = client.get("/weather")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "City parameter is required"


def test_get_weather_invalid_city_numbers(client):
    response = client.get("/weather?city=12345")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "Invalid city name"


def test_get_weather_city_too_short(client):
    response = client.get("/weather?city=A")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "City name must be at least 2 characters long"


def test_get_weather_city_too_long(client):
    response = client.get("/weather?city=" + "A" * 51)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "City name is too long"


@patch("src.routes.weather_routes.get_weather_by_city")
def test_get_weather_city_not_found(mock_service, client):
    mock_service.return_value = {}

    response = client.get("/weather?city=Fakecity")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Not found"
    assert data["message"] == "City not found"


@patch("src.routes.weather_routes.get_weather_by_city")
def test_get_weather_service_error(mock_service, client):
    import requests as req
    mock_service.side_effect = req.exceptions.RequestException("Connection failed")

    response = client.get("/weather?city=Denver")
    data = response.get_json()

    assert response.status_code == 500
    assert data["error"] == "Internal server error"


# ---- /weather/coords TESTS ----

@patch("src.routes.weather_routes.get_weather_by_coords")
def test_get_weather_coords_success(mock_service, client):
    mock_service.return_value = MOCK_WEATHER_COORDS

    response = client.get("/weather/coords?lat=39.7&lon=-104.9")
    data = response.get_json()

    assert response.status_code == 200
    assert data["location"] == "Denver, CO, United States"
    assert data["latitude"] == 39.7
    assert data["longitude"] == -104.9
    assert data["temperature"] == 72.5
    mock_service.assert_called_once_with(39.7, -104.9)


def test_get_weather_coords_missing_params(client):
    response = client.get("/weather/coords")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "Latitude and longitude parameters are required"


def test_get_weather_coords_missing_lon(client):
    response = client.get("/weather/coords?lat=39.7")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "Latitude and longitude parameters are required"


def test_get_weather_coords_not_numbers(client):
    response = client.get("/weather/coords?lat=abc&lon=xyz")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "Latitude and longitude must be numbers"


def test_get_weather_coords_out_of_range_lat(client):
    response = client.get("/weather/coords?lat=999&lon=-104.9")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "Latitude must be between -90 and 90"


def test_get_weather_coords_out_of_range_lon(client):
    response = client.get("/weather/coords?lat=39.7&lon=999")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "Longitude must be between -180 and 180"


@patch("src.routes.weather_routes.get_weather_by_coords")
def test_get_weather_coords_not_found(mock_service, client):
    mock_service.return_value = {}

    response = client.get("/weather/coords?lat=39.7&lon=-104.9")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Not found"
    assert data["message"] == "Location not found"


@patch("src.routes.weather_routes.get_weather_by_coords")
def test_get_weather_coords_service_error(mock_service, client):
    import requests as req
    mock_service.side_effect = req.exceptions.RequestException("Connection failed")

    response = client.get("/weather/coords?lat=39.7&lon=-104.9")
    data = response.get_json()

    assert response.status_code == 500
    assert data["error"] == "Internal server error"


# ---- /forecast TESTS ----

@patch("src.routes.weather_routes.get_forecast_by_city")
def test_get_forecast_success(mock_service, client):
    mock_service.return_value = MOCK_FORECAST

    response = client.get("/forecast?city=Denver")
    data = response.get_json()

    assert response.status_code == 200
    assert data["city"] == "Denver, CO, United States"
    assert len(data["forecast"]) == 2
    assert data["forecast"][0]["date"] == "2024-01-01"
    assert data["forecast"][0]["temp"] == 72.5
    assert data["forecast"][0]["temp_max"] == 80.0
    assert data["forecast"][0]["temp_min"] == 60.0
    assert data["forecast"][0]["conditions"] == "Partially cloudy"
    mock_service.assert_called_once_with("Denver")


def test_get_forecast_missing_city(client):
    response = client.get("/forecast")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "City parameter is required"


def test_get_forecast_invalid_city(client):
    response = client.get("/forecast?city=12345")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Bad request"
    assert data["message"] == "Invalid city name"


@patch("src.routes.weather_routes.get_forecast_by_city")
def test_get_forecast_city_not_found(mock_service, client):
    mock_service.return_value = {}

    response = client.get("/forecast?city=Fakecity")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Not found"
    assert data["message"] == "City not found"


@patch("src.routes.weather_routes.get_forecast_by_city")
def test_get_forecast_service_error(mock_service, client):
    import requests as req
    mock_service.side_effect = req.exceptions.RequestException("Connection failed")

    response = client.get("/forecast?city=Denver")
    data = response.get_json()

    assert response.status_code == 500
    assert data["error"] == "Internal server error"

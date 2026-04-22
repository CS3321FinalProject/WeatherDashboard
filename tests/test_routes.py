import pytest
from unittest.mock import patch
from WeatherDashboard.app import create_app

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

# ---- /health ----

def test_health_check(client):
    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["message"] == "Weather API is alive"


# ---- /weather ----

@patch("WeatherDashboard.routes.weather_routes.get_weather_by_city")
def test_get_weather_success(mock_service, client):
    mock_service.return_value = {"data": MOCK_WEATHER}

    response = client.get("/weather?city=Denver")
    data = response.get_json()

    assert response.status_code == 200
    assert data["city"] == "Denver, CO, United States"
    assert data["temperature"] == 72.5
    assert data["conditions"] == "Partially cloudy"
    assert data["humidity"] == 30.0
    assert data["wind_speed"] == 10.5
    assert "cat_url" in data


def test_get_weather_missing_city(client):
    response = client.get("/weather")
    data = response.get_json()

    assert response.status_code == 400
    assert "City parameter is required" in data["message"]
    assert "cat_url" in data


@patch("WeatherDashboard.routes.weather_routes.get_weather_by_city")
def test_get_weather_city_not_found(mock_service, client):
    mock_service.return_value = {"data": {}}

    response = client.get("/weather?city=Fakecity")
    data = response.get_json()

    assert response.status_code == 404
    assert "City not found" in data["message"]
    assert "cat_url" in data


@patch("WeatherDashboard.routes.weather_routes.get_weather_by_city")
def test_get_weather_service_error(mock_service, client):
    import requests as req
    mock_service.side_effect = req.exceptions.RequestException()

    response = client.get("/weather?city=Denver")
    data = response.get_json()

    assert response.status_code == 500
    assert "cat_url" in data


# ---- /weather/coords ----

@patch("WeatherDashboard.routes.weather_routes.get_weather_by_coords")
def test_get_weather_coords_success(mock_service, client):
    mock_service.return_value = {"data": MOCK_WEATHER_COORDS}

    response = client.get("/weather/coords?lat=39.7&lon=-104.9")
    data = response.get_json()

    assert response.status_code == 200
    assert data["location"] == "Denver, CO, United States"
    assert data["latitude"] == 39.7
    assert data["longitude"] == -104.9
    assert data["temperature"] == 72.5
    assert "cat_url" in data


@patch("WeatherDashboard.routes.weather_routes.get_weather_by_coords")
def test_get_weather_coords_not_found(mock_service, client):
    mock_service.return_value = {"data": {}}

    response = client.get("/weather/coords?lat=39.7&lon=-104.9")
    data = response.get_json()

    assert response.status_code == 404
    assert "cat_url" in data


# ---- /forecast ----

@patch("WeatherDashboard.routes.weather_routes.get_forecast_by_city")
def test_get_forecast_success(mock_service, client):
    mock_service.return_value = {"data": MOCK_FORECAST}

    response = client.get("/forecast?city=Denver")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["forecast"]) == 2
    assert "cat_url" in data


@patch("WeatherDashboard.routes.weather_routes.get_forecast_by_city")
def test_get_forecast_city_not_found(mock_service, client):
    mock_service.return_value = {"data": {}}

    response = client.get("/forecast?city=Fakecity")
    data = response.get_json()

    assert response.status_code == 404
    assert "cat_url" in data


# ---- / ----

def test_home_route(client):
    response = client.get("/")
    data = response.get_json()

    assert response.status_code == 200
    assert data["cat_url"] == "https://cataas.com/cat"

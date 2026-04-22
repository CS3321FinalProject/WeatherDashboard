from werkzeug.exceptions import BadRequest

def _validate_city(city):
    if not city or not city.strip():
        return "City parameter is required"

    city = city.strip()

    if len(city) < 2:
        return "City name must be at least 2 characters long"

    if len(city) > 50:
        return "City name is too long"

    if not city.replace(" ", "").isalpha():
        return "Invalid city name"

    return None

def _validate_coords(lat, lon):
    if not lat or not lon:
        return "Latitude and longitude parameters are required"

    if not lat.strip() or not lon.strip():
        return "Latitude and longitude cannot be blank"

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return "Latitude and longitude must be numbers"

    if not (-90 <= lat <= 90):
        return "Latitude must be between -90 and 90"

    if not (-180 <= lon <= 180):
        return "Longitude must be between -180 and 180"

    return None
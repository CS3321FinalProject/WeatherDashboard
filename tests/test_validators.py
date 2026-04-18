import pytest
from WeatherDashboard.utils.validators import _validate_city, _validate_coords


class TestValidateCity:

    # valid cities should return none
    @pytest.mark.parametrize("city", [
        "Paris",
        "New York",
        "Los Angeles",
        "AB",
        "A" * 50,
        "San Francisco",
        "Saint Louis",
        "  Paris  ",
        "São Paulo",        # accented chars are valid per .isalpha()
    ])
    def test_valid_city_returns_none(self, city):
        assert _validate_city(city) is None

    # empty or none city should return required message
    @pytest.mark.parametrize("city", [
        None,
        "",
        " ",
        "   ",
    ])
    def test_empty_or_missing_city_returns_required_message(self, city):
        assert _validate_city(city) == "City parameter is required"

    # city with 1 character should fail
    @pytest.mark.parametrize("city", [
        "A",
        "B",
    ])
    def test_city_too_short_returns_length_message(self, city):
        assert _validate_city(city) == "City name must be at least 2 characters long"

    # city longer than 50 characters should fail
    @pytest.mark.parametrize("city", [
        "A" * 51,
        "A" * 100,
        "New York " * 10,
    ])
    def test_city_too_long_returns_length_message(self, city):
        assert _validate_city(city) == "City name is too long"

    # cities with numbers symbols etc should fail
    @pytest.mark.parametrize("city", [
        "Paris123",
        "New_York",
        "Paris!",
        "New-York",
        "O'Brien",
        "Paris@City",
        "12345",
        "City#1",
    ])
    def test_invalid_characters_returns_invalid_message(self, city):
        assert _validate_city(city) == "Invalid city name"

    # exactly 2 chars is the minimum so it should pass
    def test_exactly_2_characters_is_valid(self):
        assert _validate_city("LA") is None

    # exactly 50 chars is the max so it should pass
    def test_exactly_50_characters_is_valid(self):
        assert _validate_city("A" * 50) is None

    # 51 chars is one over the limit so it should fail
    def test_exactly_51_characters_is_invalid(self):
        assert _validate_city("A" * 51) == "City name is too long"

    # spaces around a single letter get stripped so length becomes 1
    def test_single_character_after_strip_is_too_short(self):
        assert _validate_city("  A  ") == "City name must be at least 2 characters long"

    # all spaces become empty after strip so its treated as missing
    def test_whitespace_only_after_strip_is_required(self):
        assert _validate_city("     ") == "City parameter is required"

    # space between words is allowed
    def test_city_with_internal_spaces_is_valid(self):
        assert _validate_city("New York") is None

    # multiple spaces between words should also be fine
    def test_city_with_multiple_internal_spaces_is_valid(self):
        assert _validate_city("New  York") is None


class TestValidateCoords:

    # normal valid coordinates should return none
    @pytest.mark.parametrize("lat, lon", [
        ("0", "0"),
        ("90", "180"),
        ("-90", "-180"),
        ("51.5", "-0.12"),
        ("-33.9", "151.2"),
        ("40.7", "-74.0"),
        ("0.0", "0.0"),
    ])
    def test_valid_coords_returns_none(self, lat, lon):
        assert _validate_coords(lat, lon) is None

    # if lat or lon is none or empty string it should ask for both
    @pytest.mark.parametrize("lat, lon", [
        (None, None),
        (None, "10"),
        ("10", None),
        ("", ""),
        ("", "10"),
        ("10", ""),
    ])
    def test_missing_coords_returns_required_message(self, lat, lon):
        assert _validate_coords(lat, lon) == "Latitude and longitude parameters are required"

    # spaces only should be caught after strip
    @pytest.mark.parametrize("lat, lon", [
        (" ", " "),
        (" ", "10"),
        ("10", " "),
        ("   ", "   "),
    ])
    def test_blank_coords_returns_blank_message(self, lat, lon):
        assert _validate_coords(lat, lon) == "Latitude and longitude cannot be blank"

    # letters or symbols cant be converted to float so should fail
    @pytest.mark.parametrize("lat, lon", [
        ("abc", "10"),
        ("10", "xyz"),
        ("abc", "xyz"),
        ("12.3.4", "10"),
        ("10", "!@#"),
        ("null", "10"),
        ("10", "none"),
    ])
    def test_non_numeric_coords_returns_number_message(self, lat, lon):
        assert _validate_coords(lat, lon) == "Latitude and longitude must be numbers"

    # lat goes from -90 to 90 anything outside should fail
    @pytest.mark.parametrize("lat, lon", [
        ("91", "0"),
        ("90.1", "0"),
        ("-91", "0"),
        ("-90.1", "0"),
        ("180", "0"),
        ("-180", "0"),
    ])
    def test_lat_out_of_range_returns_lat_message(self, lat, lon):
        assert _validate_coords(lat, lon) == "Latitude must be between -90 and 90"

    # lon goes from -180 to 180 anything outside should fail
    @pytest.mark.parametrize("lat, lon", [
        ("0", "181"),
        ("0", "180.1"),
        ("0", "-181"),
        ("0", "-180.1"),
        ("0", "360"),
    ])
    def test_lon_out_of_range_returns_lon_message(self, lat, lon):
        assert _validate_coords(lat, lon) == "Longitude must be between -180 and 180"

    # exactly 90 and -90 are the lat boundaries so they should pass
    def test_lat_exactly_90_is_valid(self):
        assert _validate_coords("90", "0") is None

    def test_lat_exactly_minus_90_is_valid(self):
        assert _validate_coords("-90", "0") is None

    # exactly 180 and -180 are the lon boundaries so they should pass
    def test_lon_exactly_180_is_valid(self):
        assert _validate_coords("0", "180") is None

    def test_lon_exactly_minus_180_is_valid(self):
        assert _validate_coords("0", "-180") is None

    # one over the lat boundary should fail
    def test_lat_exactly_91_is_invalid(self):
        assert _validate_coords("91", "0") == "Latitude must be between -90 and 90"

    # one over the lon boundary should fail
    def test_lon_exactly_181_is_invalid(self):
        assert _validate_coords("0", "181") == "Longitude must be between -180 and 180"

    # validator checks lat first so bad lat error should come before lon error
    def test_lat_error_takes_priority_over_lon_error(self):
        assert _validate_coords("91", "181") == "Latitude must be between -90 and 90"

    # float strings should work fine not just integers
    def test_decimal_coords_are_valid(self):
        assert _validate_coords("45.123456", "90.654321") is None

    # negative float coords should also work
    def test_negative_decimal_coords_are_valid(self):
        assert _validate_coords("-45.678", "-90.123") is None
from flask import Flask
from dotenv import load_dotenv
from WeatherDashboard.routes.weather_routes import register_weather_routes
from WeatherDashboard.utils.error_handlers import register_error_handlers
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Home route MUST be inside factory OR moved to blueprint
    @app.route("/")
    def home():
        return {
            "message": "Weather Dashboard API is running",
            "cat_url": "https://cataas.com/cat"
        }

    @app.route("/health", methods=["GET"])
    def health():
        return {
            "status": "ok",
            "message": "Weather API is alive"
        }, 200

    register_weather_routes(app)
    register_error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

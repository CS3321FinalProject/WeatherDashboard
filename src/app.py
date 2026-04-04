from flask import Flask
from dotenv import load_dotenv
from src.routes.weather_routes import register_weather_routes
from src.utils.error_handlers import register_error_handlers
import os

# validator (if/else) logic for city and lat/long in validators.py
# weather routing logic in weather_routes.py
# tried to change code as minimally as possible while refactoring

load_dotenv()

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return {"message": "Weather Dashboard API is running"}

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

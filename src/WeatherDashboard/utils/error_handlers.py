from flask import jsonify
from WeatherDashboard.services.http_cats_service import get_cat_url

def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(e):
        status_code = 400
        return jsonify({
            "error": "Bad request",
            "message": getattr(e, "description", "Bad request"),
            "cat_url": get_cat_url()
        }), status_code

    @app.errorhandler(404)
    def not_found(e):
        status_code = 404
        return jsonify({
            "error": "Not found",
            "message": getattr(e, "description", "Not found"),
            "cat_url": get_cat_url()
        }), status_code

    @app.errorhandler(500)
    def internal_server_error(e):
        status_code = 500
        return jsonify({
            "error": "Internal server error",
            "message": getattr(e, "description", "Internal server error"),
            "cat_url": get_cat_url()
        }), status_code

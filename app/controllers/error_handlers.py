from flask import jsonify, make_response
from marshmallow import ValidationError

from app.exceptions import HttpException, UnauthorizedException
from app.services.session_service import clear_session_cookies
from config import Config

from .blueprints import api, views

# API error handlers for the application


@api.errorhandler(Exception)
def api_handle_exception(e):
    if Config.FLASK_ENV == "production":
        return jsonify({"message": "Internal Server Error"}), 500
    return jsonify({"message": str(e)}), 500


@api.errorhandler(HttpException)
def api_handle_http_exception(e):
    return jsonify({"message": e.message}), e.status_code


@api.errorhandler(ValidationError)
def api_handle_validation_error(e):
    return jsonify({"message": "Erro de validação", "errors": e.messages}), 400


@api.errorhandler(UnauthorizedException)
def api_handle_unauthorized_exception(e):
    return clear_session_cookies(make_response(jsonify({"message": e.message}), 401))


# Views error handlers for the application

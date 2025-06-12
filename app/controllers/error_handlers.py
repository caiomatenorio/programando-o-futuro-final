from flask import jsonify, make_response
from marshmallow import ValidationError

from app.services.session_service import clear_session_cookies
from config import Config

from .http_exceptions import HttpException, UnauthorizedException


def handle_error(e):
    if Config.FLASK_ENV == "production":
        return jsonify({"message": "Internal Server Error"}), 500
    return jsonify({"message": str(e)}), 500


def handle_http_exception(e):
    return jsonify({"message": e.message}), e.status_code


def handle_validation_exception(e):
    return jsonify({"message": "Erro de validação", "errors": e.messages}), 400


def handle_unauthorized_exception(e):
    return clear_session_cookies(make_response(jsonify({"message": e.message}), 401))


error_handlers = {
    Exception: handle_error,
    HttpException: handle_http_exception,
    ValidationError: handle_validation_exception,
    UnauthorizedException: handle_unauthorized_exception,
}

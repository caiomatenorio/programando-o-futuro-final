from flask import jsonify
from marshmallow import ValidationError

from config import Config

from .http_exceptions import HttpException


def handle_error(e):
    if Config.FLASK_ENV == "production":
        return jsonify({"message": "Internal Server Error"}), 500
    return jsonify({"message": str(e)}), 500


def handle_http_exception(e):
    return jsonify({"message": e.message}), e.status_code


def handle_validation_exception(e):
    return jsonify({"message": "Erro de validação", "errors": e.messages}), 400


def handle_unauthorized_exception(e):
    # TODO implement session cleanup
    return jsonify(e.message), 401


error_handlers = {
    Exception: handle_error,
    RuntimeError: handle_error,
    ValidationError: handle_validation_exception,
    HttpException: handle_http_exception,
}

from flask import jsonify

from config import Config


def handle_error(e):
    if Config.FLASK_ENV == "production":
        return jsonify({"message": "Internal Server Error"}), 500
    return jsonify({"message": str(e)}), 500


def handle_http_error(e):
    return jsonify({"message": e.message}), e.status_code


def handle_validation_error(e):
    return jsonify({"message": "Erro de validação", "errors": e.messages}), 400


def handle_unauthorized_error(e):
    # TODO implement session cleanup
    return jsonify(e.message), 401

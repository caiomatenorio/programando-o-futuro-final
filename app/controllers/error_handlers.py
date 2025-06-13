from marshmallow import ValidationError

from app.exceptions import HttpException, UnauthorizedException
from config import Config

from .blueprints import api, views
from .dtos import ErrorResponseDto

# API error handlers for the application


@api.errorhandler(Exception)
def api_handle_exception(e):
    if Config.FLASK_ENV == "production":
        return ErrorResponseDto(
            500,
            "Ocorreu um erro interno no servidor.",
        ).to_response()
    return ErrorResponseDto(500, str(e)).to_response()


@api.errorhandler(HttpException)
def api_handle_http_exception(e):
    return ErrorResponseDto(e.status_code, e.message).to_response()


@api.errorhandler(ValidationError)
def api_handle_validation_error(e):
    return ErrorResponseDto(400, "Erro de validação.", e.messages).to_response()


@api.errorhandler(UnauthorizedException)
def api_handle_unauthorized_exception(e):
    return ErrorResponseDto(401, e.message).to_response(clear_session=True)


# Views error handlers for the application

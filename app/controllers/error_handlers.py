"""
Error handlers for the application blueprints. These handlers catch exceptions raised during
request processing and return appropriate error responses.
"""

from marshmallow import ValidationError

from app.exceptions import HttpException, UnauthorizedException
from config import Config

from .blueprints import api
from .dtos import ErrorResponseDto


@api.errorhandler(Exception)
def api_handle_exception(e):
    """
    Handles general exceptions that occur during request processing. If the application is in
    production mode, it returns a generic error message to avoid exposing sensitive information. In
    development mode, it returns the exception message for debugging purposes.

    :param e: The exception that was raised.
    :return: An ErrorResponseDto with a status code of 500 and an error message
    """

    if Config.FLASK_ENV == "production":
        return ErrorResponseDto(
            500,
            "Ocorreu um erro interno no servidor.",
        ).to_response()
    return ErrorResponseDto(500, str(e)).to_response()


@api.errorhandler(HttpException)
def api_handle_http_exception(e):
    """
    Handles HTTP exceptions raised by the application. It returns an ErrorResponseDto with the
    status code and message from the exception.

    :param e: The HttpException that was raised.
    :return: An ErrorResponseDto with the status code and message from the exception.
    """

    return ErrorResponseDto(e.status_code, e.message).to_response()


@api.errorhandler(ValidationError)
def api_handle_validation_error(e):
    """
    Handles validation errors raised by Marshmallow schemas. It returns an ErrorResponseDto with
    a status code of 400 and the validation error messages. This is used to provide feedback on
    invalid request data, such as missing or malformed fields.

    :param e: The ValidationError that was raised.
    :return: An ErrorResponseDto with a status code of 400 and the validation error messages.
    """

    return ErrorResponseDto(400, "Erro de validação.", e.messages).to_response()


@api.errorhandler(UnauthorizedException)
def api_handle_unauthorized_exception(e):
    """
    Handles unauthorized exceptions raised by the application. It returns an ErrorResponseDto with
    a status code of 401 and the exception message. This is used to indicate that the user is not
    authenticated or does not have permission to access the requested resource. It also clears the
    session cookies to ensure that the user is logged out.

    :param e: The UnauthorizedException that was raised.
    :return: An ErrorResponseDto with a status code of 401 and the exception message
    """

    return ErrorResponseDto(401, e.message).to_response(clear_session=True)

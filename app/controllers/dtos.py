from dataclasses import dataclass
from typing import Optional, Union

from flask import jsonify, make_response

from app.services.session_service import add_session_cookies, clear_session_cookies


@dataclass
class ResponseDto:
    status_code: int
    message: str

    def to_response(self, clear_session=False):
        body = {k: v for k, v in self.__dict__.items() if v is not None}
        response = make_response(jsonify(body), self.status_code)
        if clear_session:
            return clear_session_cookies(response)
        return add_session_cookies(response)


@dataclass
class SuccessResponseDto(ResponseDto):
    data: Optional[Union[dict, list]] = None

    def __post_init__(self):
        if 300 <= self.status_code < 200:
            raise ValueError("Status code for SuccessResponseDto must be 2xx Success.")


@dataclass
class ErrorResponseDto(ResponseDto):
    errors: Optional[dict] = None

    def __post_init__(self):
        if not (400 <= self.status_code < 600):
            raise ValueError(
                "Status code for ErrorResponseDto must be 4xx or 5xx Error."
            )

"""
Data Transfer Objects (DTOs) for API responses. These DTOs are used to standardize the structure of
API responses, including success and error responses and to handle session cookies for user
authentication.
"""

from dataclasses import dataclass
from typing import Optional, Union

from flask import jsonify, make_response

from app.services.session_service import add_session_cookies, clear_session_cookies


@dataclass
class ResponseDto:
    """
    Base class for API responses. It includes a status code and a message. This class is intended
    to be extended by specific response DTOs like SuccessResponseDto and ErrorResponseDto. It
    provides a method to convert the DTO into a Flask response object with appropriate session
    cookies handling.

    :ivar status_code: HTTP status code for the response.
    :ivar message: A message describing the response.
    """

    status_code: int
    message: str

    def to_response(self, clear_session=False):
        """
        Converts the DTO into a Flask response object with JSON body and session cookies.

        :param clear_session: If True, clears the session cookies; otherwise, adds session cookies.
        :return: A Flask response object with the JSON body and session cookies.
        """

        # Filter out None values from the DTO's attributes to avoid sending them in the response
        body = {k: v for k, v in self.__dict__.items() if v is not None}
        response = make_response(jsonify(body), self.status_code)

        if clear_session:
            return clear_session_cookies(response)
        return add_session_cookies(response)


@dataclass
class SuccessResponseDto(ResponseDto):
    """
    Success response DTO for API responses. It includes a status code, a message, and optional
    data. This DTO is used to represent successful API responses, typically with a 2xx status code.
    It raises a ValueError if the status code is not in the 2xx range.

    :ivar status_code: HTTP status code for the response (must be in the 2xx range).
    :ivar message: A message describing the response.
    :ivar data: Optional data to include in the response, which can be a dictionary or
    """

    data: Optional[Union[dict, list]] = None

    def __post_init__(self):
        if 300 <= self.status_code < 200:
            raise ValueError("Status code for SuccessResponseDto must be 2xx Success.")


@dataclass
class ErrorResponseDto(ResponseDto):
    """
    Error response DTO for API responses. It includes a status code, a message, and optional
    errors. This DTO is used to represent error responses, typically with a 4xx or 5xx status code.
    It raises a ValueError if the status code is not in the 4xx or 5xx range.
    """

    errors: Optional[dict] = None

    def __post_init__(self):
        if not (400 <= self.status_code < 600):
            raise ValueError(
                "Status code for ErrorResponseDto must be 4xx or 5xx Error."
            )

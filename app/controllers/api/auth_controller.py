"""
Controller for handling user authentication operations such as registration, login, logout, and
checking authentication status. It uses Flask's request context to handle incoming JSON requests
and returns appropriate success responses. The controller interacts with the auth service to
perform the necessary operations and uses schemas for request validation.
"""

from flask import request

from app.controllers.blueprints import api
from app.controllers.dtos import SuccessResponseDto
from app.services import auth_service

from .schemas.auth_schemas import LoginSchema, RegisterSchema


@api.post("/auth/register")
def register():
    """
    POST endpoint to register a new user. It expects a JSON body with the user's name, email, and
    password.

    :return: A success response with a status code of 201 if the user is created successfully.
    :raises ValidationError: If the request body does not conform to the expected schema.
    :raises EmailAlreadyInUseException: If the email is already associated with an existing user.
    """

    body = RegisterSchema().load(request.json)  # type: ignore
    auth_service.register(body["name"], body["email"], body["password"])  # type: ignore
    return SuccessResponseDto(201, "Usuário criado com sucesso.").to_response()


@api.post("/auth/login")
def login():
    """
    POST endpoint to log in a user. It expects a JSON body with the user's email and password.

    :return: A success response with a status code of 200 if the login is successful.
    :raises ValidationError: If the request body does not conform to the expected schema.
    :raises InvalidCredentialsException: If the email or password is incorrect.
    """

    body = LoginSchema().load(request.json)  # type: ignore
    auth_service.login(body["email"], body["password"])  # type: ignore
    return SuccessResponseDto(200, "Login realizado com sucesso.").to_response()


@api.post("/auth/logout")
def logout():
    """
    POST endpoint to log out the current user. It clears the session and returns a success response.

    :return: A success response with a status code of 200 if the logout is successful.
    :raises UnauthorizedException: If the user is not authenticated or the session does not exist.
    """

    auth_service.logout()
    return SuccessResponseDto(
        200,
        "Logout realizado com sucesso.",
    ).to_response(clear_session=True)


@api.get("/auth/status")
def get_auth_status():
    """
    GET endpoint to check the authentication status of the current user.

    :return: A success response with a status code of 200 and a boolean indicating the
             authentication status.
    """

    authenticated = auth_service.is_authenticated()
    return SuccessResponseDto(
        200,
        "Status de autenticação verificado com sucesso.",
        {"authenticated": authenticated},
    ).to_response()

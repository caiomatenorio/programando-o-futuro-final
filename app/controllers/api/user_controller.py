"""
Controller for user-related operations. It provides endpoints to retrieve the current user's
information, update user details (name, email, password), and delete the user account. The
controller uses Flask's request context to handle incoming JSON requests and returns appropriate
success responses. It interacts with the user service to perform the necessary operations and uses
schemas for request validation.
"""

from flask import request

from app.controllers.blueprints import api
from app.controllers.dtos import SuccessResponseDto
from app.services import user_service

from .schemas.user_schemas import (
    DeleteUserAccountSchema,
    UpdateUserEmailSchema,
    UpdateUserNameSchema,
    UpdateUserPasswordSchema,
)


@api.get("/my-account")
def get_current_user():
    """
    GET endpoint to retrieve the current user's information.

    :return: A success response with a status code of 200 and the user's information.
    :raises UnauthorizedException: If the user is not authenticated or the session does not exist.
    """

    user = user_service.get_current_user()
    user.pop("id")
    return SuccessResponseDto(
        200,
        "Usuário atual obtido com sucesso.",
        user,
    ).to_response()


@api.put("/my-account/name")
def update_user_name():
    """
    PUT endpoint to update the current user's name. It expects a JSON body with the new name.

    :return: A success response with a status code of 200 if the name is updated successfully.
    :raises ValidationError: If the request body does not conform to the expected schema.
    :raises UnauthorizedException: If the user is not authenticated or the session does not exist.
    """

    body = UpdateUserNameSchema().load(request.json)  # type: ignore
    user_service.update_current_user_name(body["name"])  # type: ignore
    return SuccessResponseDto(
        200,
        "Nome do usuário atualizado com sucesso.",
    ).to_response()


@api.put("/my-account/email")
def update_user_email():
    """
    PUT endpoint to update the current user's email. It expects a JSON body with the new email.

    :return: A success response with a status code of 200 if the email is updated successfully.
    :raises ValidationError: If the request body does not conform to the expected schema.
    :raises UnauthorizedException: If the user is not authenticated or the session does not exist.
    :raises EmailAlreadyInUseException: If the new email is already associated with another user
    """

    body = UpdateUserEmailSchema().load(request.json)  # type: ignore
    user_service.update_current_user_email(body["email"])  # type: ignore
    return SuccessResponseDto(
        200,
        "Email do usuário atualizado com sucesso.",
    ).to_response()


@api.put("/my-account/password")
def update_user_password():
    """
    PUT endpoint to update the current user's password. It expects a JSON body with the current
    password and the new password.

    :return: A success response with a status code of 200 if the password is updated successfully.
    :raises ValidationError: If the request body does not conform to the expected schema.
    :raises UnauthorizedException: If the user is not authenticated or the session does not exist.
    :raises InvalidCredentialsException: If the current password is incorrect.
    """

    body = UpdateUserPasswordSchema().load(request.json)  # type: ignore
    user_service.update_current_user_password(
        body["current_password"],  # type: ignore
        body["new_password"],  # type: ignore
    )
    return SuccessResponseDto(
        200,
        "Senha do usuário atualizada com sucesso.",
    ).to_response()


@api.delete("/my-account")
def delete_user_account():
    """
    DELETE endpoint to delete the current user's account. It expects a JSON body with the user's
    password for confirmation.

    :return: A success response with a status code of 200 if the account is deleted successfully.
    :raises ValidationError: If the request body does not conform to the expected schema.
    :raises UnauthorizedException: If the user is not authenticated or the session does not exist.
    :raises InvalidCredentialsException: If the provided password is incorrect.
    """

    body = DeleteUserAccountSchema().load(request.json)  # type: ignore
    user_service.delete_current_user(body["password"])  # type: ignore
    return SuccessResponseDto(
        200,
        "Conta de usuário deletada com sucesso.",
    ).to_response(clear_session=True)

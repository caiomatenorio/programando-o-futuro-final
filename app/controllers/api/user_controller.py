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


@api.get("/users/me")
def get_current_user():
    user = user_service.get_current_user()
    user.pop("id")
    return SuccessResponseDto(
        200,
        "Usuário atual obtido com sucesso.",
        user,
    ).to_response()


@api.put("/users/me/name")
def update_user_name():
    body = UpdateUserNameSchema().load(request.json)  # type: ignore
    user_service.update_current_user_name(body["name"])  # type: ignore
    return SuccessResponseDto(
        200,
        "Nome do usuário atualizado com sucesso.",
    ).to_response()


@api.put("/users/me/email")
def update_user_email():
    body = UpdateUserEmailSchema().load(request.json)  # type: ignore
    user_service.update_current_user_email(body["email"])  # type: ignore
    return SuccessResponseDto(
        200,
        "Email do usuário atualizado com sucesso.",
    ).to_response()


@api.put("/users/me/password")
def update_user_password():
    body = UpdateUserPasswordSchema().load(request.json)  # type: ignore
    user_service.update_current_user_password(
        body["current_password"],  # type: ignore
        body["new_password"],  # type: ignore
    )
    return SuccessResponseDto(
        200,
        "Senha do usuário atualizada com sucesso.",
    ).to_response()


@api.delete("/users/me")
def delete_user_account():
    body = DeleteUserAccountSchema().load(request.json)  # type: ignore
    user_service.delete_current_user(body["password"])  # type: ignore
    return SuccessResponseDto(
        200,
        "Conta de usuário deletada com sucesso.",
    ).to_response(clear_session=True)

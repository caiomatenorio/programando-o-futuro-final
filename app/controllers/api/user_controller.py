from flask import jsonify

from app.controllers.blueprints import api
from app.services import user_service

from .schemas.user_schemas import (
    DeleteUserAccountRequest,
    UpdateUserEmailRequest,
    UpdateUserNameRequest,
    UpdateUserPasswordRequest,
)


@api.get("/users/me")
def get_current_user():
    user = user_service.get_current_user()
    user.pop("id")  # Remove sensitive information
    return jsonify({"message": "Usuário obtido com sucesso.", "data": user}), 200


@api.put("/users/me/name")
def update_user_name():
    body = UpdateUserNameRequest().load(request.json)  # type: ignore
    user_service.update_current_user_name(body["name"])  # type: ignore
    return jsonify({"message": "Nome do usuário atualizado com sucesso."}), 200


@api.put("/users/me/email")
def update_user_email():
    body = UpdateUserEmailRequest().load(request.json)  # type: ignore
    user_service.update_current_user_email(body["email"])  # type: ignore
    return jsonify({"message": "Email do usuário atualizado com sucesso."}), 200


@api.put("/users/me/password")
def update_user_password():
    body = UpdateUserPasswordRequest().load(request.json)  # type: ignore
    user_service.update_current_user_password(
        body["current_password"],  # type: ignore
        body["new_password"],  # type: ignore
    )
    return jsonify({"message": "Senha do usuário atualizada com sucesso."}), 200


@api.delete("/users/me")
def delete_user_account():
    body = DeleteUserAccountRequest().load(request.json)  # type: ignore
    user_service.delete_current_user_account(body["password"])  # type: ignore
    return jsonify({"message": "Conta de usuário deletada com sucesso."}), 200

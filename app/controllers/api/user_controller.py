from flask import jsonify

from app.controllers.blueprints import api
from app.services import user_service

from .schemas.user_schemas import UpdateUserEmailRequest, UpdateUserNameRequest


@api.get("/users/me")
def get_current_user():
    user = user_service.get_current_user()
    user.pop("id")  # Remove sensitive information
    return jsonify({"message": "Usuário obtido com sucesso.", "data": user}), 200


def update_user_name():
    body = UpdateUserNameRequest().load(request.json)  # type: ignore
    user_service.update_current_user_name(body["name"])  # type: ignore
    return jsonify({"message": "Nome do usuário atualizado com sucesso."}), 200


def update_user_email():
    body = UpdateUserEmailRequest().load(request.json)  # type: ignore
    user_service.update_current_user_email(body["email"])  # type: ignore
    return jsonify({"message": "Email do usuário atualizado com sucesso."}), 200


def update_user_password(): ...


def delete_user_account(): ...

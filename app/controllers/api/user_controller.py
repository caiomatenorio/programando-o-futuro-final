from flask import jsonify

from app.controllers.blueprints import api
from app.services import user_service


@api.get("/users/me")
def get_current_user():
    user = user_service.get_current_user()
    user.pop("id")
    return jsonify({"message": "Usuário obtido com sucesso.", "data": user}), 200


def update_user_name(): ...


def update_user_email(): ...


def update_user_password(): ...


def delete_user_account(): ...

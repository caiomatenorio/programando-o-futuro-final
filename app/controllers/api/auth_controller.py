from flask import jsonify, make_response, request

from app.controllers.blueprints import api
from app.services import auth_service
from app.services.session_service import add_session_cookies, clear_session_cookies

from .schemas.auth_schemas import LoginRequest, RegisterRequest


@api.post("/auth/register")
def register():
    body = RegisterRequest().load(request.json)  # type: ignore
    auth_service.register(body["name"], body["email"], body["password"])  # type: ignore
    return jsonify({"message": "Usuário criado com sucesso."}), 201


@api.post("/auth/login")
def login():
    body = LoginRequest().load(request.json)  # type: ignore
    auth_service.login(body["email"], body["password"])  # type: ignore
    return add_session_cookies(
        make_response(
            jsonify({"message": "Login realizado com sucesso."}),
            200,
        )
    )


@api.post("/auth/logout")
def logout():
    auth_service.logout()
    return clear_session_cookies(
        make_response(
            jsonify({"message": "Logout realizado com sucesso."}),
            200,
        )
    )


@api.get("/auth/status")
def auth_status():
    status = auth_service.get_auth_status()
    return jsonify(status), 200

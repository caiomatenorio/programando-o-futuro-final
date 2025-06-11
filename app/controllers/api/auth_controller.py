from flask import Blueprint, jsonify, make_response, request

from app.services import auth_service
from app.services.session_service import add_session_cookies

from .schemas.auth_schemas import LoginRequest, RegisterRequest

bp = Blueprint("api_auth", __name__, url_prefix="/api/auth")


@bp.post("/register")
def register():
    body = RegisterRequest().load(request.json)  # type: ignore
    auth_service.register(body["name"], body["email"], body["password"])  # type: ignore
    return jsonify({"message": "Usuário criado com sucesso."}), 201


@bp.post("/login")
def login():
    body = LoginRequest().load(request.json)  # type: ignore
    auth_service.login(body["email"], body["password"])  # type: ignore
    return add_session_cookies(
        make_response(
            jsonify({"message": "Login realizado com sucesso."}),
            200,
        )
    )


# @bp.post("/logout")
# def logout(): ...


# @bp.get("/me")
# def me(): ...

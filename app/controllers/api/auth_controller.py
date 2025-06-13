from flask import request

from app.controllers.blueprints import api
from app.controllers.dtos import SuccessResponseDto
from app.services import auth_service

from .schemas.auth_schemas import LoginSchema, RegisterSchema


@api.post("/auth/register")
def register():
    body = RegisterSchema().load(request.json)  # type: ignore
    auth_service.register(body["name"], body["email"], body["password"])  # type: ignore
    return SuccessResponseDto(201, "Usuário criado com sucesso.").to_response()


@api.post("/auth/login")
def login():
    body = LoginSchema().load(request.json)  # type: ignore
    auth_service.login(body["email"], body["password"])  # type: ignore
    return SuccessResponseDto(200, "Login realizado com sucesso.").to_response()


@api.post("/auth/logout")
def logout():
    auth_service.logout()
    return SuccessResponseDto(
        200,
        "Logout realizado com sucesso.",
    ).to_response(clear_session=True)


@api.get("/auth/status")
def get_auth_status():
    authenticated = auth_service.is_authenticated()
    return SuccessResponseDto(
        200,
        "Status de autenticação verificado com sucesso.",
        {"authenticated": authenticated},
    ).to_response()

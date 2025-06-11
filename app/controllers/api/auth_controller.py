from flask import Blueprint, jsonify, request

from app.services import auth_service

from .schemas.auth_schemas import RegisterRequest

bp = Blueprint("api_auth", __name__, url_prefix="/api/auth")


@bp.post("/register")
def register():
    body = RegisterRequest().load(request.json)  # type: ignore
    auth_service.register(body["name"], body["email"], body["password"])  # type: ignore
    return jsonify({}), 201


# @bp.post("/login")
# def login(): ...


# @bp.post("/logout")
# def logout(): ...


# @bp.get("/me")
# def me(): ...

from app.controllers.http_exceptions import UnauthorizedException
from app.extensions import db

from . import session_service, user_service


def register(name, email, password):
    user_service.create_user(name, email, password)


def login(email, password):
    with db.session.begin():
        user = user_service.validate_credentials(email, password, True)
        session = session_service.create_session(user.id)
        jwt = session_service.create_jwt(session.id, user.id, user.name, user.email)
        session_service.set_new_tokens(jwt, session.refresh_token)


def get_auth_status():
    response: dict = {"message": "Status de autenticação obtido com sucesso."}

    try:
        session_service.validate_session()
        response["data"] = {
            "authenticated": True,
            "user": {
                "name": session_service.g.name,
                "email": session_service.g.email,
            },
        }
        return response
    except UnauthorizedException:
        response["data"] = {"authenticated": False}
        return response

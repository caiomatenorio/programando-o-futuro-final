from datetime import timedelta

from flask import g
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.session import Session
from config import Config


def create_session(user_id):
    with db.session.begin_nested():
        session = Session(user_id=user_id)  # type: ignore
        db.session.add(session)
    return session


def create_jwt(session_id, user_id, name, email):
    return create_access_token(
        identity=session_id,
        expires_delta=timedelta(seconds=Config.JWT_EXPIRATION_SECS),
        additional_claims={
            "user_id": user_id,
            "name": name,
            "email": email,
        },
    )


def set_new_tokens(access_token, refresh_token):
    g.access_token = access_token
    g.refresh_token = refresh_token


def get_new_tokens():
    return g.get("access_token"), g.get("refresh_token")


def add_session_cookies(response):
    for index, token in enumerate(get_new_tokens()):
        response.set_cookie(
            "access_token" if index == 0 else "refresh_token",
            token,
            max_age=(
                Config.JWT_EXPIRATION_SECS
                if index == 0
                else Config.SESSION_EXPIRATION_SECS
            ),
            httponly=True,
            secure=Config.FLASK_ENV == "production",
            samesite="Strict" if Config.FLASK_ENV == "production" else "Lax",
            path="/",
        )

    return response

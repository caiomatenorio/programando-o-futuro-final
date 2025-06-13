from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from flask import g, request

from app.exceptions import SessionNotFoundException, UnauthorizedException
from app.extensions import db
from app.models.session import Session
from config import Config


def create_session(user_id):
    with db.session.begin_nested():
        session = Session(user_id=user_id)  # type: ignore
        db.session.add(session)
    return session


def get_session_by_id(session_id, inside_transaction=False):
    with db.session.begin_nested() if inside_transaction else db.session.begin():
        session = Session.query.filter_by(id=session_id).with_for_update().first()

        if session:
            if not session.is_expired():
                return session
            delete_session(session)


def get_session_by_id_or_raise(session_id, inside_transaction=False):
    session = get_session_by_id(session_id, inside_transaction)

    if not session:
        raise SessionNotFoundException()

    return session


def get_session_by_refresh_token(refresh_token, inside_transaction=False):
    with db.session.begin_nested() if inside_transaction else db.session.begin():
        session = (
            Session.query.filter_by(refresh_token=refresh_token)
            .with_for_update()
            .first()
        )

        if session:
            if not session.is_expired():
                return session
            delete_session(session)


def get_session_by_refresh_token_or_raise(refresh_token, inside_transaction=False):
    session = get_session_by_refresh_token(refresh_token, inside_transaction)

    if not session:
        raise SessionNotFoundException()

    return session


def delete_session(session):
    with db.session.begin_nested():
        db.session.delete(session)


def delete_session_by_id(session_id):
    with db.session.begin():
        session = get_session_by_id_or_raise(session_id, True)
        delete_session(session)


def create_jwt(session_id, user_id, name, email):
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(seconds=Config.JWT_EXPIRATION_SECS)
    payload = {
        "data": {
            "session_id": str(session_id),
            "user_id": str(user_id),
            "name": name,
            "email": email,
        },
        "exp": int(expiration.timestamp()),
        "iat": int(now.timestamp()),
    }

    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")


def decode_jwt(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        payload["data"]["session_id"] = UUID(payload["data"]["session_id"])
        payload["data"]["user_id"] = UUID(payload["data"]["user_id"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise UnauthorizedException()


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


def clear_session_cookies(response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

    return response


def extract_session_from_request():
    return tuple(
        request.cookies.get(cookie_name)
        for cookie_name in ["access_token", "refresh_token"]
    )


def set_current_session(access_token=None, refresh_token=None):
    if access_token:
        payload = decode_jwt(access_token)

        g.session_id = payload["data"]["session_id"]
        g.user_id = payload["data"]["user_id"]
        g.name = payload["data"]["name"]
        g.email = payload["data"]["email"]
    elif refresh_token:
        session = get_session_by_refresh_token_or_raise(refresh_token)

        g.session_id = session.id
        g.user_id = session.user_id
        g.name = session.user.name
        g.email = session.user.email


def validate_session():
    access_token, refresh_token = extract_session_from_request()

    if access_token:
        try:
            set_current_session(access_token=access_token)
            return
        except UnauthorizedException:
            pass

    if refresh_token:
        try:
            new_tokens = refresh_session(refresh_token)
            set_current_session(access_token=new_tokens[0])
            set_new_tokens(*new_tokens)
            return
        except SessionNotFoundException:
            pass

    raise UnauthorizedException()


def refresh_session(refresh_token):
    with db.session.begin():
        session = get_session_by_refresh_token_or_raise(refresh_token, True)

        session.refresh_token = Session.generate_refresh_token()
        session.expires_at = Session.calculate_expiration()
        session.updated_at = datetime.now(timezone.utc)

        db.session.add(session)

        jwt = create_jwt(
            session.id,
            session.user_id,
            session.user.name,
            session.user.email,
        )

        return jwt, session.refresh_token


def get_current_session_id():
    session_id = g.get("session_id")

    if not session_id:
        raise UnauthorizedException()
    return session_id

"""
# Session Service Module

This module provides functions to manage user sessions, including creating, retrieving, refreshing,
and deleting sessions. It also handles JWT creation and decoding, session validation, and cookie
management for session tokens.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from flask import g, request

from app.exceptions import SessionNotFoundException, UnauthorizedException
from app.extensions import db
from app.models.session import Session
from config import Config


def create_session(user_id):
    """
    Create a new session for the given user. This function generates a new session with a unique
    refresh token and sets the expiration time based on the configuration.

    :param user_id: The ID of the user for whom the session is being created.
    :return: The newly created session object.
    """

    with db.session.begin_nested():
        session = Session(user_id=user_id)  # type: ignore
        db.session.add(session)
    return session


def get_session_by_id(session_id, inside_transaction=False):
    """
    Retrieve a session by its ID. If the session is found and not expired, it is returned. If the
    session is expired, it is deleted.

    :param session_id: The ID of the session to retrieve.
    :param inside_transaction: Whether the function is called within an existing transaction.
    :return: The session object if found and not expired, otherwise None.
    """

    with db.session.begin_nested() if inside_transaction else db.session.begin():
        session = Session.query.filter_by(id=session_id).with_for_update().first()

        if session:
            if not session.is_expired():
                return session
            delete_session(session)


def get_session_by_id_or_raise(session_id, inside_transaction=False):
    """
    Retrieve a session by its ID and raise an exception if not found. This function is used to
    ensure that the session exists and is valid.

    :param session_id: The ID of the session to retrieve.
    :param inside_transaction: Whether the function is called within an existing transaction.
    :return: The session object if found and valid.
    :raises SessionNotFoundException: If the session with the given ID does not exist or is
        expired.
    """

    session = get_session_by_id(session_id, inside_transaction)

    if not session:
        raise SessionNotFoundException()

    return session


def get_session_by_refresh_token(refresh_token, inside_transaction=False):
    """
    Retrieve a session by its refresh token. If the session is found and not expired, it is
    returned. If the session is expired, it is deleted.

    :param refresh_token: The refresh token associated with the session.
    :param inside_transaction: Whether the function is called within an existing transaction.
    :return: The session object if found and not expired, otherwise None.
    """

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
    """
    Retrieve a session by its refresh token and raise an exception if not found. This function is
    used to ensure that the session exists and is valid.

    :param refresh_token: The refresh token associated with the session.
    :param inside_transaction: Whether the function is called within an existing transaction.
    :return: The session object if found and valid.
    :raises SessionNotFoundException: If the session with the given refresh token does not exist or
        is expired.
    """

    session = get_session_by_refresh_token(refresh_token, inside_transaction)

    if not session:
        raise SessionNotFoundException()

    return session


def get_current_session_id():
    """
    Retrieve the current session ID from the global context. This function checks if the session ID
    is set in the global context and returns it. If the session ID is not set, it raises an
    UnauthorizedException.

    :return: The current session ID.
    :raises UnauthorizedException: If the session ID is not set in the global context.
    """

    session_id = g.get("session_id")

    if not session_id:
        raise UnauthorizedException()
    return session_id


def refresh_session(refresh_token):
    """
    Refresh the session by generating a new refresh token and updating the session's expiration
    time. This function retrieves the session using the provided refresh token, updates its refresh
    token and expiration time, and returns a new JWT and refresh token.

    :param refresh_token: The refresh token used to retrieve the session.
    :return: A tuple containing the new JWT and refresh token.
    :raises SessionNotFoundException: If the session with the given refresh token does not exist or
        is expired.
    """

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


def delete_session(session):
    """
    Delete a session from the database. This function is used to remove a session when it is no
    longer needed or has expired.

    :param session: The session object to be deleted.
    :return: None
    """

    with db.session.begin_nested():
        db.session.delete(session)


def delete_session_by_id(session_id):
    """
    Delete a session by its ID. This function is used to remove a session when it is no longer
    needed or has expired.

    :param session_id: The ID of the session to be deleted.
    :return: None
    :raises SessionNotFoundException: If the session with the given ID does not exist.
    """

    with db.session.begin():
        session = get_session_by_id_or_raise(session_id, True)
        delete_session(session)


def create_jwt(session_id, user_id, name, email):
    """
    Create a JSON Web Token (JWT) for the given session and user information. The token includes
    the session ID, user ID, name, and email, along with expiration and issued at timestamps.

    :param session_id: The ID of the session for which the JWT is being created.
    :param user_id: The ID of the user associated with the session.
    :param name: The name of the user associated with the session.
    :param email: The email of the user associated with the session.
    :return: The encoded JWT as a string.
    """

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
    """
    Decode a JSON Web Token (JWT) and return its payload. The function verifies the token's
    signature and extracts the session ID and user ID, converting them to UUIDs. If the token is
    expired or invalid, an UnauthorizedException is raised.

    :param token: The JWT to decode.
    :return: The decoded payload containing session and user information.
    :raises UnauthorizedException: If the token is expired or invalid.
    """

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        payload["data"]["session_id"] = UUID(payload["data"]["session_id"])
        payload["data"]["user_id"] = UUID(payload["data"]["user_id"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise UnauthorizedException()


def set_new_tokens(access_token, refresh_token):
    """
    Set new access and refresh tokens in the global context. This function is used to store the
    tokens for the current session, allowing them to be accessed later.

    :param access_token: The new access token to be set.
    :param refresh_token: The new refresh token to be set.
    :return: None
    """

    g.access_token = access_token
    g.refresh_token = refresh_token


def get_new_tokens():
    """
    Retrieve the new access and refresh tokens from the global context. This function is used to
    access the tokens that were set during the session creation or refresh process.

    :return: A tuple containing the access token and refresh token, or None if not set.
    """

    return g.get("access_token"), g.get("refresh_token")


def add_session_cookies(response):
    """
    Add session cookies to the response. This function sets the access and refresh tokens as
    cookies in the response, with appropriate attributes such as max age, httponly, secure,
    samesite, and path. The cookies are set based on the tokens retrieved from the global context
    and only if both tokens are available to ensure a valid session.

    :param response: The response object to which the cookies will be added.
    :return: The response object with the session cookies added.
    """

    if all(new_tokens := get_new_tokens()):
        for index, token in enumerate(new_tokens):
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
    """
    Clear session cookies from the response. This function removes the access and refresh tokens
    from the response cookies, effectively logging out the user by invalidating the session.

    :param response: The response object from which the cookies will be removed.
    :return: The response object with the session cookies cleared.
    """

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

    return response


def set_current_session(access_token=None, refresh_token=None):
    """
    Set the current session in the global context based on the provided access and refresh tokens.
    This function decodes the access token to extract session and user information, or retrieves
    the session by refresh token if the access token is not provided. The session information is
    stored in the global context for later use.

    :param access_token: The access token to decode and set the current session.
    :param refresh_token: The refresh token to retrieve the session if access token is not provided
    :return: None
    :raises UnauthorizedException: If neither access token nor refresh token is provided or valid.
    """

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


def extract_session_from_request():
    """
    Extract the access and refresh tokens from the request cookies. This function retrieves the
    session tokens from the request cookies, which are used to validate the user's session.

    :return: A tuple containing the access token and refresh token, or None if not found.
    """

    return tuple(
        request.cookies.get(cookie_name)
        for cookie_name in ["access_token", "refresh_token"]
    )


def validate_session():
    """
    Validate the current session by checking the access and refresh tokens. If the access token is
    valid, it sets the current session. If the access token is invalid but the refresh token is
    valid, it refreshes the session and sets the new access token. If neither token is valid, it
    raises an UnauthorizedException.

    :return: None
    :raises UnauthorizedException: If neither access token nor refresh token is valid.
    """

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

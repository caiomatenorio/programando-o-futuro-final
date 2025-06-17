"""
# Auth Service Module

This module provides authentication services, including user registration, login, logout, and
session management. It interacts with the user service and session service to handle user
authentication and session creation.
"""

from app.exceptions import SessionNotFoundException, UnauthorizedException
from app.extensions import db

from . import session_service, user_service


def register(name, email, password):
    """
    Register a new user with the provided name, email, and password. If the email is already in
    use, an exception is raised.

    :param name: The name of the user.
    :param email: The email of the user.
    :param password: The password for the user.
    :return: None
    :raises EmailAlreadyInUseException: If the email is already associated with an existing user.
    """

    user_service.create_user(name, email, password)


def login(email, password):
    """
    Login a user with the provided email and password. If the credentials are valid, a new session
    is created, and a JWT is generated. If the credentials are invalid, an exception is raised.

    :param email: The email of the user.
    :param password: The password for the user.
    :return: None
    :raises InvalidCredentialsException: If the email or password is incorrect.
    """

    with db.session.begin():
        user = user_service.validate_credentials(email, password, True)
        session = session_service.create_session(user.id)
        jwt = session_service.create_jwt(session.id, user.id, user.name, user.email)
        session_service.set_new_tokens(jwt, session.refresh_token)


def logout():
    """
    Logout the current user by deleting their session. If no session is found, an exception is raised.

    :return: None
    :raises UnauthorizedException: If the user is not authenticated or the session does not exist.
    """

    try:
        session_id = session_service.get_current_session_id()
        session_service.delete_session_by_id(session_id)
    except SessionNotFoundException:
        raise UnauthorizedException()


def is_authenticated():
    """
    Check if the current user is authenticated by validating the session. If the session is valid,
    it returns True; otherwise, it returns False.

    :return: True if the user is authenticated, False otherwise.
    :raises UnauthorizedException: If the session is not valid or does not exist.
    """

    try:
        session_service.validate_session()
        return True
    except UnauthorizedException:
        return False

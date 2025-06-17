"""
This module provides services related to user management, including creating users, validating
credentials, and managing user data.
"""

from flask import g

from app.exceptions import (
    EmailAlreadyInUseException,
    InvalidCredentialsException,
    UnauthorizedException,
    UserNotFoundException,
)
from app.extensions import bcrypt, db
from app.models.user import User


def user_exists(email, for_update=False):
    """
    Check if a user with the given email exists in the database. If `for_update` is True, the query
    will lock the row for update.

    :param email: The email of the user to check.
    :param for_update: If True, locks the row for update.
    :return: True if the user exists, False otherwise.
    """

    query = User.query.filter_by(email=email)

    if for_update:
        query = query.with_for_update()

    return query.first() is not None


def hash_password(password):
    """
    Hash a password using bcrypt.

    :param password: The password to hash.
    :return: The hashed password as a string.
    """

    return bcrypt.generate_password_hash(password).decode()


def check_password(password, password_hash):
    """
    Check if the provided password matches the hashed password.

    :param password: The plain text password to check.
    :param password_hash: The hashed password to compare against.
    :return: True if the passwords match, False otherwise.
    """

    return bcrypt.check_password_hash(password_hash, password)


def create_user(name, email, password):
    """
    Create a new user with the given name, email, and password. If a user with the given email
    already exists, an EmailAlreadyInUseException is raised.

    :param name: The name of the user.
    :param email: The email of the user.
    :param password: The password for the user.
    :return: None
    :raises EmailAlreadyInUseException: If a user with the given email already exists.
    """

    with db.session.begin():
        if user_exists(email, True):
            raise EmailAlreadyInUseException()

        user = User(name=name, email=email, password_hash=hash_password(password))  # type: ignore
        db.session.add(user)


def get_user_by_id(user_id, for_update=False):
    """
    Retrieve a user by their ID. If `for_update` is True, the query will lock the row for update.

    :param user_id: The ID of the user to retrieve.
    :param for_update: If True, locks the row for update.
    :return: The User object if found, None otherwise.
    """

    query = User.query.filter_by(id=user_id)

    if for_update:
        query = query.with_for_update()

    return query.first()


def get_user_by_id_or_raise(user_id, for_update=False):
    """
    Retrieve a user by their ID and raise an exception if the user is not found.

    :param user_id: The ID of the user to retrieve.
    :param for_update: If True, locks the row for update.
    :return: The User object if found.
    :raises UserNotFoundException: If the user with the given ID does not exist.
    """

    user = get_user_by_id(user_id, for_update)

    if not user:
        raise UserNotFoundException()

    return user


def get_user_by_email(email, for_update=False):
    """
    Retrieve a user by their email. If `for_update` is True, the query will lock the row for
    update.

    :param email: The email of the user to retrieve.
    :param for_update: If True, locks the row for update.
    :return: The User object if found, None otherwise.
    """

    query = User.query.filter_by(email=email)

    if for_update:
        query = query.with_for_update()

    return query.first()


def get_user_by_email_or_raise(email, for_update=False):
    """
    Retrieve a user by their email and raise an exception if the user is not found.

    :param email: The email of the user to retrieve.
    :param for_update: If True, locks the row for update.
    :return: The User object if found.
    :raises UserNotFoundException: If the user with the given email does not exist.
    """

    user = get_user_by_email(email, for_update)

    if not user:
        raise UserNotFoundException()

    return user


def validate_credentials(email, password, for_update=False):
    """
    Validate user credentials by checking if the user exists and if the provided password matches
    the stored password hash. If the user does not exist or the password is incorrect, an
    InvalidCredentialsException is raised.

    :param email: The email of the user to validate.
    :param password: The password to validate.
    :param for_update: If True, locks the row for update.
    :return: The User object if credentials are valid.
    :raises InvalidCredentialsException: If the credentials are invalid.
    """

    try:
        user = get_user_by_email_or_raise(email, for_update)
        if check_password(password, user.password_hash):
            return user
    except UserNotFoundException:
        pass
    raise InvalidCredentialsException()


def get_current_user():
    """
    Retrieve the current user from the Flask global context. The user information is expected to be
    stored in the global context (g) with keys 'user_id', 'name', and 'email'.

    :return: A dictionary containing the user's ID, name, and email.
    :raises UnauthorizedException: If the user information is not available in the global context.
    """

    user = {
        "id": g.get("user_id"),
        "name": g.get("name"),
        "email": g.get("email"),
    }

    if not all(user.values()):
        raise UnauthorizedException()
    return user


def fetch_and_lock_current_user():
    """
    Fetch the current user from the database and lock the row for update. This is useful for
    ensuring that the user data is not modified by another transaction while it is being updated.

    :return: The User object representing the current user.
    :raises UnauthorizedException: If the current user cannot be determined.
    """

    try:
        user_id = get_current_user()["id"]
        return get_user_by_id_or_raise(user_id, True)
    except UserNotFoundException:
        raise UnauthorizedException()


def update_current_user_name(name):
    """
    Update the name of the current user. The user's row is locked for update to prevent concurrent
    modifications.

    :param name: The new name for the user.
    :return: None
    """

    with db.session.begin():
        user = fetch_and_lock_current_user()
        user.name = name
        db.session.add(user)


def update_current_user_email(email):
    """
    Update the email of the current user. If a user with the given email already exists, an
    EmailAlreadyInUseException is raised. The user's row is locked for update to prevent concurrent
    modifications.

    :param email: The new email for the user.
    :return: None
    :raises EmailAlreadyInUseException: If a user with the given email already exists.
    """

    with db.session.begin():
        user = fetch_and_lock_current_user()

        if user_exists(email, True):
            raise EmailAlreadyInUseException()

        user.email = email
        db.session.add(user)


def update_current_user_password(current_password, new_password):
    """
    Update the password of the current user. The user's row is locked for update to prevent
    concurrent modifications. If the current password does not match the stored password hash, an
    InvalidCredentialsException is raised.

    :param current_password: The current password of the user.
    :param new_password: The new password for the user.
    :return: None
    :raises InvalidCredentialsException: If the current password does not match the stored password
        hash.
    """

    with db.session.begin():
        user = fetch_and_lock_current_user()

        if not check_password(current_password, user.password_hash):
            raise InvalidCredentialsException()

        user.password_hash = hash_password(new_password)
        db.session.add(user)


def delete_current_user(password):
    """
    Delete the current user from the database. The user's row is locked for update to prevent
    concurrent modifications. If the provided password does not match the stored password hash, an
    InvalidCredentialsException is raised.

    :param password: The password of the user to confirm deletion.
    :return: None
    :raises InvalidCredentialsException: If the provided password does not match the stored
        password hash.
    """

    with db.session.begin():
        user = fetch_and_lock_current_user()

        if not check_password(password, user.password_hash):
            raise InvalidCredentialsException()

        db.session.delete(user)

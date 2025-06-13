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
    query = User.query.filter_by(email=email)

    if for_update:
        query = query.with_for_update()

    return query.first() is not None


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode()


def check_password(password, password_hash):
    return bcrypt.check_password_hash(password_hash, password)


def create_user(name, email, password):
    with db.session.begin():
        if user_exists(email, True):
            raise EmailAlreadyInUseException()

        user = User(name=name, email=email, password_hash=hash_password(password))  # type: ignore
        db.session.add(user)


def get_user_by_id(user_id, for_update=False):
    query = User.query.filter_by(id=user_id)

    if for_update:
        query = query.with_for_update()

    return query.first()


def get_user_by_id_or_raise(user_id, for_update=False):
    user = get_user_by_id(user_id, for_update)

    if not user:
        raise UserNotFoundException()

    return user


def get_user_by_email(email, for_update=False):
    query = User.query.filter_by(email=email)

    if for_update:
        query = query.with_for_update()

    return query.first()


def get_user_by_email_or_raise(email, for_update=False):
    user = get_user_by_email(email, for_update)

    if not user:
        raise UserNotFoundException()

    return user


def validate_credentials(email, password, for_update=False):
    try:
        user = get_user_by_email_or_raise(email, for_update)
        if check_password(password, user.password_hash):
            return user
    except UserNotFoundException:
        pass
    raise InvalidCredentialsException()


def get_current_user():
    user = {
        "id": g.get("user_id"),
        "name": g.get("name"),
        "email": g.get("email"),
    }

    if not all(user.values()):
        raise UnauthorizedException()
    return user


def fetch_and_lock_current_user():
    user_id = get_current_user()["id"]
    return get_user_by_id_or_raise(user_id, True)


def update_current_user_name(name):
    with db.session.begin():
        user = fetch_and_lock_current_user()
        user.name = name
        db.session.add(user)


def update_current_user_email(email):
    with db.session.begin():
        user = fetch_and_lock_current_user()

        if user_exists(email, True):
            raise EmailAlreadyInUseException()

        user.email = email
        db.session.add(user)


def update_current_user_password(current_password, new_password):
    with db.session.begin():
        user = fetch_and_lock_current_user()

        if not check_password(current_password, user.password_hash):
            raise InvalidCredentialsException()

        user.password_hash = hash_password(new_password)
        db.session.add(user)


def delete_current_user(password):
    with db.session.begin():
        user = fetch_and_lock_current_user()

        if not check_password(password, user.password_hash):
            raise InvalidCredentialsException()

        db.session.delete(user)

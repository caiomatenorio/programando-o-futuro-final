from app.controllers.http_exceptions import (
    EmailAlreadyInUseException,
    InvalidCredentialsException,
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

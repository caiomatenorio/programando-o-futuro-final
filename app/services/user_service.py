from app.controllers.http_exceptions import EmailAlreadyInUseException
from app.extensions import bcrypt, db
from app.models.user import User


def user_exists(email, for_update=False):
    query = User.query.filter_by(email=email)

    if for_update:
        query = query.with_for_update()

    return query.first() is not None


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode()


def create_user(name, email, password):
    with db.session.begin():
        if user_exists(email, True):
            raise EmailAlreadyInUseException()

        user = User(name=name, email=email, password_hash=hash_password(password))  # type: ignore
        db.session.add(user)

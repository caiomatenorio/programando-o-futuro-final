from . import user_service


def register(name, email, password):
    user_service.create_user(name, email, password)

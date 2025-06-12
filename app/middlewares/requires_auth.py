from functools import wraps

from app.services import session_service


def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session_service.validate_session()
        return f(*args, **kwargs)

    return wrapper

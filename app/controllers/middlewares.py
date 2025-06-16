from flask import redirect, request, url_for

from app.exceptions import UnauthorizedException
from app.services import session_service
from app.services.session_service import add_session_cookies

from .blueprints import api, views

# API middlewares for the application


@api.before_request
def api_before_request():
    if request.endpoint in ["api.login", "api.register", "api.auth_status"]:
        return

    session_service.validate_session()


@api.after_request
def api_after_request(response):
    if request.endpoint in [
        "api.update_user_name",
        "api.update_user_email",
        "api.update_user_password",
    ]:
        response.delete_cookie("access_token", path="/")
    return response


# Views middlewares for the application


@views.before_request
def views_before_request():
    if request.endpoint == "views.index":
        return

    if request.endpoint in ["views.login", "views.register"]:
        try:
            session_service.validate_session()
            return redirect(url_for("views.home"))
        except UnauthorizedException:
            return

    try:
        session_service.validate_session()
    except UnauthorizedException:
        return redirect(url_for("views.login"))


@views.after_request
def views_after_request(response):
    return add_session_cookies(response)

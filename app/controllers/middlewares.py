from flask import redirect, request, url_for

from app.exceptions import UnauthorizedException
from app.services import session_service
from app.services.session_service import add_session_cookies

from .blueprints import api, views

# API middlewares for the application


@api.before_request
def api_before_request():
    PUBLIC_ENDPOINTS = ["api.login", "api.register", "api.auth_status"]

    if request.endpoint in PUBLIC_ENDPOINTS:
        return

    session_service.validate_session()


# Views middlewares for the application


@views.before_request
def views_before_request():
    PUBLIC_ENDPOINTS = ["views.index", "views.login", "views.register"]

    if request.endpoint in PUBLIC_ENDPOINTS:
        try:
            session_service.validate_session()
            redirect(url_for("views.home"))
        except UnauthorizedException:
            return

    try:
        session_service.validate_session()
    except UnauthorizedException:
        return redirect(url_for("views.login"))


@views.after_request
def views_after_request(response):
    return add_session_cookies(response)

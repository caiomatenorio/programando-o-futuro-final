from flask import redirect, request, url_for

from app.exceptions import UnauthorizedException
from app.services import session_service

from .blueprints import api, views

# API middlewares for the application


@api.before_request
def api_middleware():
    PUBLIC_ENDPOINTS = ["api.login", "api.register", "api.auth_status"]

    if request.endpoint in PUBLIC_ENDPOINTS:
        return

    session_service.validate_session()


# Views middlewares for the application

# FIXME - Uncomment the following code when the login and register views are implemented
# @views.before_request
# def views_middleware():
#     PUBLIC_ENDPOINTS = ["views.index", "views.login", "views.register"]

#     if request.endpoint in PUBLIC_ENDPOINTS:
#         return

#     try:
#         session_service.validate_session()
#     except UnauthorizedException:
#         return redirect(url_for("views.login"))

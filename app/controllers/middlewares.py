"""
Middlewares for the application blueprints to handle session validation and cookie management.
"""

from flask import redirect, request, url_for

from app.exceptions import UnauthorizedException
from app.services import session_service
from app.services.session_service import add_session_cookies

from .blueprints import api, views

# API middlewares for the application


@api.before_request
def api_before_request():
    """
    Middleware to validate the session for API requests. It checks if the user is authenticated
    before allowing access to any API endpoints except for login, register, and auth status endpoints.

    :return: None
    :raises UnauthorizedException: If the session is invalid or the user is not authenticated.
    """

    if request.endpoint in ["api.login", "api.register", "api.auth_status"]:
        return

    session_service.validate_session()


@api.after_request
def api_after_request(response):
    """
    Middleware to forcefully remove the access token cookie from the response for specific API endpoints.
    This is done to ensure that the user information is updated correctly after certain actions,
    such as updating user details.

    :return: The response object with the access token cookie removed for specific endpoints.
    """

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
    """
    Middleware to validate the session for view requests. It checks if the user is authenticated
    before allowing access to any view endpoints except for the index, login, and register pages.
    If the user is authenticated and tries to access the login or register pages, they are redirected
    to the home page. If the session is invalid, the user is redirected to the login page.

    :return: None
    """

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
    """
    Middleware to add session cookies to the response for view requests. This ensures that the
    session cookies are set correctly for the user's browser after each request.

    :return: The response object with session cookies added.
    """
    return add_session_cookies(response)

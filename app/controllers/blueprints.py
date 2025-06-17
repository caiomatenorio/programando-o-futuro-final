"""
Blueprints for organizing routes in the application.
"""

from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")
"""
Blueprint for API routes. This blueprint is used to group all API-related routes under the
"/api" URL prefix. It allows for better organization of the application and makes it easier to
manage routes related to the API functionality.
"""

views = Blueprint("views", __name__, url_prefix="/")
"""
Blueprint for views. This blueprint is used to group all view-related routes under the
"/" URL prefix. It allows for better organization of the application and makes it easier to manage
routes related to the web views of the application.
"""

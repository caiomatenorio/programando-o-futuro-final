from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")
views = Blueprint("views", __name__, url_prefix="/")

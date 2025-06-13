from flask import Blueprint, jsonify, request, render_template

bp = Blueprint("view_home", __name__, url_prefix="/home")


@bp.get("/home")
def index():
    return render_template("home.html")

from flask import Blueprint, jsonify, request, render_template

bp = Blueprint("view_whoAmI", __name__, url_prefix="/games/who-am-i")


@bp.get("/")
def index():
    return render_template("whoAmI.html")

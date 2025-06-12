from flask import Blueprint, jsonify, request, render_template

bp = Blueprint("view_memoryGame", __name__, url_prefix="/games/memory-game")


@bp.get("/")
def index():
    return render_template("memoryGame.html")

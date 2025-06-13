from flask import render_template

from app.controllers.blueprints import views


@views.get("/games/memory-game")
def memory_game():
    return render_template("memoryGame.html")

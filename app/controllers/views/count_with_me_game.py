from flask import render_template

from app.controllers.blueprints import views


@views.get("/games/count-with-me-game")
def memory_game():
    return render_template("countWithMeGame.html")
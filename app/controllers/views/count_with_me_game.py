from flask import render_template

from app.controllers.blueprints import views


@views.get("/jogos/conte-comigo")
def count_with_me_game():
    return render_template("countWithMeGame.html")
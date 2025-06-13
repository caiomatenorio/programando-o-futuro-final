from flask import render_template

from app.controllers.blueprints import views


@views.get("/jogos/jogo-das-cores")
def color_game():
    return render_template("colorGame.html")

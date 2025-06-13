from flask import render_template

from app.controllers.blueprints import views


@views.get("/jogos/jogo-da-memoria")
def memory_game():
    return render_template("memoryGame.html")

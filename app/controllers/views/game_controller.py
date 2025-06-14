from flask import render_template

from app.controllers.blueprints import views


@views.get("/jogos/jogo-da-memoria")
def memory_game():
    return render_template("memoryGame.html")


@views.get("/jogos/quem-sou-eu")
def who_am_i_game():
    return render_template("whoAmI.html")

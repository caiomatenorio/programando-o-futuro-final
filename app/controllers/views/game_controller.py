from flask import render_template

from app.controllers.blueprints import views


@views.get("/jogos/vamos-contar")
def count_with_me_game():
    return render_template("count-with-me-game.html")


@views.get("/jogos/jogo-da-memoria")
def memory_game():
    return render_template("memory-game.html")


@views.get("/jogos/quem-sou-eu")
def who_am_i_game():
    return render_template("who-am-i-game.html")


@views.get("/jogos/jogo-das-cores")
def color_game():
    return render_template("color-game.html")

from flask import render_template

from app.controllers.blueprints import api


@api.get("/jogos/quem-sou-eu")
def who_am_i_game():
    return render_template("whoAmI.html")

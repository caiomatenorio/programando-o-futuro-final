from flask import render_template

from app.controllers.blueprints import api


@api.get("/jogos/quem-sou-eu")
def index():
    return render_template("whoAmI.html")

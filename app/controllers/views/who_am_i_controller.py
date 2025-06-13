from flask import render_template

from app.controllers.blueprints import views


@views.get("/jogos/quem-sou-eu")
def index():
    return render_template("whoAmI.html")

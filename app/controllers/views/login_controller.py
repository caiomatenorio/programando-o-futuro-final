from flask import render_template

from app.controllers.blueprints import views


@views.get("/entrar")
def login():
    return render_template("login.html")

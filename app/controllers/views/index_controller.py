from flask import render_template

from app.controllers.blueprints import views


@views.get("/")
def index():
    return render_template("home.html")

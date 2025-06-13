from flask import render_template

from app.controllers.blueprints import views


@views.get("/inicio")
def home():
    return render_template("home.html")

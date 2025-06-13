from flask import render_template

from app.controllers.blueprints import views


@views.get("/home")
def home():
    return render_template("home.html")

from flask import render_template

from app.controllers.blueprints import api


@api.get("/login")
def login():
    return render_template("login.html")

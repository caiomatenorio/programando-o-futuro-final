from app.controllers.blueprints import views
from app.utils import render_template_with_auth


@views.get("/inicio")
def home():
    return render_template_with_auth("home.html")

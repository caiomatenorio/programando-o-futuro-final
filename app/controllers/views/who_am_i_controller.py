from app.controllers.blueprints import api
from app.utils import render_template_with_auth


@api.get("/jogos/quem-sou-eu")
def who_am_i_game():
    return render_template_with_auth("whoAmI.html")

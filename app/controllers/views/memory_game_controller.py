from app.controllers.blueprints import views
from app.utils import render_template_with_auth


@views.get("/jogos/jogo-da-memoria")
def memory_game():
    return render_template_with_auth("memoryGame.html")

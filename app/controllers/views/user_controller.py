from flask import render_template, request

from app.controllers.blueprints import views
from app.services import user_service


@views.get("/minha-conta")
def my_account():
    editar = request.args.get("editar")
    delete = request.args.get("excluir") is not None
    user = user_service.get_current_user()
    return render_template(
        "my-account.html",
        editar=editar,
        name=user["name"],
        email=user["email"],
        delete=delete,
    )

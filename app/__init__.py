def create_app():
    from flask import Flask

    from config import Config

    from . import models
    from .controllers.blueprints import api, views
    from .extensions import bcrypt, db, ma, migrate

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    bcrypt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api)
    app.register_blueprint(views)
    app.url_map.strict_slashes = False

    return app

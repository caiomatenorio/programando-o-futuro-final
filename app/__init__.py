def create_app():
    from flask import Flask

    from config import Config

    from . import models
    from .controllers import blueprints
    from .controllers.error_handlers import error_handlers
    from .extensions import bcrypt, db, ma, migrate

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    bcrypt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    for error, handler in error_handlers.items():
        app.register_error_handler(error, handler)

    return app

def create_app():
    from flask import Flask

    from app.extensions import db, ma, migrate
    from config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    return app

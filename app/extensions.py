from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# SQLALchemy
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Marshmallow
ma = Marshmallow()

# Flask-Migrate
migrate = Migrate()

# Bcrypt
bcrypt = Bcrypt()

# Flask JWT Extended
jwt = JWTManager()

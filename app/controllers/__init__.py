from .api import blueprints as api_blueprints
from .views import blueprints as view_blueprints

blueprints = api_blueprints + view_blueprints

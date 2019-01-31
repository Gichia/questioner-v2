from flask import Flask
from app.api.utils.errors import bad_request, internal_server_error, not_found
from app.api.views.user_views import ver2 as v2
from app.api.views.meetup_views import ver2 as v2
from app.api.views.question_views import ver2 as v2
from app.api.views.home import ver2 as v2
from instance.config import app_config


def create_app(config_name):
    """function creating the flask app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(v2)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, bad_request)
    app.register_error_handler(500, internal_server_error)
    return app
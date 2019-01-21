from flask import Flask
from .api.v2.utils.errors import bad_request, internal_server_error, not_found
from .api.v2.views.user_views import ver2 as v2
from .api.v2.views.meetup_views import ver2 as v2


def create_app(config):
    '''function creating the flask app'''
    app = Flask(__name__)
    app.register_blueprint(v2)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, bad_request)
    app.register_error_handler(500, internal_server_error)
    return app
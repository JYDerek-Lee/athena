from flask import Flask
from app.http.api import public_api


def create_app(config_name="default", settings_override=None):
    app = Flask(__name__)
    app.register_blueprint(public_api, url_prefix="/pub")
    return app

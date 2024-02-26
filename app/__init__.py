from flask import Flask
from .controllers.main_controller import main_controller
from .controllers.auth_controller import auth_controller
from .controllers.registration_controller import registration_controller

import os

def create_app():
    app = Flask(__name__)

    # Registra los Blueprints
    app.secret_key = os.urandom(24)
    app.register_blueprint(main_controller)
    app.register_blueprint(auth_controller)
    app.register_blueprint(registration_controller)

    return app

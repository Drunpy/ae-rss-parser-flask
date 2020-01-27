from flask import Flask
from flask_jwt import JWT
from .security import authenticate, identity

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "Lorosa"
    jwt = JWT(app, authenticate, identity)

    from . import main
    app.register_blueprint(main.bp)
    return app

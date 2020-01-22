from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__)

    from . import main
    app.register_blueprint(main.bp)
    return app

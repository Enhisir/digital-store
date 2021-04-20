from flask import Flask
from app.store.manager import store_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.ProductionConfig")

    app.register_blueprint(store_blueprint)

    return app

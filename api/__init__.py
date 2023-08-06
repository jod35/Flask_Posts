# app.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    #load environment variables from .env
    app.config.from_prefixed_env()
    @app.shell_context_processor
    def make_shell():
        return {
            'app':app
        }

    return app

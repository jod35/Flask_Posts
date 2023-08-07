# app.py
from flask import Flask
from .exts import db, migrate, api, jwt
from .posts.routes import posts_nspace
from .users.routes import users_nspace


def create_app():
    """
    App factory.
    - Create an instance of it to configure app for many scenarios

    Returns:
        app : A Flask application instance
    """
    app = Flask(__name__)

    # load environment variables from .env
    app.config.from_prefixed_env()

    # initialize third party apps
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    # register all namespaces
    api.add_namespace(posts_nspace, path="/v1")

    api.add_namespace(users_nspace, path="/v1")

    # exposee some vars to Flask shell
    @app.shell_context_processor
    def make_shell():
        return {"db": db}

    return app

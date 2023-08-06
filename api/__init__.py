# app.py
from flask import Flask
from .exts import db, migrate, api, jwt
from .posts.routes import posts_bp
from .users.routes import users_bp


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
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register all blueprints
    app.register_blueprint(posts_bp, url_prefix="/v1")
    app.register_blueprint(users_bp, url_prefix="/v1")

    @app.shell_context_processor
    def make_shell():
        return {"db": db, "app": app}

    return app

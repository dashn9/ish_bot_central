from flask import Flask

from .blueprints import bot_identity


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db

    db.init_app(app)
    app.register_blueprint(bot_identity.identity_bp)

    return app

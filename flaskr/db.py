from flask import current_app, g
from pymongo import MongoClient


def get_db():
    if "mongo_db" not in g:
        g.mongo_db = MongoClient(
            current_app.config["MONGO_HOST"],
            current_app.config["MONGO_PORT"],
            username=current_app.config["MONGO_USERNAME"],
            password=current_app.config["MONGO_PASSWORD"],
        )

    return g.mongo_db


def close_db(e=None):
    mongo_db = g.pop("mongo_db", None)
    if mongo_db:
        mongo_db.close()


def init_app(app):
    app.teardown_appcontext(close_db)

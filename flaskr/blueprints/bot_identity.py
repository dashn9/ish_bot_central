import json
from flask import Blueprint, jsonify, request
from flaskr.db import get_db

from flaskr.services.bot_identity import IdentityService
from flaskr.services.ads import AdService

identity_bp = Blueprint("identity", __name__, url_prefix="/api/bots/identity")


def update_visit_count(identity_id):
    """Updates the visit count for the provided identity in the database.

    Args:
        identity_id (str): The ID of the identity whose visit count needs to be incremented.
    """

    mongo_db = get_db()
    collection.update_one({"_id": identity_id}, {"$inc": {"HAS_VISITED_TODAY": 1}})


@identity_bp.route("/<string:method>/", defaults={"value": None}, methods=["GET"])
@identity_bp.route("/<string:method>/<string:value>/", methods=["GET"])
def get_identity(method, value):

    identity_service = IdentityService(db_client=get_db())
    ad_service = AdService()

    if method == "random":
        identity = identity_service.get_identity(method)
    else:
        if value is None:
            return jsonify({"error": "Value is required for this method"}), 400

        identity = identity_service.get_identity(method, json.loads(value))

    ad_service.insert_monetag_ads_attribs_to_identity(identity)
    return jsonify(identity)


@identity_bp.route("/<int:identity_id>/timezone/", methods=["GET"])
def fetch_timezone(identity_id: int):

    identity_service = IdentityService(db_client=get_db())
    timezone = identity_service.get_timezone(
        request.environ.get("HTTP_X_REAL_IP", request.remote_addr), identity_id
    )
    return jsonify(timezone)


@identity_bp.route("/<int:identity_id>/cookies/", methods=["PUT"])
def update_cookies(identity_id: int):
    cookies = request.json
    identity_service = IdentityService(db_client=get_db())
    cookies = identity_service.update_cookies(identity_id, cookies)
    return jsonify(cookies)

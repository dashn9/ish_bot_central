import json
from flask import Blueprint, jsonify
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


@identity_bp.route("/<string:method>/<string:value>", methods=["GET"])
def get_identity(method, value):
    """Handles GET requests to the root route, retrieving and processing identity data."""

    identity_service = IdentityService(db_client=get_db())
    ad_service = AdService()

    identity = identity_service.get_identity(method, json.loads(value))
    ad_service.insert_monetag_ads_attribs_to_identity(identity)
    return jsonify(identity)

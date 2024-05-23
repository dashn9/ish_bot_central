from flask import Blueprint, jsonify

from flaskr.services.urls import UrlService

url_bp = Blueprint("urls", __name__, url_prefix="/api/url/")


@url_bp.route("/<string:index>/", methods=["GET"])
def get_identity(index):
    """Handles GET requests to the root route, retrieving and processing identity data."""

    url_service = UrlService()
    if index == "random":
        url_to_use = url_service.fetch_random_url()
    return jsonify(url_to_use)

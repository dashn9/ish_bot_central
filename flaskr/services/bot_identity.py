from pymongo import MongoClient
from flaskr.models.identity import BotIdentityModel


class IdentityService:
    __bot_identity_model = None

    def __init__(self, db_client: MongoClient) -> None:
        self.__bot_identity_model = BotIdentityModel(db_client)

    def get_identity(self, method: str, value: dict | str | int) -> dict:
        identity = {}
        if method == "id":
            identity = self.__bot_identity_model.fetch_identity_by_id(value)

        identity.pop("_id")
        identity.pop("FULL_TIMEZONE_INFO")
        return identity

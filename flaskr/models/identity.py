from pymongo import MongoClient
from ._model import MongoBaseModel


class BotBaseModel:
    def get_database(self) -> str:
        return "bots"


class BotIdentityModel(BotBaseModel, MongoBaseModel):
    def __init__(self, db_client: MongoClient) -> None:
        super().__init__(db_client)

    def fetch_identity_by_id(self, id: int) -> dict:
        return self.find(id=id)

    def get_collection(self) -> str:
        return "identities"

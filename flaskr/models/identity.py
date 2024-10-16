from pymongo import MongoClient
from ._model import MongoBaseModel


class BotBaseModel:
    def get_database(self) -> str:
        return "bots"


class BotIdentityModel(BotBaseModel, MongoBaseModel):
    def __init__(self, db_client: MongoClient) -> None:
        super().__init__(db_client)

    def fetch_identity_by_id(self, id: int) -> dict:
        return self.find(ID=id)

    def fetch_random_identity(self, filter: dict = None) -> dict:
        pipeline = [{"$sample": {"size": 1}}]
        if filter:
            pipeline.insert(0, {"$match": filter})
        result = self.aggregate(pipeline)
        return result[0] if result else {}

    def update_timezone_details(self, timezone: dict):
        return self.update(TIMEZONE=timezone)

    def update_cookies(self, cookies: list):
        return self.update(COOKIES=cookies)

    def get_collection(self) -> str:
        return "identities"

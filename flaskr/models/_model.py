from abc import ABC, abstractmethod
from pymongo import MongoClient


class MongoBaseModel(ABC):
    __db_client = None
    models = []

    def __init__(self, db_client: MongoClient) -> None:
        self.__db_client = db_client

    def find(self, **kwargs) -> dict:
        item: dict = self.__db_client[self.get_database()][
            self.get_collection()
        ].find_one(kwargs)
        self.models = [item]

        return item

    def update(self, **kwargs) -> bool:
        for model in self.models:
            self.__db_client[self.get_database()][self.get_collection()].update_one(
                {"ID": model["ID"]}, {"$set": kwargs}
            )
        return True

    @abstractmethod
    def get_database(self) -> str:
        pass

    @abstractmethod
    def get_collection(self) -> str:
        pass

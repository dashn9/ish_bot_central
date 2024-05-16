from abc import ABC, abstractmethod
from pymongo import MongoClient


class MongoBaseModel(ABC):
    __db_client = None

    def __init__(self, db_client: MongoClient) -> None:
        self.__db_client = db_client

    def find(self, remove_object_id=True, **kwargs) -> dict:
        item: dict = self.__db_client[self.get_database()][
            self.get_collection()
        ].find_one(kwargs)

        return item

    @abstractmethod
    def get_database(self) -> str:
        pass

    @abstractmethod
    def get_collection(self) -> str:
        pass

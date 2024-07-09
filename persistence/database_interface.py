from abc import ABC
from abc import abstractmethod

from google.cloud.firestore_v1.collection import CollectionReference


class DatabaseInterface(ABC):
    @abstractmethod
    def get_users(self) -> CollectionReference:
        raise NotImplementedError()

    @abstractmethod
    def get_user_availability(self) -> CollectionReference:
        raise NotImplementedError()

from typing import Union

from persistence.database import Database
from persistence.database_interface import DatabaseInterface


class DatabaseFactory:
    _instance: Union[DatabaseInterface, None] = None

    @classmethod
    def build(cls) -> DatabaseInterface:
        if cls._instance:
            return cls._instance

        cls._instance = Database()
        return cls._instance

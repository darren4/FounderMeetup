import os
from typing import Literal
from pydantic import BaseModel
import firebase_admin
from firebase_admin import firestore
from google.cloud import firestore as google_firestore
from google.cloud.firestore_v1.collection import CollectionReference


class DatabaseConfig(BaseModel):
    database_type: Literal["Emulator", "Deployed"] 


class Database:
    def __init__(self, config: DatabaseConfig):
        if os.getenv("ENV") == "LOCAL":
            os.environ["FIRESTORE_DATASET"] = "test"
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8001"
            os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8001/firestore"
            os.environ["FIRESTORE_HOST"] = "http://localhost:8001"
            os.environ["FIRESTORE_PROJECT_ID"] = "test"

        app: firebase_admin.App = firebase_admin.initialize_app()
        db: google_firestore.Client = firestore.client()
        self._users_collection: CollectionReference = db.collection("Users")
        self._user_availability_collection: CollectionReference = db.collection("UserAvailability")

    def get_users(self) -> CollectionReference:
        return self._users_collection
    
    def get_user_availability(self) -> CollectionReference:
        return self._user_availability_collection

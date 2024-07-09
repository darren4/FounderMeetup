import os

import firebase_admin
from firebase_admin import firestore
from google.cloud import firestore as google_firestore
from google.cloud.firestore_v1.collection import CollectionReference

from persistence.database_interface import DatabaseInterface


class Database(DatabaseInterface):
    def __init__(self):
        # TODO: remove if statement
        if os.getenv("ENV") == "LOCAL":
            os.environ["FIRESTORE_DATASET"] = "test"
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8001"
            os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8001/firestore"
            os.environ["FIRESTORE_HOST"] = "http://localhost:8001"
            os.environ["FIRESTORE_PROJECT_ID"] = "test"

        firebase_admin.initialize_app()
        db: google_firestore.Client = firestore.client()
        self._users_collection: CollectionReference = db.collection("Users")
        self._user_availability_collection: CollectionReference = db.collection(
            "UserAvailability"
        )

    def get_users(self) -> CollectionReference:
        return self._users_collection

    def get_user_availability(self) -> CollectionReference:
        return self._user_availability_collection

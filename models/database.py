# models/database.py
import firebase_admin
from firebase_admin import firestore

import os


env = os.getenv("ENV")

if env == "LOCAL":
    os.environ["FIRESTORE_DATASET"] = "test"
    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8001"
    os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8001/firestore"
    os.environ["FIRESTORE_HOST"] = "http://localhost:8001"
    os.environ["FIRESTORE_PROJECT_ID"] = "test"

app = firebase_admin.initialize_app()
db = firestore.client()

user = db.collection("Users")
user_availability = db.collection("UserAvailability")


# Define Class to use to map Mongodb Data for user login
class User:
    """Class Definition to handle Flask login for user"""

    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

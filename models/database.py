# models/database.py
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

client = MongoClient(dotenv_values(".env").get("MONGO_DB_CONNECTION_STRING"), server_api=ServerApi('1'))

# Access a database from the client 
db = client["FounderMeetup"]
user = db["Users"] # Example Users

# Define Class to use to map Mongodb Data for user login
class User:
    """Class Definition to handle Flask login for user"""
    def __init__(self, username, id):
        self.username = username
        self.id = id

    @staticmethod 
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id
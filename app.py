from flask import Flask
from blueprints.main_blueprint import main_views
from blueprints.auth_blueprint import auth_views
from blueprints.professional_support_blueprint import professional_support_views
from blueprints.peer_meetup_blueprint import peer_meetup_views

from flask_login import LoginManager
from models.database import db, user, User
from bson import ObjectId
from dotenv import dotenv_values

# create an instance of the flask application
app = Flask(__name__)

app.secret_key = dotenv_values(".env").get("FLASK_SECRET_KEY")
app.register_blueprint(main_views)
app.register_blueprint(auth_views)
app.register_blueprint(professional_support_views)
app.register_blueprint(peer_meetup_views)

login = LoginManager(app)
login.login_view = "/login"

# setup the login user loader
@login.user_loader #3
def load_user(id):
    """Confirm user exists in database then use else return None"""
    cur_user = user.find_one({"_id": ObjectId(id)})

    if cur_user is None:
        return None

    # Create a user instance from the retrieved user
    return User(cur_user.get("username"), str(cur_user.get("_id")))
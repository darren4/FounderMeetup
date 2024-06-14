from flask import Blueprint, request

main_views = Blueprint("main", __name__)

@main_views.get("/", strict_slashes=False)
def index():
    return "<h1>This is the Home Page</h1>"

@main_views.get("/profile/<string:username>", strict_slashes=False)
def profile(username):
    return f"<h1>Welcome {username}! This is your profile</h1>"

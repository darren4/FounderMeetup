from flask import Blueprint, render_template
from flask_login import login_required

main_views = Blueprint("main", __name__)


# Create routes on this blueprint instance
@main_views.get("/", strict_slashes=False)
def index():
    # Define application logic for homepage
    return render_template("index.html")


@main_views.get("/profile/<string:username>", strict_slashes=False)
@login_required
def profile(username):
    # Define application logic for profile page
    return render_template("profile.html", username=username)

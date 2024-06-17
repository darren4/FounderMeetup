from flask import Blueprint, render_template
from flask_login import login_required


peer_meetup_views = Blueprint("peer_meetup", __name__)


@peer_meetup_views.get("/peermeetup", strict_slashes=False)
@login_required
def peer_meetup():
    # Define application logic for profile page
    return render_template("peer_meetup.html")

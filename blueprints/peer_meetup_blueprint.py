from flask import Blueprint, render_template, request
from flask_login import login_required


peer_meetup_views = Blueprint("peer_meetup", __name__)


@peer_meetup_views.route("/peermeetup", strict_slashes=False, methods=["GET", "POST"])
@login_required
def peer_meetup():
    if request.method == "POST":
        print(request.form.get("sunday-morning"))

    return render_template("peer_meetup.html")

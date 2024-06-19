from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from typing import List, Final, Set


peer_meetup_views = Blueprint("peer_meetup", __name__)


TIMES: Final[List[str]] = [
    "sunday-morning",
    "sunday-afternoon",
    "monday-morning",
    "monday-afternoon",
    "tuesday-morning",
    "tuesday-afternoon",
    "wednesday-morning",
    "wednesday-afternoon",
    "thursday-morning",
    "thursday-afternoon",
    "friday-morning",
    "friday-afternoon",
    "saturday-morning",
    "saturday-afternoon",
]


@peer_meetup_views.route("/peermeetup", strict_slashes=False, methods=["GET", "POST"])
@login_required
def peer_meetup():
    if request.method == "POST":
        availabilities: Set[str] = {
            time for time in TIMES if request.form.get(time) == "on"
        }
        print(current_user)
        username: str = current_user.username
        print(current_user.id)
        print(username)

        flash("Times submitted, will email if connected", "info")

    return render_template("peer_meetup.html")

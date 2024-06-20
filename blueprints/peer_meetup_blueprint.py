from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from models.database import user_availability
from typing import List, Final, Set, Dict, Any


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
        user_id: str = current_user.id
        user_availability.delete_many({"user_id": user_id})

        ready_times: List[str] = [
            time for time in TIMES if request.form.get(time) == "on"
        ]
        ready_times_regex: str = "|".join(ready_times)
        match: Any = user_availability.find_one_and_delete({"ready-times", {"$regex": ready_times_regex}})
        
        if match:
            
            # TODO: send email


        flash("Times submitted, will email if connected", "info")

    return render_template("peer_meetup.html")

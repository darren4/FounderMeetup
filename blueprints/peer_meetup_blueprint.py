from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from models.database import user_availability, user
from typing import List, Final, Set, Dict, Any
from bson.objectid import ObjectId
from google.cloud.firestore_v1.base_query import FieldFilter
from enum import Enum
from firebase_admin import firestore


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


class UserAvailabilityFields(Enum):
    AVAILABILITIES = "availabilities"
    UPDATE_TIME = "update_time"


@peer_meetup_views.route("/peermeetup", strict_slashes=False, methods=["GET", "POST"])
@login_required
def peer_meetup():
    if request.method == "POST":
        current_username: str = current_user.username
        user_availability.document(current_username).delete()

        availability: List[str] = [
            time for time in TIMES if request.form.get(time) == "on"
        ]
        matches = user_availability.where(
            filter=FieldFilter(
                UserAvailabilityFields.AVAILABILITIES.value,
                "array_contains_any",
                availability,
            )
        ).order_by(UserAvailabilityFields.UPDATE_TIME.value).limit(1).get()

        if matches:
            match = matches[0]
            match.reference.delete()
            matched_username = match.id
            matched_email = user.document(matched_username).get().get("email")
            flash(f"Matched with user with email {matched_email}")
            # TODO: send emails
        else:
            user_availability.document(current_username).set({
                UserAvailabilityFields.UPDATE_TIME.value: firestore.SERVER_TIMESTAMP,
                UserAvailabilityFields.AVAILABILITIES.value: availability
            })
            flash("Times submitted", "info")

    return render_template("peer_meetup.html")

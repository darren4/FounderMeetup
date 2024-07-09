from enum import Enum
from typing import Final
from typing import List

from firebase_admin import firestore
from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import login_required
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.base_query import QueryType
from google.cloud.firestore_v1.collection import CollectionReference

from persistence.database_factory import DatabaseFactory
from persistence.database_interface import DatabaseInterface


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

        database: DatabaseInterface = DatabaseFactory.build()
        user_availability: CollectionReference = database.get_user_availability()
        user_availability.document(current_username).delete()

        availability: List[str] = [
            time for time in TIMES if request.form.get(time) == "on"
        ]
        matches: QueryType = (
            user_availability.where(
                filter=FieldFilter(
                    UserAvailabilityFields.AVAILABILITIES.value,
                    "array_contains_any",
                    availability,
                )
            )
            .order_by(UserAvailabilityFields.UPDATE_TIME.value)
            .limit(1)
            .get()
        )

        if matches:
            match: DocumentSnapshot = matches[0]
            match.reference.delete()
            matched_username = match.id
            users: CollectionReference = database.get_users()
            matched_email: str = users.document(matched_username).get().get("email")
            flash(f"Matched with user with email {matched_email}")
            # TODO: send emails
        else:
            user_availability.document(current_username).set(
                {
                    UserAvailabilityFields.UPDATE_TIME.value: firestore.SERVER_TIMESTAMP,
                    UserAvailabilityFields.AVAILABILITIES.value: availability,
                }
            )
            flash("Times submitted", "info")

    return render_template("peer_meetup.html")

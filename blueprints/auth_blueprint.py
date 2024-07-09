# Update file blueprints/auth_blueprints
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.base_query import QueryType
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from models.user import User
from persistence.database_factory import DatabaseFactory
from persistence.database_interface import DatabaseInterface


auth_views = Blueprint("auth", __name__)


@auth_views.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = {
            "email": email,
            "password": generate_password_hash(password),
        }
        users: CollectionReference = DatabaseFactory.build().get_users()
        existing_user: DocumentReference = users.document(username).get()
        if existing_user.exists:
            flash("Username already in use", "error")
            return redirect("/register")

        existing_with_email: QueryType = users.where(
            filter=FieldFilter("email", "==", email)
        ).get()
        if existing_with_email:
            flash("Email already in use", "error")
            return redirect("/register")

        users.document(username).set(new_user)
        return redirect("/login")

    return render_template("register.html")


@auth_views.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        user_password = request.form.get("password")

        users: CollectionReference = DatabaseFactory.build().get_users()
        find_user: DocumentReference = users.document(username).get()

        if not find_user.exists:
            flash("Invalid Login Credentials!", "error")
            return redirect("/login")

        is_valid_password = check_password_hash(
            find_user.get("password"), user_password
        )

        if not is_valid_password:
            flash("Invalid Login Credentials!", "error")
            return redirect("/login")

        log_user = User(username)
        login_user(log_user)

        return redirect("/")
    return render_template("login.html")


@auth_views.route("/logout", strict_slashes=False)
@login_required
def logout():
    logout_user()
    return redirect("/")


@auth_views.route("/deleteaccount", strict_slashes=False, methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        username = request.form.get("username")

        if username != current_user.username:
            flash(
                f"Username entered incorrectly, your username is {current_user.username}"
            )
        else:
            database: DatabaseInterface = DatabaseFactory.build()
            user_availability: CollectionReference = database.get_user_availability()
            user_availability.document(username).delete()
            users: CollectionReference = database.get_users()
            users.document(username).delete()

            logout_user()
            return redirect("/")

    # When it's a GET request we sent the html form
    return render_template("delete_account.html")

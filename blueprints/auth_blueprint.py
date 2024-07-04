# Update file blueprints/auth_blueprints
from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import user, user_availability
from google.cloud.firestore_v1.base_query import FieldFilter


auth_views = Blueprint("auth", __name__)


# Create routes on this blueprint instance
@auth_views.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    # Define application logic for homepage
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = {
            "email": email,
            "password": generate_password_hash(password),
        }
        try:
            # Check if the email/username already exists in db
            existing_user = user.document(username).get()
            if existing_user.exists:
                flash("Username already in use", "error")
                return redirect("/register")

            existing_with_email = user.where(
                filter=FieldFilter(
                    "email",
                    "==",
                    email
                )
            ).get()
            if existing_with_email:
                flash("Email already in use", "error")
                return redirect("/register")

            user.document(username).set(new_user)
            return redirect("/login")

        # If any error occurs, we can catch it
        except Exception as e:
            print(e)
            flash("Error occured during registration. Try again!", "error")
            return (redirect("/register"),)

    # When it's a GET request we sent the html form
    return render_template("register.html")


@auth_views.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    # Define application logic for profile page
    # If a user alredy exists and tries to be funny by
    # manually entering the /login route, they should be
    # redirected to the index page
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        # Enter logic for processing registration
        from models.database import user, User

        # Get username and password from the form
        username = request.form.get("username")
        user_password = request.form.get("password")

        # Retrieve user from the database with username
        find_user = user.document(username).get()

        # Return an error if user not in database
        if not find_user.exists:
            flash("Invalid Login Credentials!", "error")
            return redirect("/login")

        # Compare the user's password with the password returned from db

        is_valid_password = check_password_hash(
            find_user.get("password"), user_password
        )

        # If password does not match, redirect user to login again
        if not is_valid_password:
            flash("Invalid Login Credentials!", "error")
            return redirect("/login")

        # At this point all is well; so instantiate the User class
        # This is to enable the Flask-Login Extension kick in
        log_user = User(username)

        # use the login_user function imported from flask_login
        login_user(log_user)

        # Then return the user to the index page after sucess
        return redirect("/")

        # Make sure to do proper error handling with try/except
        # I don't want to make the code too bulky

    # for Get request to the route, we sent the html form
    return render_template("login.html")


# Create Sign Out Route which we'll create a button for
@auth_views.route("/logout", strict_slashes=False)
@login_required
def logout():
    # We wrap the logout function with @login_required decorator
    # So that only logged in users should be able to 'log out'
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
            user_availability.document(username).delete()
            user.document(username).delete()

            logout_user()
            return redirect("/")

    # When it's a GET request we sent the html form
    return render_template("delete_account.html")

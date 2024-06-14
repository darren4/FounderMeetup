from flask import Blueprint, request, render_template
from flask import redirect

auth_views = Blueprint("auth", __name__)

@auth_views.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    # Define application logic for homepage
    if request.method == "POST":
        uploaded_file = request.files['picture']
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Save the uploaded file to a directory on your server
        # Preferably outside the application root or as you desire
        uploaded_file.save(f"/tmp/{uploaded_file.filename}")

        # Implement database logic to register user

        return render_template("login.html")

    # Render template for GET requests
    return render_template("register.html")


@auth_views.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    # Define application logic for profile page
    if request.method == "POST":
        # Enter logic for processing login
        return "<h1>After Login</h1>"

    return "<h1>Here goes the Login Page</h1>"
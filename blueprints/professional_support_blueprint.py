from flask import Blueprint, render_template
from flask_login import login_required


professional_support_views = Blueprint("professional_support", __name__)


@professional_support_views.get("/professionalsupport", strict_slashes=False)
@login_required
def professional_support():
    # Define application logic for profile page
    return render_template("professional_support.html")

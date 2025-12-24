# routes/user_routes.py

from flask import Blueprint, render_template, request, flash
from models.models import Certificate

user_bp = Blueprint("user", __name__)

# ---------------------- VERIFY PAGE ----------------------
@user_bp.route("/verify", methods=["GET", "POST"])
def verify_page():

    # GET request → show empty verification page
    if request.method == "GET":
        return render_template("verify_certificate.html", active="verify")

    # POST request → user entered something
    query = request.form.get("certificate_query")

    if not query:
        flash("Please enter a certificate hash or registration number.", "warning")
        return render_template("verify_certificate.html", active="verify")

    query = query.strip()

    # Search database
    certificate = Certificate.query.filter(
        (Certificate.reg_number == query) |
        (Certificate.certificate_hash == query)
    ).first()

    if not certificate:
        flash("❌ No matching certificate found.", "danger")
        return render_template("verify_certificate.html", active="verify")

    # Found result → show certificate details
    return render_template("result.html", cert=certificate, active="verify")


# ---------------------- ABOUT PAGE ----------------------
@user_bp.route("/about")
def about_page():
    return render_template("about.html", active="about")


# ---------------------- CONTACT PAGE ----------------------
@user_bp.route("/contact")
def contact_page():
    return render_template("contact.html", active="contact")

# routes/admin_auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.admin import Admin

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")

# --------------------- REGISTER ---------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if email exists
        if Admin.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(request.url)

        admin = Admin(username=name, email=email)
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("admin/register.html")


# --------------------- LOGIN ---------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        admin = Admin.query.filter_by(email=email).first()

        if admin and admin.check_password(password):
            session["admin_id"] = admin.id
            session["admin_name"] = admin.username
            flash("Login successful!", "success")
            return redirect(url_for("admin.dashboard"))

        flash("Invalid email or password!", "danger")

    return render_template("admin/login.html")


# --------------------- LOGOUT ---------------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))

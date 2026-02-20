from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.admin import Admin, SuperAdmin

super_admin_bp = Blueprint("super_admin", __name__, url_prefix="/super-admin")

# --------------------- LOGIN ---------------------
@super_admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        super_admin = SuperAdmin.query.filter_by(email=email).first()

        if super_admin and super_admin.check_password(password):
            session["super_admin_id"] = super_admin.id
            session["super_admin_name"] = super_admin.username
            flash("Login successful!", "success")
            return redirect(url_for("super_admin.dashboard"))

        flash("Invalid email or password!", "danger")

    return render_template("super_admin/login.html")

# --------------------- DASHBOARD ---------------------
@super_admin_bp.route("/dashboard")
def dashboard():
    if "super_admin_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("super_admin.login"))

    admins = Admin.query.all()
    total_admins = len(admins)
    
    return render_template("super_admin/dashboard.html", admins=admins, total_admins=total_admins)

# --------------------- ADD ADMIN ---------------------
@super_admin_bp.route("/add-admin", methods=["GET", "POST"])
def add_admin():
    if "super_admin_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("super_admin.login"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        school_name = request.form.get("school_name")

        if Admin.query.filter_by(email=email).first():
            flash("Admin with this email already exists!", "danger")
            return redirect(request.url)

        new_admin = Admin(username=name, email=email, school_name=school_name)
        new_admin.set_password(password)

        db.session.add(new_admin)
        db.session.commit()

        flash(f"Admin for {school_name} added successfully!", "success")
        return redirect(url_for("super_admin.dashboard"))

    return render_template("super_admin/add_admin.html")

# --------------------- LOGOUT ---------------------
@super_admin_bp.route("/logout")
def logout():
    session.pop("super_admin_id", None)
    session.pop("super_admin_name", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("super_admin.login"))

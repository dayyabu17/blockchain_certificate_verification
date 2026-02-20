from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from models import db
from models.models import Certificate
from models.admin import Admin
from utils.hash_generator import generate_certificate_hash
from blockchain.blockchain import Blockchain
from datetime import date
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Upload paths
CERT_UPLOAD_FOLDER = "static/uploads/certificates/"
PHOTO_UPLOAD_FOLDER = "static/uploads/photos/"

os.makedirs(CERT_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PHOTO_UPLOAD_FOLDER, exist_ok=True)

ALLOWED_CERT_TYPES = {"pdf", "jpg", "jpeg", "png"}
ALLOWED_PHOTO_TYPES = {"jpg", "jpeg", "png"}

blockchain = Blockchain()

# ------------------------------ HELPERS ------------------------------
def allowed_file(filename, allowed_set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set
from functools import wraps

def login_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please login to continue.", "danger")
            return redirect(url_for("admin.login"))
        return route(*args, **kwargs)
    return wrapper

# ------------------------------ REGISTER ------------------------------
@admin_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing = Admin.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered!", "danger")
            return redirect(request.url)

        admin = Admin(username=username, email=email)
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for("admin.login"))

    return render_template("admin/register.html")

# ------------------------------ LOGIN ------------------------------
@admin_bp.route("/login", methods=["GET", "POST"])
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

# ------------------------------ LOGOUT ------------------------------
@admin_bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))

# ------------------------------ DASHBOARD ------------------------------
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if "school_name" not in session:
        # Try to recover from DB if admin_id exists
        if "admin_id" in session:
            current_admin = Admin.query.get(session["admin_id"])
            if current_admin:
                session["school_name"] = current_admin.school_name
                school_name = current_admin.school_name
            else:
                 return redirect(url_for("auth.logout"))
        else:
            return redirect(url_for("auth.logout"))
    else:
        school_name = session["school_name"]
    certificates = Certificate.query.filter_by(institution=school_name).all()
    return render_template("admin/dashboard.html", certificates=certificates)

# ------------------------------ UPLOAD CERTIFICATE ------------------------------
@admin_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_certificate():
    if request.method == "POST":

        # Collect student data
        issue_date = date.today()
        student_data = {
            "student_name": request.form.get("student_name"),
            "reg_number": request.form.get("reg_number"),
            "department": request.form.get("department"),
            "faculty": request.form.get("faculty"),
            "program": request.form.get("program"),
            "institution": session.get("school_name", "Bayero University Kano"), # Force institution from session
            "level": request.form.get("level"),
            "grad_year": request.form.get("grad_year"),
            "issue_date": issue_date  
        }

        # Check for duplicate reg_number in the same institution
        existing_cert = Certificate.query.filter_by(reg_number=student_data["reg_number"], institution=student_data["institution"]).first()
        if existing_cert:
            flash("A result with the same reg number has been uploaded", "danger")
            return redirect(request.url)


        # Required fields check
        if any(v is None or str(v).strip() == "" for v in student_data.values()):
            flash("All fields are required!", "danger")
            return redirect(request.url)


        cert_file = request.files.get("certificate_file")
        passport = request.files.get("passport_photo")

        # Validate certificate
        if not cert_file or not allowed_file(cert_file.filename, ALLOWED_CERT_TYPES):
            flash("Invalid certificate file!", "danger")
            return redirect(request.url)

        # Validate passport
        if not passport or not allowed_file(passport.filename, ALLOWED_PHOTO_TYPES):
            flash("Invalid passport photo!", "danger")
            return redirect(request.url)

        # Save certificate
        cert_filename = secure_filename(cert_file.filename)
        cert_path = os.path.join(CERT_UPLOAD_FOLDER, cert_filename)
        cert_file.save(cert_path)

        # Save passport
        passport_filename = secure_filename(passport.filename)
        passport_path = os.path.join(PHOTO_UPLOAD_FOLDER, passport_filename)
        passport.save(passport_path)

        # Generate hash
        certificate_hash = generate_certificate_hash(cert_path, passport_path, student_data)

        # Add to blockchain
        previous_hash = blockchain.get_last_hash()
        block_index = blockchain.add_block({**student_data, "certificate_hash": certificate_hash, "issue_date": issue_date.isoformat()})

        # Save in DB
        new_cert = Certificate(
            **student_data,
            certificate_file=cert_path,
            passport_photo=passport_path,
            certificate_hash=certificate_hash,
            previous_hash=previous_hash,
            blockchain_index=block_index
        )

        db.session.add(new_cert)
        db.session.commit()

        return redirect(url_for("admin.success", cert_id=new_cert.id))

    return render_template("admin/upload_certificate.html")

# ------------------------------ SUCCESS PAGE ------------------------------
@admin_bp.route("/success/<int:cert_id>")
@login_required
def success(cert_id):
    cert = Certificate.query.get_or_404(cert_id)
    return render_template("admin/upload_success.html", cert=cert)

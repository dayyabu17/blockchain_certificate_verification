from app import app, db
from models.admin import Admin


def seed_admin():
    with app.app_context():
        # Update these defaults as needed
        email = "admin@school.com"

        existing = Admin.query.filter_by(email=email).first()
        if existing:
            print("Admin already exists.")
            return

        admin = Admin(
            username="SchoolAdmin",
            email=email,
            school_name="My School"
        )
        admin.set_password("password123")

        db.session.add(admin)
        db.session.commit()

        print("Admin created: admin@school.com / password123")


if __name__ == "__main__":
    seed_admin()

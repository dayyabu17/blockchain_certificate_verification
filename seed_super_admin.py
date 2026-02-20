from app import app, db
from models.admin import SuperAdmin

def seed_super_admin():
    with app.app_context():
        # Check if exists
        existing = SuperAdmin.query.filter_by(email="super@admin.com").first()
        if existing:
            print("Super Admin already exists.")
            return

        super_admin = SuperAdmin(username="SuperAdmin", email="super@admin.com")
        super_admin.set_password("password123")
        db.session.add(super_admin)
        db.session.commit()
        print("Super Admin created: super@admin.com / password123")

if __name__ == "__main__":
    seed_super_admin()


from app import app, db

def reset_database():
    print("Resetting database...")
    with app.app_context():
        db.drop_all()
        print("All tables dropped.")
        db.create_all()
        print("All tables recreated.")
    print("Database reset complete.")

if __name__ == "__main__":
    reset_database()

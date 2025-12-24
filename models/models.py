from datetime import datetime
from . import db

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    reg_number = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    faculty = db.Column(db.String(120), nullable=False)
    program = db.Column(db.String(120), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    grad_year = db.Column(db.String(20), nullable=False)
    issue_date = db.Column(db.String(20), nullable=False)

    certificate_file = db.Column(db.String(300), nullable=False)
    passport_photo = db.Column(db.String(300), nullable=False)

    certificate_hash = db.Column(db.String(300), unique=True, nullable=False)
    previous_hash = db.Column(db.String(300))
    blockchain_index = db.Column(db.Integer)

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Certificate {self.student_name} - {self.reg_number}>"

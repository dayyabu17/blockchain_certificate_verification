
import unittest
import os
import sys
# Add parent directory to path to import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.models import Certificate
from models.admin import Admin
from io import BytesIO

class TestDuplicateUpload(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

        # Create Admin
        self.admin = Admin(username="admin", email="admin@test.com", school_name="Test Uni")
        self.admin.set_password("password")
        db.session.add(self.admin)
        db.session.commit()

        # Create Uploads folder if not exists (mocking file save)
        os.makedirs("static/uploads/certificates/", exist_ok=True)
        os.makedirs("static/uploads/photos/", exist_ok=True)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def login(self):
        return self.app.post('/admin/login', data=dict(
            email="admin@test.com",
            password="password"
        ), follow_redirects=True)

    def test_duplicate_upload(self):
        self.login()

        # Data for upload
        data = {
            "student_name": "John Doe",
            "reg_number": "REG123", # Duplicate target
            "department": "CS",
            "faculty": "Science",
            "program": "BSc",
            "level": "400",
            "grad_year": "2023",
            "certificate_file": (BytesIO(b"dummy cert content"), "cert.pdf"),
            "passport_photo": (BytesIO(b"dummy photo content"), "photo.jpg")
        }

        # First Upload
        response = self.app.post('/admin/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
        self.assertIn(b"Certificate Uploaded Successfully", response.data)
        
        # Verify it's in DB
        cert = Certificate.query.filter_by(reg_number="REG123").first()
        self.assertIsNotNone(cert)

        # Second Upload (Same Reg No)
        # Re-create file streams as they are consumed
        data["certificate_file"] = (BytesIO(b"dummy cert content"), "cert.pdf")
        data["passport_photo"] = (BytesIO(b"dummy photo content"), "photo.jpg")
        
        response = self.app.post('/admin/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
        
        # Should fail with specific message
        self.assertIn(b"A result with the same reg number has been uploaded", response.data)
        
        # Verify count is still 1
        count = Certificate.query.filter_by(reg_number="REG123").count()
        self.assertEqual(count, 1)

if __name__ == '__main__':
    unittest.main()

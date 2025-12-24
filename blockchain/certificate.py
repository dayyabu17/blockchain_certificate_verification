# blockchain/certificate.py

class CertificateData:
    """
    Represents the certificate data stored inside each blockchain block.
    This keeps the blockchain structure clean and organized.
    """

    def __init__(
        self,
        student_name,
        reg_number,
        department,
        faculty,
        program,
        level,
        grad_year,
        issue_date,
        certificate_hash
    ):
        self.student_name = student_name
        self.reg_number = reg_number
        self.department = department
        self.faculty = faculty
        self.program = program
        self.level = level
        self.grad_year = grad_year
        self.issue_date = issue_date
        self.certificate_hash = certificate_hash

    def to_dict(self):
        """Return data in dictionary form (for hashing & block storage)."""
        return {
            "student_name": self.student_name,
            "reg_number": self.reg_number,
            "department": self.department,
            "faculty": self.faculty,
            "program": self.program,
            "level": self.level,
            "grad_year": self.grad_year,
            "issue_date": self.issue_date,
            "certificate_hash": self.certificate_hash
        }

    def __repr__(self):
        return f"<CertificateData {self.reg_number} - {self.student_name}>"

import hashlib

def generate_certificate_hash(certificate_path, photo_path, student_data):
    """
    Generates a SHA-256 hash using:
    - certificate file bytes
    - passport photo bytes
    - student details (dictionary)

    This ensures full tamper-proof security.
    """

    sha = hashlib.sha256()

    # --- Include Certificate File in Hash ---
    try:
        with open(certificate_path, "rb") as cert_file:
            for chunk in iter(lambda: cert_file.read(4096), b""):
                sha.update(chunk)
    except Exception as e:
        print(f"Error hashing certificate file: {e}")
        return None

    # --- Include Passport Photo File in Hash ---
    try:
        with open(photo_path, "rb") as photo_file:
            for chunk in iter(lambda: photo_file.read(4096), b""):
                sha.update(chunk)
    except Exception as e:
        print(f"Error hashing passport photo: {e}")
        return None

    # --- Include Student Details in Hash ---
    try:
        for key, value in sorted(student_data.items()):
            sha.update(f"{key}:{value}".encode())
    except Exception as e:
        print(f"Error hashing student data: {e}")
        return None

    return sha.hexdigest()

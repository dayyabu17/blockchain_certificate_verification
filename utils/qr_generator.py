import qrcode
import os

def generate_qr_code(certificate_hash):
    qr = qrcode.make(certificate_hash)

    # Ensure folder exists
    save_path = "static/uploads/certificates/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    qr_path = os.path.join(save_path, f"qr_{certificate_hash}.png")
    
    qr.save(qr_path)
    return qr_path

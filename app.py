from flask import Flask, render_template
from models import db
from routes.admin_routes import admin_bp
from routes.admin_auth import auth_bp
from routes.user_routes import user_bp
import os

app = Flask(__name__)

# -----------------------------
# DATABASE CONFIG
# -----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'instance/blockchain.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

# -----------------------------
# INIT DB
# -----------------------------
db.init_app(app)

# -----------------------------
# REGISTER BLUEPRINTS
# -----------------------------
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

# -----------------------------
# HOME
# -----------------------------
@app.route('/')
def home():
    return render_template("index.html")

# -----------------------------
# CREATE TABLES
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)

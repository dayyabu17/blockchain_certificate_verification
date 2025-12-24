from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Register models
from .models import Certificate   # noqa
from .admin import Admin          # noqa

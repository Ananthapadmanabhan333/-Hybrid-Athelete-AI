
import sys
import os

sys.path.append(os.getcwd())

try:
    from app.core.config import settings
    print(f"DB URI: {settings.SQLALCHEMY_DATABASE_URI}")
except Exception as e:
    print(f"Error loading config: {e}")

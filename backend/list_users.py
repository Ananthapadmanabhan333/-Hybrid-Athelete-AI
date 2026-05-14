import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
users = db.query(User).all()

for u in users:
    print(f"User: {u.id}, email: {u.email}, full_name: {u.full_name}")

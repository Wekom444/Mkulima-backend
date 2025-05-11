# backend/utils/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions for OTP
def get_user_by_phone(db, phone: str):
    from models.user import User as UserModel
    return db.query(UserModel).filter(UserModel.phone == phone).first()

def save_otp(phone: str, otp: str, expiry):
    # Use a DB update here
    from models.user import User as UserModel
    db = next(get_db())
    user = get_user_by_phone(db, phone) or UserModel(phone=phone, name="", password_hash="", role="farmer")
    user.otp = otp
    user.otp_expiry = expiry
    db.add(user)
    db.commit()

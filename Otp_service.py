# backend/services/otp_service.py

import random
from utils.db import get_user_by_phone, save_otp
from datetime import datetime, timedelta

def send_otp(phone: str) -> str:
    code = f"{random.randint(100000,999999)}"
    save_otp(phone, code, datetime.utcnow() + timedelta(minutes=10))
    # integrate SMS API here (Twilio/AfricasTalking)
    return code

def verify_otp(db, phone: str, otp: str):
    user = get_user_by_phone(db, phone)
    if not user or user.otp != otp or user.otp_expiry < datetime.utcnow():
        return None
    user.otp = None
    user.otp_expiry = None
    db.commit()
    return user

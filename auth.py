# backend/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from services.otp_service import send_otp, verify_otp
from utils.db import get_db
from utils.schemas import UserOut
from utils.security import create_access_token

router = APIRouter()

class AuthRequest(BaseModel):
    phone: str

class VerifyRequest(BaseModel):
    phone: str
    otp: str

@router.post("/send-otp")
def route_send_otp(req: AuthRequest):
    code = send_otp(req.phone)
    if not code:
        raise HTTPException(500, "Failed to send OTP")
    return {"status": "otp_sent"}

@router.post("/verify-otp")
def route_verify_otp(
    req: VerifyRequest,
    db: Session = Depends(get_db)
):
    user = verify_otp(db, req.phone, req.otp)
    if not user:
        raise HTTPException(400, "Invalid OTP")

    # Issue JWT
    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.from_orm(user)
    }


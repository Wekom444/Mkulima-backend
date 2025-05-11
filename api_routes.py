# backend/routes/api_routes.py

from fastapi import APIRouter, Depends, HTTPException
from services.api import get_recommendations, process_mpesa_payment
from utils.auth import get_current_user

router = APIRouter()

@router.get("/recommendations")
def recommend(user=Depends(get_current_user)):
    data = get_recommendations(user["id"])
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data


@router.post("/pay")
def pay(payload: dict):
    phone = payload.get("phone")
    amount = payload.get("amount")
    result = process_mpesa_payment(phone, amount)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# backend/routes/premium.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.security import get_current_user
from utils.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class SubscribeRequest(BaseModel):
    plan: str  # "premium_records" or "featured_listing"

@router.post("/subscribe", dependencies=[Depends(get_current_user)])
def subscribe_plan(req: SubscribeRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Determine fee
    if req.plan == "premium_records":
        fee = float(os.getenv("PRO_RECORDS_FEE"))
    elif req.plan == "featured_listing":
        fee = float(os.getenv("PREMIUM_LISTING_FEE"))
    else:
        raise HTTPException(400, "Unknown plan")

    # Create a pseudo-order for the subscription
    # and charge via same billing logic or directly use billing endpoint
    # ...
    return {"status": "pending_payment", "plan": req.plan, "amount": fee}

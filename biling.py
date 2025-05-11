# backend/routes/billing.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from services.mpesa import stk_push, b2c_payout
from services.airtel import airtel_charge
from services.delivery import calculate_delivery_fee
from utils.db import get_db
import os

router = APIRouter()

class ChargeRequest(BaseModel):
    order_id: str
    payment_method: str           # "mpesa" or "airtel"
    phone: str                    # buyer’s phone
    gross_amount: float           # sum of item prices
    origin: str                   # seller location
    destination: str              # buyer address
    weight: float                 # total weight in KG
    sponsor_recommendation: bool = False  # if seller paid for featured placement

@router.post("/charge")
def charge_customer(req: ChargeRequest, db: Session = Depends(get_db)):
    # 1. Validate order & amount
    record = db.execute(
        "SELECT total_amount, farmer_id FROM orders WHERE id=:id",
        {"id": req.order_id}
    ).fetchone()
    if not record or req.gross_amount != record.total_amount:
        raise HTTPException(400, "Order not found or amount mismatch")
    farmer_id = record.farmer_id

    # 2. Compute fees
    commission_rate = float(os.getenv("COMMISSION_RATE", 0.02))
    commission_amt  = round(req.gross_amount * commission_rate, 2)
    delivery_fee    = calculate_delivery_fee(req.origin, req.destination, req.weight)
    sponsor_fee     = 0.0
    if req.sponsor_recommendation:
        sponsor_rate = float(os.getenv("SPONSOR_RATE", 0.01))
        sponsor_fee = round(req.gross_amount * sponsor_rate, 2)

    total_charge = req.gross_amount + delivery_fee + sponsor_fee

    # 3. Charge buyer
    if req.payment_method == "mpesa":
        result = stk_push(req.phone, total_charge, account_ref=req.order_id)
    else:
        result = airtel_charge(req.phone, total_charge, description="AgriMarket Order")
    if result.get("error"):
        raise HTTPException(400, result["error"])

    # 4. Disburse net to farmer
    net_to_farmer = req.gross_amount - commission_amt
    farmer_phone  = db.execute(
        "SELECT phone FROM users WHERE id=:id", {"id": farmer_id}
    ).scalar_one()
    payout = b2c_payout(farmer_phone, net_to_farmer, remarks="Farmer Payout")
    if payout.get("error"):
        # Log payout failure but don't rollback buyer payment
        print("Payout error:", payout["error"])

    # 5. Record transaction
    db.execute("""
        INSERT INTO transactions (
            order_id, method, gross_amount, commission,
            delivery_fee, sponsor_fee, net_amount,
            external_ref, payout_status, payout_details
        ) VALUES (
            :order_id, :method, :gross, :comm,
            :deliv, :spons, :net,
            :ref, :pstat, :pdet
        )
    """, {
        "order_id": req.order_id,
        "method": req.payment_method,
        "gross": req.gross_amount,
        "comm": commission_amt,
        "deliv": delivery_fee,
        "spons": sponsor_fee,
        "net": net_to_farmer,
        "ref": result.get("CheckoutRequestID") or result.get("transactionId"),
        "pstat": payout.get("ResponseCode", "unknown"),
        "pdet": payout
    })
    db.execute(
        "UPDATE orders SET payment_status='completed' WHERE id=:id",
        {"id": req.order_id}
    )
    db.commit()

    return {
        "status": "success",
        "commission": commission_amt,
        "delivery_fee": delivery_fee,
        "sponsor_fee": sponsor_fee,
        "net_to_farmer": net_to_farmer,
        "payout": payout,
        "details": result
    }



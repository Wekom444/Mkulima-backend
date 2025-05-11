# backend/routes/orders.py

from fastapi import APIRouter, Depends
from typing import List
from utils.schemas import OrderCreate, OrderOut
from utils.db import get_db
from models.order import Order as OrderModel, OrderItem as OrderItemModel
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    order = OrderModel(
        user_id=payload.user_id,
        total_amount=payload.total_amount,
        payment_status="pending",
        delivery_status="pending",
        delivery_address=payload.delivery_address
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in payload.items:
        oi = OrderItemModel(order_id=order.id, **item.dict())
        db.add(oi)
    db.commit()

    return order

@router.get("/", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(OrderModel).all()

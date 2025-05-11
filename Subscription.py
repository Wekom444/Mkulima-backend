# backend/routes/subscription.py

from fastapi import APIRouter, Depends
from typing import List
from utils.schemas import SubscriptionCreate, SubscriptionOut
from utils.db import get_db
from models.subscription import SubscriptionBox as SubsModel, SubscriptionItem as ItemModel
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=SubscriptionOut)
def create_subscription(payload: SubscriptionCreate, db: Session = Depends(get_db)):
    box = SubsModel(
        user_id=payload.user_id,
        box_type=payload.box_type,
        frequency=payload.frequency,
        delivery_location=payload.delivery_location,
        status="active"
    )
    db.add(box)
    db.commit()
    db.refresh(box)
    for item in payload.items:
        mi = ItemModel(box_id=box.id, product_id=item.product_id, quantity=item.quantity)
        db.add(mi)
    db.commit()
    return box

@router.get("/", response_model=List[SubscriptionOut])
def list_subscriptions(db: Session = Depends(get_db)):
    return db.query(SubsModel).all()

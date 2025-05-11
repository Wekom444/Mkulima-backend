from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class Order(BaseModel):
    id: Optional[str]
    buyer_id: str
    farmer_id: str
    items: List[OrderItem]
    total_price: float
    status: str  # pending, confirmed, dispatched, delivered
    delivery_address: Optional[str]
    delivery_date: Optional[datetime]
    created_at: datetime = datetime.utcnow()

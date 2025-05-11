from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    quantity: int
    price: float
    unit: str  # e.g. "kg", "bunch", "pieces"
    category: str  # e.g. "root", "fruit", "leafy", etc.
    location: str
    farmer_id: str
    image_url: Optional[str]
    created_at: datetime = datetime.utcnow()

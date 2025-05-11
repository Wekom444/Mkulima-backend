# backend/utils/schemas.py

from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr = None
    password: str
    role: str

class UserOut(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr = None
    role: str

class ProductCreate(BaseModel):
    name: str
    description: str = None
    price: float
    unit: str
    category: str
    location: str

class ProductOut(ProductCreate):
    id: int

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]
    total_amount: float
    delivery_address: str

class OrderOut(OrderCreate):
    id: int
    payment_status: str
    delivery_status: str

class SubscriptionItem(BaseModel):
    product_id: int
    quantity: int

class SubscriptionCreate(BaseModel):
    user_id: int
    box_type: str
    frequency: str
    delivery_location: str
    items: List[SubscriptionItem]

class SubscriptionOut(SubscriptionCreate):
    id: int

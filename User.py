from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str]
    name: str
    email: Optional[EmailStr]
    phone: str
    password: Optional[str]  # hashed
    role: str  # "farmer", "buyer", "logistics", "admin", "government"
    region: Optional[str]
    created_at: datetime = datetime.utcnow()

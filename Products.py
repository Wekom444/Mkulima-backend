# backend/routes/products.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from utils.schemas import ProductCreate, ProductOut
from utils.db import get_db
from models.product import Product as ProductModel
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=ProductOut)
def add_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = ProductModel(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

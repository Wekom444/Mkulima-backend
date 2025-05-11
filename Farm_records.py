from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from utils.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Pydantic Models
class CropPlan(BaseModel):
    crop_name: str
    area_planted: str
    start_date: str
    end_date: str
    notes: str

class CropRecord(BaseModel):
    crop: str
    yield_amount: str
    notes: str

class LivestockRecord(BaseModel):
    type: str
    quantity: int
    production: str

class ExpenseRecord(BaseModel):
    item: str
    amount: float

class IncomeRecord(BaseModel):
    source: str
    amount: float

# In-memory store (replace with DB queries in production)
farm_data = {
    "crop_plans": [],
    "crop_records": [],
    "livestock_records": [],
    "expenses": [],
    "incomes": []
}

@router.post("/crop-plan")
def add_crop_plan(plan: CropPlan, db: Session = Depends(get_db)):
    farm_data["crop_plans"].append(plan.dict())
    return {"status": "success", "message": "Crop plan recorded."}

@router.post("/crop-records")
def add_crop_record(record: CropRecord, db: Session = Depends(get_db)):
    farm_data["crop_records"].append(record.dict())
    return {"status": "success", "message": "Crop record added."}

@router.post("/livestock-records")
def add_livestock_record(record: LivestockRecord, db: Session = Depends(get_db)):
    farm_data["livestock_records"].append(record.dict())
    return {"status": "success", "message": "Livestock record added."}

@router.post("/expenses")
def add_expense(expense: ExpenseRecord, db: Session = Depends(get_db)):
    farm_data["expenses"].append(expense.dict())
    return {"status": "success", "message": "Expense recorded."}

@router.post("/incomes")
def add_income(income: IncomeRecord, db: Session = Depends(get_db)):
    farm_data["incomes"].append(income.dict())
    return {"status": "success", "message": "Income recorded."}

# backend/routes/analytics.py

from fastapi import APIRouter, Query
from typing import Any, List, Dict
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/")
def get_analytics() -> Any:
    # ... existing analytics ...
    return { /* existing payload */ }

@router.get("/forecast")
def get_forecast(region: str = Query(...)) -> Dict[str, List]:
    # Dummy: next 6 months yield forecast
    labels = []
    data = []
    today = datetime.utcnow()
    for i in range(6):
        month = (today + timedelta(days=30*i)).strftime("%b %Y")
        labels.append(month)
        data.append(round(random.uniform(20, 100), 2))
    return {"labels": labels, "data": data}

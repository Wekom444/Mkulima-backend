# backend/routes/analytics.py

from fastapi import APIRouter
from typing import Any

router = APIRouter()

@router.get("/")
def get_analytics() -> Any:
    # placeholder: integrate real analytics here
    return {
        "topProducts": [{"name": "Cassava", "totalSold": 500}],
        "topRegions": [{"name": "Central", "sales": 1200}],
        "seasonalTrends": [{"season": "Mar-May", "product": "Sweet Potatoes"}],
        "industryOpportunities": "High cassava yield suggests potential starch processing.",
        "activeFarmers": 150,
        "totalProductsListed": 2400
    }

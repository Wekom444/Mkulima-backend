# backend/services/delivery.py

import os
from typing import Tuple

def calculate_delivery_fee(origin: str, destination: str, weight: float) -> float:
    """
    Stub: calculate a delivery fee based on origin/destination and weight.
    Replace with real logic (distance matrix, zone pricing, etc.).
    """
    # Example: flat rate per km + per-kg surcharge
    # You might integrate a mapping API (e.g. Mapbox) to get distance
    DISTANCE_KM = 10  # TODO: compute from origin & destination
    BASE_RATE_PER_KM = float(os.getenv("BASE_RATE_PER_KM", 5))
    WEIGHT_SURCHARGE_PER_KG = float(os.getenv("WEIGHT_SURCHARGE_PER_KG", 2))

    return round(DISTANCE_KM * BASE_RATE_PER_KM + weight * WEIGHT_SURCHARGE_PER_KG, 2)

# backend/services/airtel.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

AIRTEL_API_URL     = os.getenv("AIRTEL_API_URL")
AIRTEL_KEY         = os.getenv("AIRTEL_KEY")
AIRTEL_SERVICE_ID  = os.getenv("AIRTEL_SERVICE_ID")

def airtel_charge(phone: str, amount: float, description: str = "AgriMarket Payment") -> dict:
    """
    Initiate an Airtel Money charge for any platform service or order.
    """
    headers = {
        "Authorization": f"Bearer {AIRTEL_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "customer_msisdn": phone,
        "amount": amount,
        "serviceID": AIRTEL_SERVICE_ID,
        "transactionDesc": description
    }
    try:
        r = requests.post(AIRTEL_API_URL, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


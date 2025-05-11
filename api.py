# backend/services/api.py

import requests
import os

MPESA_API_URL = os.getenv("MPESA_API_URL")
MPESA_KEY = os.getenv("MPESA_KEY")
AIRTEL_API_URL = os.getenv("AIRTEL_API_URL")
AIRTEL_KEY = os.getenv("AIRTEL_KEY")


def get_recommendations(user_id):
    # Simulate AI logic internally
    from services.recommendation_engine import recommend_products
    return recommend_products(user_id)


def process_mpesa_payment(phone_number, amount):
    headers = {
        "Authorization": f"Bearer {MPESA_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "phone": phone_number,
        "amount": amount,
        "reference": "AGRI_ORDER"
    }
    try:
        response = requests.post(MPESA_API_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def process_airtel_payment(phone_number, amount):
    headers = {
        "Authorization": f"Bearer {AIRTEL_KEY}"
    }
    payload = {
        "phone": phone_number,
        "amount": amount
    }
    try:
        response = requests.post(AIRTEL_API_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# backend/services/mpesa.py

import os
import requests
from dotenv import load_dotenv
from services.api import get_recommendations  # if still needed

load_dotenv()

# Existing C2B STK Push
MPESA_API_URL       = os.getenv("MPESA_API_URL")
MPESA_KEY           = os.getenv("MPESA_KEY")
# ...

# New B2C Payout
MPESA_B2C_API_URL          = os.getenv("MPESA_B2C_API_URL")
MPESA_INITIATOR_NAME       = os.getenv("MPESA_INITIATOR_NAME")
MPESA_SECURITY_CREDENTIAL  = os.getenv("MPESA_SECURITY_CREDENTIAL")
MPESA_B2C_QUEUE_TIMEOUT_URL= os.getenv("MPESA_B2C_QUEUE_TIMEOUT_URL")
MPESA_B2C_RESULT_URL       = os.getenv("MPESA_B2C_RESULT_URL")

def process_mpesa_payment(phone_number: str, amount: float) -> dict:
    # ... existing STK push code ...
    pass

def b2c_payout(phone_number: str, amount: float, remarks: str = "Farmer Payout") -> dict:
    """
    Disburse net amount to farmer via M-Pesa B2C API.
    """
    headers = {
        "Authorization": f"Bearer {MPESA_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "InitiatorName": MPESA_INITIATOR_NAME,
        "SecurityCredential": MPESA_SECURITY_CREDENTIAL,
        "CommandID": "BusinessPayment",
        "Amount": amount,
        "PartyA": MPESA_SHORTCODE,
        "PartyB": phone_number,
        "Remarks": remarks,
        "QueueTimeOutURL": MPESA_B2C_QUEUE_TIMEOUT_URL,
        "ResultURL": MPESA_B2C_RESULT_URL,
        "Occasion": "AgriMarket Payout"
    }
    try:
        r = requests.post(MPESA_B2C_API_URL, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

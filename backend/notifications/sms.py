# backend/app/notifications/sms.py

import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load env vars from .env file (only needed in dev)
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")  # your Twilio phone

if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_FROM_NUMBER:
    print(" Twilio is not fully configured. SMS sending will fail.")

_twilio_client = None


def get_twilio_client() -> Client:
    global _twilio_client
    if _twilio_client is None:
        _twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    return _twilio_client


def send_fall_alert_sms(to_phone: str, patient_name: str, severity: str, confidence: float):
    """
    Sends a real SMS using Twilio.
    'to_phone' must be in E.164 format, e.g. '+14165551234'
    """
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER):
        print(" Twilio config missing, not sending SMS.")
        return

    severity = severity.upper()
    msg = (
        f"🚨 Fall detected for {patient_name}.\n"
        f"Severity: {severity}, confidence: {confidence:.2f}.\n"
        f"Please check on them immediately."
    )

    client = get_twilio_client()
    message = client.messages.create(
        body=msg,
        from_=TWILIO_FROM_NUMBER,
        to=to_phone,
    )
    print(f" SMS sent to {to_phone}. Twilio SID: {message.sid}")

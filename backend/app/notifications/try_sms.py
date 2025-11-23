from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

sid = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_FROM_NUMBER")

client = Client(sid, token)

message = client.messages.create(
    body="Hello from Ishan's fall detection app! 🚨",
    from_=from_number,
    to="+19055987068"
)

print("Message SID:", message.sid)

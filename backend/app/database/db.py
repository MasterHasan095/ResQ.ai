import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()  # load .env

MONGO_URI = os.environ["MONGO_URI"]
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "fall_detector_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# ---- Collections (match exactly what Compass shows) ----
users_collection = db["users"]
incident_collection = db["incidents"]
contacts_collection = db["contacts"]
devices_collection = db["devices"]
notifications_collection = db["notifications"]

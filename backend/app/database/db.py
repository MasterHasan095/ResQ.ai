from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGO_URI = config("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["fall_detector_db"]  # choose your DB name here

users_collection = db["users"]
falls_collection = db["fall_events"]

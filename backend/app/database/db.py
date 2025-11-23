from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

# Load Mongo connection string from .env or environment
MONGO_URI = config("MONGO_URI")

# Create async Mongo client
client = AsyncIOMotorClient(MONGO_URI)

# Choose your database
db = client["fall_detector_db"]

# Collections
users_collection = db["users"]
falls_collection = db["fall_events"]

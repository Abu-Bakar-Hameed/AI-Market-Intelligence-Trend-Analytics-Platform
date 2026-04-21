# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

raw_collection = db["raw_data"]
processed_collection = db["processed_data"]
users_collection = db["users"]
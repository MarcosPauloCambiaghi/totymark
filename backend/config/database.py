from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "totymark")

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Coleções
users_collection = database.users
messages_collection = database.messages
chats_collection = database.chats 
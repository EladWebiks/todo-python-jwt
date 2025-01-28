import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import Todo
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # MongoDB connection string

async def init_db():
    """
    Initialize the MongoDB connection and Beanie models.
    """
    client = AsyncIOMotorClient(MONGO_DB_URL)
    await init_beanie(database=client.todo_db, document_models=[Todo])

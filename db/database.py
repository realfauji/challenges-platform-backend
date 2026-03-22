from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.settings import settings
import logging


class DatabaseManager():
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None
    
db = DatabaseManager()

async def connect_to_db():
    logging.info("Connecting to MongoDB.")
    db.client = AsyncIOMotorClient(str(settings.MONGODB_URL), minPoolSize=30, maxPoolSize=100)
    db_name = str(settings.DB_NAME)
    db.db = db.client[db_name]
    logging.info("Connected to MongoDB.")

async def close_db_connection():
    logging.info("Closing connection to database")
    if db.client:
        db.client.close()
    await db.db.close()
    logging.info("Connection closed")
    
async def get_database() -> AsyncIOMotorClient:
    return db.db

async def get_connection() -> AsyncIOMotorClient:
    return db.client

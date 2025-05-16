from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI
import asyncio

async def test_connection():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.transcriptions
    users = await db["users"].find().to_list(10)
    print(users)

asyncio.run(test_connection())
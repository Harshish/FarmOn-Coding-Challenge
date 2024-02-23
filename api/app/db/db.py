import os

import dotenv
from motor.motor_asyncio import AsyncIOMotorClient

dotenv.load_dotenv()


async def get_db():
    client = AsyncIOMotorClient(
        os.environ["MONGODB_URL"], uuidRepresentation="standard"
    )
    db = client[os.environ["DATABASE_NAME"]]
    return db


async def yield_db():
    client = AsyncIOMotorClient(
        os.environ["MONGODB_URL"], uuidRepresentation="standard"
    )
    db = client[os.environ["DATABASE_NAME"]]
    yield db



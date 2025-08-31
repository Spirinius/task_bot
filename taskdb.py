import asyncio
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from beanie import Document, Indexed, init_beanie

from const import MONGO_URL

class Tasks(Document):
    user_id : int
    task : Optional[str] = None
    done : bool = False

class addTask(BaseModel):
    user_id : int
    task : str

async def db_init():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client.TaskDB, document_models=[Tasks])
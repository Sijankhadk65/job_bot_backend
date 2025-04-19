from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import models as models


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        from_attributes = True


async def initiate_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    await init_beanie(
        database=client.get_database("job_bot_db_dev"),
        document_models=models.__all__,
    )

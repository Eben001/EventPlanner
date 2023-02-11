from typing import Optional, Any

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings, BaseModel

from models.event import Event
from models.user import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.event_planner,
                          document_models=[User,Event])

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()

        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc
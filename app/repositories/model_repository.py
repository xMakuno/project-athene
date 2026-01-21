from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from app.models.all import Model
from app.data.dummy import AVAILABLE_MODELS

class ModelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Model]:
        query = select(Model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, model_id: UUID) -> Model | None:
        query = select(Model).where(Model.id == model_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, model: Model) -> Model:
        self.session.add(model)
        return model

    async def delete(self, model_id: UUID) -> bool:
        query = delete(Model).where(Model.id == model_id)
        result = await self.session.execute(query)
        return result.rowcount > 0

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.repositories.model_repository import ModelRepository
from app.schemas.model import ModelCreate, ModelResponse
from app.models.all import Model
from app.services.llm_service import LLMService

class ModelService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ModelRepository(session)
        
    async def get_models(self) -> list[ModelResponse]:
        return await self.repo.get_all()

    async def create_model(self, model_data: ModelCreate) -> ModelResponse:
        model = Model(**model_data.model_dump())
        new_model = await self.repo.create(model)
        await self.session.commit()
        await self.session.refresh(new_model)
        return new_model

    async def delete_model(self, model_id: UUID) -> None:
        deleted = await self.repo.delete(model_id)
        if not deleted:
            raise ValueError("Model not found")
        await self.session.commit()

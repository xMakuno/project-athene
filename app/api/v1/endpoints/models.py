from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.services.model_service import ModelService
from app.schemas.model import ModelCreate, ModelResponse

router = APIRouter()

async def get_model_service(db: AsyncSession = Depends(get_db)) -> ModelService:
    return ModelService(db)

@router.get("/", response_model=list[ModelResponse])
async def get_models(service: ModelService = Depends(get_model_service)):
    return await service.get_models()

@router.post("/", response_model=ModelResponse)
async def create_model(model_data: ModelCreate, service: ModelService = Depends(get_model_service)):
    return await service.create_model(model_data)

@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(model_id: UUID, service: ModelService = Depends(get_model_service)):
    try:
        await service.delete_model(model_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

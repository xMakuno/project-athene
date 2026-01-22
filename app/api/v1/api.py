from fastapi import APIRouter
from app.api.v1.endpoints import chat, models, auth, summary
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(summary.router, prefix="/summary", tags=["summary"])
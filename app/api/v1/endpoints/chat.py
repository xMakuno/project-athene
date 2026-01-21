from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.services.chat_service import ChatService
from app.schemas.chat import ChatCreate, ChatResponse, ChatCompletionRequest, MessageResponse
import logging

logger = logging.getLogger(__name__)


router = APIRouter()

async def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    return ChatService(db)

@router.get("/", response_model=list[ChatResponse])
async def list_chats(chat_service: ChatService = Depends(get_chat_service)):
    return await chat_service.get_chats()

@router.post("/", response_model=ChatResponse)
async def create_new_chat(chat_data: ChatCreate, chat_service: ChatService = Depends(get_chat_service)):
    return await chat_service.create_chat(chat_data)

@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat_history(chat_id: UUID, chat_service: ChatService = Depends(get_chat_service)):
    chat = await chat_service.get_chat_history(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/completions", response_model=MessageResponse)
async def send_message(request: ChatCompletionRequest, chat_service: ChatService = Depends(get_chat_service)):
    try:
        return await chat_service.send_message(request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

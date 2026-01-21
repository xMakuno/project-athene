from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.models.all import TaskRole

class MessageBase(BaseModel):
    role: TaskRole
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: UUID
    created_at: datetime
    model_used: Optional[str] = None
    
    class Config:
        from_attributes = True

class ChatBase(BaseModel):
    title: str = "New Chat"

class ChatCreate(ChatBase):
    model_id: UUID
    pass

class ChatResponse(ChatBase):
    id: UUID
    # For now we'll assume a single user system or we can omit user_id in response if not needed by UI yet
    user_id: UUID 
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class ChatCompletionRequest(BaseModel):
    chat_id: UUID
    message: str
    model_id: UUID

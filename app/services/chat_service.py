from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.chat_repository import ChatRepository
from app.repositories.model_repository import ModelRepository
from app.services.llm_service import LLMService
from app.schemas.chat import ChatCreate, ChatResponse, ChatCompletionRequest, MessageResponse
from app.models.all import Chat, Message, TaskRole

# Placeholder User ID until auth is reintroduced or logic refined
DEFAULT_USER_ID = UUID('00000000-0000-0000-0000-000000000000') 

class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.chat_repo = ChatRepository(session)
        self.model_repo = ModelRepository(session)
        self.llm_service = LLMService()

    async def create_chat(self, chat_data: ChatCreate) -> ChatResponse:
        # TODO: Check if model exists
        new_chat = Chat(
            title=chat_data.title,
            user_id=DEFAULT_USER_ID
        )
        chat = await self.chat_repo.create_chat(new_chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat

    async def get_chats(self) -> list[ChatResponse]:
        return await self.chat_repo.get_chats_by_user(DEFAULT_USER_ID)

    async def get_chat_history(self, chat_id: UUID) -> ChatResponse | None:
        chat = await self.chat_repo.get_chat_by_id(chat_id)
        return chat

    async def send_message(self, request: ChatCompletionRequest) -> MessageResponse:
        chat = await self.chat_repo.get_chat_by_id(request.chat_id)
        if not chat:
            raise ValueError("Chat not found")

        model = await self.model_repo.get_by_id(request.model_id)
        if not model:
            raise ValueError("Model not found")

        # 1. Save User Message
        user_msg = Message(
            chat_id=chat.id,
            role=TaskRole.USER,
            content=request.message,
            model_used=model.name
        )
        await self.chat_repo.add_message(user_msg)
        await self.session.commit() # Commit to ensure user message is saved before LLM call failure risk

        # 2. Call LLM
        # Construct history for context (basic implementation)
        # For now, just sending the current message or last N messages
        # Ideally we fetch history from chat.messages
        context_messages = [{"role": msg.role.value, "content": msg.content} for msg in chat.messages]
        # Append the new message (it might not be in chat.messages yet if not refreshed, depending on ORM state)
        # Since we committed and access relationships, we might need to refresh chat to get the new message in the list
        # OR just append it manually to the list we pass to LLM
        
        # Let's ensure context includes the new user message
        if not any(m["content"] == request.message and m["role"] == "user" for m in context_messages):
             context_messages.append({"role": "user", "content": request.message})

        llm_response_text = await self.llm_service.generate_response(model, context_messages)

        # 3. Save Assistant Message
        assistant_msg = Message(
            chat_id=chat.id,
            role=TaskRole.ASSISTANT,
            content=llm_response_text,
            model_used=model.name
        )
        await self.chat_repo.add_message(assistant_msg)
        await self.session.commit()
        await self.session.refresh(assistant_msg)
        
        return assistant_msg

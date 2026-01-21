from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.models.all import Chat, Message

class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_chats_by_user(self, user_id: UUID) -> list[Chat]:
        # Using selectinload to eagerly load messages if needed, or we can lazy load
        query = select(Chat).where(Chat.user_id == user_id).order_by(Chat.updated_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_chat_by_id(self, chat_id: UUID) -> Chat | None:
        query = select(Chat).where(Chat.id == chat_id).options(selectinload(Chat.messages))
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create_chat(self, chat: Chat) -> Chat:
        self.session.add(chat)
        # return chat # Service will commit
        return chat

    async def add_message(self, message: Message) -> Message:
        self.session.add(message)
        return message
    
    async def delete_chat(self, chat_id: UUID) -> None:
        query = delete(Chat).where(Chat.id == chat_id)
        await self.session.execute(query)

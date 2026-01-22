from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.all import User
from app.schemas.auth import UserCreate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def create(self, user_create: UserCreate, hashed_password: str) -> User:
        user = User(
            username=user_create.username,
            hashed_password=hashed_password,
            is_active=True
        )
        self.session.add(user)
        return user
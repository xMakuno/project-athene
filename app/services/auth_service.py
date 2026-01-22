from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def register_user(self, user_create: UserCreate) -> UserResponse:
        existing_user = await self.user_repo.get_by_username(user_create.username)
        if existing_user:
            raise ValueError("Username already registered")
        
        hashed_password = get_password_hash(user_create.password)
        new_user = await self.user_repo.create(user_create, hashed_password)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def authenticate_user(self, user_login: UserLogin) -> Token:
        user = await self.user_repo.get_by_username(user_login.username)
        if not user or not verify_password(user_login.password, user.hashed_password):
            raise ValueError("Incorrect username or password")
        
        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")

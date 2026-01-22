from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse

router = APIRouter()

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, service: AuthService = Depends(get_auth_service)):
    try:
        return await service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, service: AuthService = Depends(get_auth_service)):
    try:
        return await service.authenticate_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

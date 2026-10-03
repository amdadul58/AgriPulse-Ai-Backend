from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth import service
from app.auth.schemas import UserCreate, UserLogin, TokenResponse
from app.core.security import create_access_token

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model=TokenResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await service.AuthService.create_user(db, user_data.email, user_data.full_name, user_data.password)
    return TokenResponse(access_token=create_access_token({'sub': user.email}))

@router.post('/login', response_model=TokenResponse)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await service.AuthService.authenticate(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return TokenResponse(access_token=create_access_token({'sub': user.email}))

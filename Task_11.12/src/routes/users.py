from fastapi import APIRouter, Depends


from src.entity.models import User
from src.schemas.user import UserResponse
from src.services.auth import auth_service

from fastapi_limiter.depends import RateLimiter



router = APIRouter(prefix='/users', tags=['user'])


@router.get(path='/me', response_model=UserResponse)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user
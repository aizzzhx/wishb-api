from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserCreate, UserUpdate, UserResponse
from database import get_session
from services.users import create_user, get_user_by_email, get_user_by_id, update_user, delete_user

router = APIRouter()

@router.post("/users/create", response_model=UserResponse)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await create_user(session, user.email, user.name)

@router.get("/users/get/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/edit/{user_id}", response_model=UserResponse)
async def edit_user(user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_session)):
    return await update_user(session, user_id, user.name)

@router.delete("/users/delete/{user_id}")
async def remove_user(user_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

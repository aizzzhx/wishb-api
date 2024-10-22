from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User

# Methods for User
async def create_user(session: AsyncSession, email: str, name: str, description: str) -> User:
    new_user = User(email=email, name=name, description=description)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def get_user_by_email(session: AsyncSession, email: str) -> User:
    result = await session.execute(select(User).filter_by(email=email))
    return result.scalar_one_or_none()

async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).filter_by(id=user_id))
    return result.scalar_one_or_none()


async def update_user(session: AsyncSession, user_id: int, name: str, description: str) -> User:
    user = await get_user_by_id(session, user_id)
    if user:
        user.name = name
        user.description = description
        await session.commit()
        await session.refresh(user)
        return user
    return None

async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False

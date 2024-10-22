import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment variables")

engine = create_async_engine(DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"), echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

sync_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=sync_engine)

Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

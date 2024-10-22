from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine
from models import Base
from routers import auth_routes, book_routes, user_routes  
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


app.mount("/img", StaticFiles(directory="img"), name="img")

app.include_router(auth_routes.router)

# Подключаем другие маршруты
app.include_router(book_routes.router, prefix="/api", tags=["Books"])
app.include_router(user_routes.router, prefix="/api", tags=["Users"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the WishbAPI"}
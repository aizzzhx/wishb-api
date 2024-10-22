from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book, BookCondition
from schemas import BookCreate, BookConditionResponse, BookResponse
from database import get_session, get_async_session
from typing import List
from services.books import (
    add_book, 
    get_books_by_user, 
    update_book, 
    delete_book, 
    mark_book_as_favorite,
    get_all_book_conditions,
    upload_photo
)

router = APIRouter()

@router.post("/books/", response_model=BookResponse)
async def add_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    return await add_book(session, book)

@router.get("/books/{user_id}", response_model=list[BookResponse])
async def list_user_books(user_id: int, session: AsyncSession = Depends(get_session)):
    return await get_books_by_user(session, user_id)

@router.put("/books/{book_id}", response_model=BookResponse)
async def edit_book(book_id: int, book: BookCreate, session: AsyncSession = Depends(get_session)):
    return await update_book(session, book_id, book)

@router.delete("/books/{book_id}")
async def remove_book(book_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_book(session, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

@router.patch("/books/{book_id}/favorite")
async def favorite_book(book_id: int, session: AsyncSession = Depends(get_session)):
    return await mark_book_as_favorite(session, book_id)

@router.post("/upload-photo/")
async def upload_photo_route(file: UploadFile = File(...)):
    return await upload_photo(file)

@router.get("/book-conditions/", response_model=List[BookConditionResponse])
async def get_book_conditions(session: AsyncSession = Depends(get_async_session)):
    conditions = await get_all_book_conditions(session)
    return conditions

import os
import select
import uuid
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book, BookCondition
from database import get_session
from schemas import BookCreate
from fastapi import UploadFile

# Methods for Books
async def add_book(book_data: BookCreate, session: AsyncSession = Depends(get_session)):
    new_book = Book(
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        language=book_data.language,
        condition_id=book_data.condition_id,
        description=book_data.description,
        photo_url=book_data.photo_url,
        user_id=book_data.user_id
    )
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book

async def get_books_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).filter_by(user_id=user_id))
    books = result.scalars().all()
    return books

async def update_book(book_id: int, book_data: BookCreate, session: AsyncSession = Depends(get_session)):
    book = await session.get(Book, book_id)
    if book:
        book.title = book_data.title
        book.author = book_data.author
        book.year = book_data.year
        book.language = book_data.language
        book.condition_id = book_data.condition_id
        book.description = book_data.description
        book.photo_url = book_data.photo_url
        await session.commit()
        await session.refresh(book)
        return book
    return None

async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await session.get(Book, book_id)
    if book:
        await session.delete(book)
        await session.commit()
        return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}

async def mark_book_as_favorite(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await session.get(Book, book_id)
    if book:
        book.is_favorite = True
        await session.commit()
        await session.refresh(book)
        return book
    return None

async def upload_photo(book_id: int, file: UploadFile):
    book_folder = os.path.join("img", "books", str(book_id))
    os.makedirs(book_folder, exist_ok=True)
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    file_location = os.path.join(book_folder, unique_filename)   
    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
    return {"photo_url": f"/img/books/{book_id}/{unique_filename}"}

async def get_all_book_conditions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(BookCondition))
    return result.scalars().all()

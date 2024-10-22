from pydantic import BaseModel
from typing import Optional

# Схема для создания пользователя
class UserCreate(BaseModel):
    email: str
    name: str
    class_name: Optional[str]

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    class_name: Optional[str] = None

    class Config:
        orm_mode = True  
class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    class_name: Optional[str]

    class Config:
        from_attributes = True 

class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int]
    language: str
    condition_id: int
    description: Optional[str]
    photo_url: Optional[str]
    user_id: int

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int]
    language: str
    condition_id: int
    description: Optional[str]
    photo_url: Optional[str]
    is_favorite: bool
    user_id: int

    class Config:
        from_attributes = True

class BookConditionResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

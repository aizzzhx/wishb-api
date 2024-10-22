from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

# Модель состояния книги
class BookCondition(Base):
    __tablename__ = 'book_conditions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<BookCondition(id={self.id}, name={self.name})>"

# Модель книги
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # Название книги
    author = Column(String, nullable=False)  # Автор книги
    year = Column(Integer, nullable=True)  # Год издания
    language = Column(String, nullable=False)  # Язык книги
    condition_id = Column(Integer, ForeignKey('book_conditions.id'))  # Состояние книги
    condition = relationship('BookCondition')  # Связь с состоянием книги
    description = Column(String, nullable=True)  # Описание книги
    photo_url = Column(String, nullable=True)  # Фото книги (ссылка)
    is_favorite = Column(Boolean, default=False)  # Признак "Избранное"
    user_id = Column(Integer, ForeignKey('users.id'))  # Владелец книги
    user = relationship('User', back_populates='books')

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    is_active = Column(Integer, default=1)
    books = relationship('Book', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"

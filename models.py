from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base
import enum
from sqlalchemy import Enum as SQLAlchemyEnum

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
    

class ExchangeStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class ExchangeRequest(Base):
    __tablename__ = "exchange_requests"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    requester_id = Column(Integer, ForeignKey("users.id"))
    offered_book_id = Column(Integer, ForeignKey("books.id"))
    status = Column(SQLAlchemyEnum(ExchangeStatus), default=ExchangeStatus.pending)
    exchange_location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    book = relationship("Book", foreign_keys=[book_id])
    requester = relationship("User", foreign_keys=[requester_id])
    offered_book = relationship("Book", foreign_keys=[offered_book_id])
    comments = relationship("ExchangeMessage", back_populates="exchange_request")

class ExchangeMessage(Base):
    __tablename__ = "exchange_messages"

    id = Column(Integer, primary_key=True, index=True)
    exchange_request_id = Column(Integer, ForeignKey("exchange_requests.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    exchange_request = relationship("ExchangeRequest", back_populates="comments")
    sender = relationship("User")

class ExchangeHistory(Base):
    __tablename__ = "exchange_history"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    previous_owner_id = Column(Integer, ForeignKey("users.id"))
    new_owner_id = Column(Integer, ForeignKey("users.id"))
    exchange_date = Column(DateTime, default=datetime.utcnow)
    comments = Column(Text, nullable=True)

    previous_owner = relationship("User", foreign_keys=[previous_owner_id])
    new_owner = relationship("User", foreign_keys=[new_owner_id])
    book = relationship("Book")
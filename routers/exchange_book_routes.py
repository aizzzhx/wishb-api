from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session

from services.exchangeRequestService import (
    ExchangeRequestService
)

from services.exchangeMessageService import (
    ExchangeMessageService
)

from services.exchangeHistoryService import (
    ExchangeHistoryService
)

router = APIRouter()

@router.post("/exchange/request")
def create_exchange_request(book_id: int, offered_book_id: int, requester_id: int, db: Session = Depends(get_session)):
    return ExchangeRequestService.create_exchange_request1(db, book_id, requester_id, offered_book_id)

@router.get("/exchange/book/{book_id}")
def get_exchange_requests(book_id: int, db: Session = Depends(get_session)):
    return ExchangeRequestService.get_requests_for_book(db, book_id)

@router.post("/exchange/{request_id}/accept")
def accept_exchange_request(request_id: int, location: str, db: Session = Depends(get_session)):
    return ExchangeRequestService.update_exchange_request_status(db, request_id, "accepted", location)

@router.post("/exchange/{request_id}/reject")
def reject_exchange_request(request_id: int, db: Session = Depends(get_session)):
    return ExchangeRequestService.update_exchange_request_status(db, request_id, "rejected")


@router.post("/exchange/{request_id}/message")
def send_message(request_id: int, sender_id: int, message: str, db: Session = Depends(get_session)):
    return ExchangeMessageService.send_message(db, request_id, sender_id, message)

@router.get("/exchange/{request_id}/messages")
def get_messages(request_id: int, db: Session = Depends(get_session)):
    return ExchangeMessageService.get_messages_for_exchange(db, request_id)


@router.get("/history/user/{user_id}")
def get_user_history(user_id: int, db: Session = Depends(get_session)):
    return ExchangeHistoryService.get_user_history(db, user_id)
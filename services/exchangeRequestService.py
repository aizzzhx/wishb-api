from sqlalchemy.orm import Session
from models import ExchangeRequest, ExchangeStatus

class ExchangeRequestService:
    @staticmethod
    def create_exchange_request(db: Session, book_id: int, requester_id: int, offered_book_id: int):
        exchange_request = ExchangeRequest(
            book_id=book_id,
            requester_id=requester_id,
            offered_book_id=offered_book_id
        )
        db.add(exchange_request)
        db.commit()
        db.refresh(exchange_request)
        return exchange_request

    @staticmethod
    def get_requests_for_book(db: Session, book_id: int):
        return db.query(ExchangeRequest).filter(ExchangeRequest.book_id == book_id).all()

    @staticmethod
    def update_exchange_request_status(db: Session, request_id: int, status: ExchangeStatus, location: str = None):
        exchange_request = db.query(ExchangeRequest).filter(ExchangeRequest.id == request_id).first()
        if exchange_request:
            exchange_request.status = status
            if status == ExchangeStatus.accepted and location:
                exchange_request.exchange_location = location
            db.commit()
            db.refresh(exchange_request)
        return exchange_request

from sqlalchemy.orm import Session
from models import ExchangeMessage

class ExchangeMessageService:
    @staticmethod
    def send_message(db: Session, exchange_request_id: int, sender_id: int, message: str):
        new_message = ExchangeMessage(
            exchange_request_id=exchange_request_id,
            sender_id=sender_id,
            message=message
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message

    @staticmethod
    def get_messages_for_exchange(db: Session, exchange_request_id: int):
        return db.query(ExchangeMessage).filter(ExchangeMessage.exchange_request_id == exchange_request_id).all()

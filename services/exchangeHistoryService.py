from sqlalchemy.orm import Session
from models import ExchangeHistory

class ExchangeHistoryService:
    @staticmethod
    def log_exchange(db: Session, book_id: int, previous_owner_id: int, new_owner_id: int, comments: str = None):
        history_entry = ExchangeHistory(
            book_id=book_id,
            previous_owner_id=previous_owner_id,
            new_owner_id=new_owner_id,
            comments=comments
        )
        db.add(history_entry)
        db.commit()
        db.refresh(history_entry)
        return history_entry

    @staticmethod
    def get_user_history(db: Session, user_id: int):
        return db.query(ExchangeHistory).filter(ExchangeHistory.previous_owner_id == user_id).all()

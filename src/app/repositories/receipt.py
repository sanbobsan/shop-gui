from sqlalchemy.orm import Session

from app.models import Receipt

from .base import BaseRepository


class ReceiptRepository(BaseRepository[Receipt]):
    def __init__(self, db: Session) -> None:
        super().__init__(Receipt, db)

from typing import Generic, Type, TypeVar

from sqlalchemy import Sequence, delete, select
from sqlalchemy.orm import Session

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session) -> None:
        self.Model: Type[ModelType] = model
        self.db: Session = db

    def get(self, id: int) -> ModelType | None:
        return self.db.get(self.Model, id)

    def get_all(self, **kwargs) -> Sequence[ModelType]:
        stmt = select(self.Model).filter_by(**kwargs)
        return self.db.scalars(stmt).all()

    def create(self, **kwds) -> ModelType:
        instance = self.Model(**kwds)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        stmt = delete(self.Model).where(self.Model.id == id)
        result = self.db.execute(stmt)
        self.db.flush()
        return result.rowcount > 0

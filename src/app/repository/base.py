from typing import Generic, Type, TypeVar

from sqlalchemy import Sequence, delete, select
from sqlalchemy.orm import Session

from app.database import Base, Category, Employee, JobTitle, Product, SaleItem

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session) -> None:
        self.model: ModelType = model
        self.db: Session = db

    def get(self, id: int) -> ModelType | None:
        return self.db.get(self.model, id)

    def get_all(self, **kwargs) -> Sequence[ModelType]:
        stmt = select(self.model).filter_by(**kwargs)
        return self.db.scalars(stmt).all()

    def create(self, **kwds) -> ModelType:
        instance = self.model(**kwds)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount > 0


class CategoryRepository(BaseRepository[Category]): ...


class SaleItemRepository(BaseRepository[SaleItem]): ...


class EmployeeRepository(BaseRepository[Employee]): ...


class JobTitleRepository(BaseRepository[JobTitle]): ...


class ProductRepository(BaseRepository[Product]): ...

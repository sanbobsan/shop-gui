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
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = self.db.execute(stmt)
        self.db.flush()
        return result.rowcount > 0


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session) -> None:
        super().__init__(Category, db)


class SaleItemRepository(BaseRepository[SaleItem]):
    def __init__(self, db: Session) -> None:
        super().__init__(SaleItem, db)


class EmployeeRepository(BaseRepository[Employee]):
    def __init__(self, db: Session) -> None:
        super().__init__(Employee, db)


class JobTitleRepository(BaseRepository[JobTitle]):
    def __init__(self, db: Session) -> None:
        super().__init__(JobTitle, db)


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session) -> None:
        super().__init__(Product, db)

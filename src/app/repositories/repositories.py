from sqlalchemy.orm import Session

from app.models import Category, Employee, JobTitle, Product, SaleItem

from .base import BaseRepository


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

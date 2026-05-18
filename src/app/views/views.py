from app.database import session_local
from app.models import (
    Category,
    Employee,
    JobTitle,
    Product,
    Receipt,
    SaleItem,
)
from app.schemas import (
    CategorySchema,
    EmployeeSchema,
    JobTitleSchema,
    ProductSchema,
    ReceiptSchema,
    SaleItemSchema,
)

from .base import BaseContainer


class CategoryContainer(BaseContainer[CategorySchema]):
    def __init__(self) -> None:
        super().__init__(CategorySchema, Category, session_local)


class ProductContainer(BaseContainer[ProductSchema]):
    def __init__(self) -> None:
        super().__init__(ProductSchema, Product, session_local)


class EmployeeContainer(BaseContainer[EmployeeSchema]):
    def __init__(self) -> None:
        super().__init__(EmployeeSchema, Employee, session_local)


class JobTitleContainer(BaseContainer[JobTitleSchema]):
    def __init__(self) -> None:
        super().__init__(JobTitleSchema, JobTitle, session_local)


class ReceiptContainer(BaseContainer[ReceiptSchema]):
    def __init__(self) -> None:
        super().__init__(ReceiptSchema, Receipt, session_local)


class SaleItemContainer(BaseContainer[SaleItemSchema]):
    def __init__(self) -> None:
        super().__init__(SaleItemSchema, SaleItem, session_local)

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
        super().__init__(CategorySchema, Category)


class ProductContainer(BaseContainer[ProductSchema]):
    def __init__(self) -> None:
        super().__init__(ProductSchema, Product)


class EmployeeContainer(BaseContainer[EmployeeSchema]):
    def __init__(self) -> None:
        super().__init__(EmployeeSchema, Employee)


class JobTitleContainer(BaseContainer[JobTitleSchema]):
    def __init__(self) -> None:
        super().__init__(JobTitleSchema, JobTitle)


class ReceiptContainer(BaseContainer[ReceiptSchema]):
    def __init__(self) -> None:
        super().__init__(ReceiptSchema, Receipt)


class SaleItemContainer(BaseContainer[SaleItemSchema]):
    def __init__(self) -> None:
        super().__init__(SaleItemSchema, SaleItem)

from datetime import datetime

from pydantic import Field

from .base import BaseSchema


class CategorySchema(BaseSchema):
    name: str = Field(title="Category Name")


class ProductSchema(BaseSchema):
    name: str = Field(title="Product Name")
    price: float = Field(title="Price")
    quantity_at_storage: int = Field(title="Quantity")

    category_id: int = Field(title="Category ID")


class SaleItemSchema(BaseSchema):
    quantity: int = Field(title="Quantity")

    product_id: int = Field(title="Product ID")
    receipt_id: int = Field(title="Receipt ID")


class JobTitleSchema(BaseSchema):
    name: str = Field(title="Name")


class EmployeeSchema(BaseSchema):
    name: str = Field(title="Name")
    surname: str = Field(title="Surname")

    job_title_id: int = Field(title="Job title ID")


class ReceiptSchema(BaseSchema):
    created_at: datetime = Field(title="Created at")

    employee_id: int = Field(title="Employee ID")

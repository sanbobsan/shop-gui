from pydantic import Field

from .base import BaseSchema


class CategorySchema(BaseSchema):
    name: str = Field(title="Category Name")


class ProductSchema(BaseSchema):
    name: str = Field(title="Product Name")
    price: float = Field(title="Price")
    quantity_at_storage: int = Field(title="Quantity")

    category_id: int = Field(title="Category ID")

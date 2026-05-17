from abc import ABC

from pydantic import BaseModel, Field


class BaseSchema(BaseModel, ABC):
    id: int | None = Field(None, title="ID")

    @classmethod
    def get_model_fields(cls, id: bool = False) -> list[str]:
        return [field for field in cls.model_fields if (field != "id" or id)]


class CategorySchema(BaseSchema):
    name: str = Field(title="Category Name")


class ProductSchema(BaseSchema):
    name: str = Field(title="Product Name")
    price: float = Field(title="Price")
    quantity_at_storage: int = Field(title="Quantity")

    category_id: int = Field(title="Category ID")

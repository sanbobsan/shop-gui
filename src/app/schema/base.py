from abc import ABC
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


@dataclass
class FieldDesc:
    name: str
    title: str


@dataclass
class FieldData:
    value: Any
    desc: FieldDesc


class BaseSchema(BaseModel, ABC):
    id: int | None = Field(None, title="ID")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def get_field_desc(cls, include_id: bool = False) -> list[FieldDesc]:
        field_descriptions: list[FieldDesc] = [
            FieldDesc(
                name=name,
                title=info.title or name,
            )
            for name, info in cls.model_fields.items()
            if include_id or name != "id"
        ]
        return field_descriptions

    def get_field_data(self, include_id: bool = False) -> list[FieldData]:
        descs: list[FieldDesc] = self.__class__.get_field_desc(include_id=include_id)
        values: dict[str, Any] = self.model_dump(include={desc.name for desc in descs})
        return [
            FieldData(
                value=values.get(desc.name),
                desc=desc,
            )
            for desc in descs
        ]


class CategorySchema(BaseSchema):
    name: str = Field(title="Category Name")


class ProductSchema(BaseSchema):
    name: str = Field(title="Product Name")
    price: float = Field(title="Price")
    quantity_at_storage: int = Field(title="Quantity")

    category_id: int = Field(title="Category ID")

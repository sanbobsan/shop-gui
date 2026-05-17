from app.models import Category, Product
from app.schemas import CategorySchema, ProductSchema

from .base import BaseContainer


class CategoryContainer(BaseContainer[CategorySchema]):
    def __init__(self) -> None:
        super().__init__(CategorySchema, Category)


class ProductContainer(BaseContainer[ProductSchema]):
    def __init__(self) -> None:
        super().__init__(ProductSchema, Product)

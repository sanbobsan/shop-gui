from app.models import Category
from app.repositories import CategoryRepository

from .base import BaseService


class CategoryService(BaseService[Category, CategoryRepository]):
    def __init__(self, repository: CategoryRepository) -> None:
        self.repo: CategoryRepository = repository

    def create_instance(self, **kwds) -> Category:
        return super().create_instance(**kwds)

    def get_instance(self, id) -> Category | None:
        return super().get_instance(id)

    def delete_instance(self, id) -> bool:
        return super().delete_instance(id)

    def get_all_instances(self) -> list[Category]:
        return super().get_all_instances()

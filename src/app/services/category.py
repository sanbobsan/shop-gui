from app.database import Category
from app.repositories import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repo: CategoryRepository = repository

    def create_category(self, name: str) -> Category:
        return self.repo.create(name=name)

    def get_category(self, id: int) -> Category | None:
        return self.repo.get(id)

    def delete_category(self, id: int) -> bool:
        return self.repo.delete(id)

    def get_all_categories(self) -> list[Category]:
        return self.repo.get_all()

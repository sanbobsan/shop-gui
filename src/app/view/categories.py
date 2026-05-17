import flet as ft

from app.database import Category, session_local
from app.repository import CategoryRepository
from app.service.category import CategoryService


class CategoryCard(ft.Card):
    def __init__(self, category_name: str) -> None:
        super().__init__()

        with session_local() as db:
            repo = CategoryRepository(db)
            service = CategoryService(repo)
            category_obj: Category = service.create_category(category_name)
            db.commit()

            self.id: int = category_obj.id
            self.name: str = category_obj.name

        self.content = ft.Text(self.name)

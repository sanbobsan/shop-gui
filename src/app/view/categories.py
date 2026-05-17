import flet as ft

from app.database import Category, session_local
from app.repository import CategoryRepository
from app.service.category import CategoryService


class CategoryCard(ft.Card):
    def __init__(self, id: int, name: str) -> None:
        super().__init__()

        self.id: int = id
        self.name: str = name

        self.content = ft.Text(self.name)


class CategoryContainer(ft.Container):
    def __init__(self) -> None:
        super().__init__()

        self.button = ft.Button("Add Category", on_click=self.add_category)
        self.text_field = ft.TextField(label="Category Name")
        self.cards = ft.Column()

        self.content = ft.Column(
            [
                self.button,
                self.text_field,
                self.cards,
            ]
        )

    def add_category(self) -> None:
        category_name: str = self.text_field.value
        if not category_name:
            return

        with session_local() as db:  # dependency injection?
            repo = CategoryRepository(db)
            service = CategoryService(repo)
            category: Category = service.create_category(category_name)
            db.commit()

        category_card = CategoryCard(category.id, category.name)
        self.cards.controls.append(category_card)
        self.update()

    def load_categories(self) -> None:
        with session_local() as db:
            repo = CategoryRepository(db)
            service = CategoryService(repo)
            categories: list[Category] = service.get_all_categories()

        for category in categories:
            category_card = CategoryCard(category.id, category.name)
            self.cards.controls.append(category_card)

        self.update()

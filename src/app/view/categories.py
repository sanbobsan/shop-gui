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
        category_card = CategoryCard(category_name)
        self.cards.controls.append(category_card)
        self.update()

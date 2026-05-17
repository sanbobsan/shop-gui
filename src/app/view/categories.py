import flet as ft

from app.database import Category, session_local
from app.repository import CategoryRepository
from app.service.category import CategoryService


class CategoryCard(ft.Card):
    def __init__(self, id: int, name: str, on_delete: callable) -> None:
        super().__init__()

        self.id: int = id
        self.name: str = name
        self.button = ft.Button("delete", on_click=lambda _: on_delete(self.id))

        self.content = ft.Row(
            [
                ft.Row(
                    [ft.Text(self.name)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                self.button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )


class CategoryContainer(ft.Container):
    def __init__(self) -> None:
        super().__init__()

        self.text_field = ft.TextField(label="Category Name")
        self.button = ft.Button("Add Category", on_click=self.add_category)
        self.cards = ft.Column()

        self.content = ft.Column(
            [
                ft.Row([self.text_field, self.button]),
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

        category_card = CategoryCard(category.id, category.name, self.delete_category)
        self.cards.controls.append(category_card)
        self.text_field.value = ""
        self.update()

    def delete_category(self, category_id: int) -> None:
        with session_local() as db:
            repo = CategoryRepository(db)
            service = CategoryService(repo)
            service.delete_category(category_id)
            db.commit()

        self.cards.controls = [
            card for card in self.cards.controls if card.id != category_id
        ]
        self.update()

    def load_categories(self) -> None:
        with session_local() as db:
            repo = CategoryRepository(db)
            service = CategoryService(repo)
            categories: list[Category] = service.get_all_categories()

        for category in categories:
            category_card = CategoryCard(
                category.id, category.name, self.delete_category
            )
            self.cards.controls.append(category_card)

        self.update()

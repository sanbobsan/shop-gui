import flet as ft

from app.database import create_tables
from app.views import CategoryContainer, ProductContainer


def main(page: ft.Page) -> None:
    page.title = "shop-gui"
    create_tables()

    tabs = ft.Tabs(
        expand=True,
        length=2,
        content=ft.Column(
            [
                ft.TabBar(
                    tabs=[
                        ft.Tab("Categories"),
                        ft.Tab("Products"),
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        category_container := CategoryContainer(),
                        product_container := ProductContainer(),
                    ],
                ),
            ],
        ),
    )

    page.add(ft.SafeArea(expand=True, content=tabs))
    category_container.load_instances()
    product_container.load_instances()


ft.run(main)

import flet as ft

from app.view.base import CategoryContainer, ProductContainer


def main(page: ft.Page) -> None:

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
                        CategoryContainer(),
                        ProductContainer(),
                    ],
                ),
            ],
        ),
    )

    page.add(ft.SafeArea(expand=True, content=tabs))


ft.run(main)

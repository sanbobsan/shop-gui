import flet as ft

from app.database import create_tables
from app.views import (
    CategoryContainer,
    EmployeeContainer,
    JobTitleContainer,
    ProductContainer,
    ReceiptContainer,
    SaleItemContainer,
)
from app.views.base import BaseContainer


def main(page: ft.Page) -> None:
    page.title = "shop-gui"
    create_tables()

    containers: list[BaseContainer] = [
        CategoryContainer(),
        EmployeeContainer(),
        JobTitleContainer(),
        ProductContainer(),
        ReceiptContainer(),
        SaleItemContainer(),
    ]

    tabs = ft.Tabs(
        expand=True,
        length=len(containers),
        content=ft.Column(
            [
                ft.TabBar(tabs=[ft.Tab("Tab") for container in containers]),
                ft.TabBarView(expand=True, controls=containers),
            ],
        ),
    )

    page.add(ft.SafeArea(expand=True, content=tabs))
    for container in containers:
        container.load_instances()


ft.run(main)

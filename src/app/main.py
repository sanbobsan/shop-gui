import flet as ft


def main(page: ft.Page) -> None:

    tabs = ft.Tabs(
        expand=True,
        length=2,
        content=ft.Column(
            [
                ft.TabBar(
                    tabs=[
                        ft.Tab("Tab 1"),
                        ft.Tab("Tab 2"),
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(content=ft.Text("Tab 1 content")),
                        ft.Container(content=ft.Text("Tab 2 content")),
                    ],
                ),
            ],
        ),
    )

    page.add(ft.SafeArea(expand=True, content=tabs))


ft.run(main)

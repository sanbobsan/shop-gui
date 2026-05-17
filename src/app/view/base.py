from typing import Callable, Generic, Type, TypeVar

import flet as ft

from app.database import Category, Product, session_local
from app.repository.base import BaseRepository, ModelType
from app.schema.base import BaseSchema, CategorySchema, ProductSchema

BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseSchema)


class BaseCard(ft.Card, Generic[BaseSchemaType]):
    def __init__(self, schema: BaseSchema, on_delete: Callable[[int], None]) -> None:
        super().__init__()

        self.schema: BaseSchema = schema

        assert self.schema.id
        self.button = ft.Button("Delete", on_click=lambda _: on_delete(self.schema.id))
        self.content_row = ft.Row(
            controls=[ft.Text(field.value) for field in self.schema.get_field_data()],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        self.content = ft.Row(
            controls=[
                self.content_row,
                self.button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )


class BaseContainer(ft.Container, Generic[BaseSchemaType]):
    def __init__(self, schema: Type[BaseSchemaType], model: Type[ModelType]) -> None:
        super().__init__()

        self.schema: Type[BaseSchemaType] = schema
        self.model: Type[ModelType] = model
        self.base_card = BaseCard[BaseSchemaType]

        self.text_fields: list[ft.TextField] = [
            ft.TextField(
                label=(field.title),
                data=(field.name),
            )
            for field in schema.get_field_desc()
        ]
        self.button = ft.Button("Add", on_click=self.add_instance)
        self.add_row = ft.Row(self.text_fields + [self.button], wrap=True)
        self.cards = ft.Column()

        self.content = ft.Column(
            [
                self.add_row,
                self.cards,
            ]
        )

    def add_instance(self) -> None:
        schema_dict: dict[str, str] = {
            field.data: field.value for field in self.text_fields
        }
        schema: BaseSchemaType = self.schema.model_validate(schema_dict)

        with session_local() as db:  # dependency injection?
            repo: BaseRepository[ModelType] = BaseRepository(self.model, db)
            # BaseService?
            model: ModelType = repo.create(**schema.model_dump())
            schema.id = model.id
            db.commit()

        card: BaseCard[BaseSchemaType] = self.base_card(
            schema,
            lambda _: print(f"{schema} deleted"),
        )
        self.cards.controls.append(card)

        for field in self.text_fields:
            field.value = ""

        self.update()


class CategoryContainer(BaseContainer[CategorySchema]):
    def __init__(self) -> None:
        super().__init__(CategorySchema, Category)


class ProductContainer(BaseContainer[ProductSchema]):
    def __init__(self) -> None:
        super().__init__(ProductSchema, Product)

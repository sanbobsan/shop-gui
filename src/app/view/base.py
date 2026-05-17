from typing import Generic, Type, TypeVar

import flet as ft

from app.database import Category, Product, session_local
from app.repository.base import BaseRepository, ModelType
from app.schema.base import BaseSchema, CategorySchema, ProductSchema

Schema = TypeVar("Schema", bound=BaseSchema)


class BaseCard(ft.Card, Generic[Schema]):
    def __init__(self, schema: Type[Schema], on_delete: callable, **kwds) -> None:
        super().__init__()

        # maybe use schema to store field values instead of setting them as attributes?
        for key, value in kwds.items():
            setattr(self, key, value)  # maybe use schema prefix?

        self.button = ft.Button("delete", on_click=lambda _: on_delete(self.id))
        self.content_row = ft.Row(
            [ft.Text(getattr(self, field)) for field in schema.get_model_fields()],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        self.content = ft.Row(
            [
                self.content_row,
                self.button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )


class BaseContainer(ft.Container, Generic[Schema]):
    def __init__(self, schema: Type[Schema], model: Type[ModelType]) -> None:
        super().__init__()

        self.schema: Type[Schema] = schema
        self.model: Type[ModelType] = model
        self.base_card = BaseCard[Schema]

        for field in self.schema.get_model_fields():
            setattr(self, f"{field}_field", ft.TextField(label=field.title()))

        self.button = ft.Button("Add", on_click=self.add_instance)
        self.add_row = ft.Row(
            [
                getattr(self, f"{field}_field")
                for field in self.schema.get_model_fields()
            ]
            + [self.button],
            wrap=True
        )
        self.cards = ft.Column()

        self.content = ft.Column(
            [
                self.add_row,
                self.cards,
            ]
        )

    def add_instance(self) -> None:
        schema_dict = {}
        for field in self.schema.get_model_fields():
            schema_dict[field] = getattr(
                self, f"{field}_field", ft.TextField(label=field.title())
            ).value
        schema: Schema = self.schema.model_validate(schema_dict)

        with session_local() as db:  # dependency injection?
            repo: BaseRepository[ModelType] = BaseRepository(
                self.model, db
            )  # BaseService?
            model: ModelType = repo.create(**schema.model_dump())
            schema.id = model.id
            db.commit()

        card: BaseCard[Schema] = self.base_card(
            self.schema,
            lambda _: print(f"{schema.id} deleted"),
            **schema.model_dump(),
        )
        self.cards.controls.append(card)

        for field in self.schema.get_model_fields():
            getattr(self, f"{field}_field").value = ""

        self.update()


class CategoryContainer(BaseContainer[CategorySchema]):
    def __init__(self) -> None:
        super().__init__(CategorySchema, Category)


class ProductContainer(BaseContainer[ProductSchema]):
    def __init__(self) -> None:
        super().__init__(ProductSchema, Product)

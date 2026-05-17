from typing import Callable, Generic, Type, TypeVar

import flet as ft

from app.database import session_local
from app.repositories.base import BaseRepository, ModelType
from app.schemas.base import BaseSchema

BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseSchema)


class BaseCard(ft.Card, Generic[BaseSchemaType]):
    def __init__(self, schema: BaseSchema, on_delete: Callable[[int], None]) -> None:
        super().__init__()

        self.schema: BaseSchemaType = schema

        assert self.schema.id
        self.button = ft.Button("Delete", on_click=lambda _: on_delete(self.schema.id))
        self.content_row = ft.Row(
            controls=[
                ft.Text(field.value)
                for field in self.schema.get_field_data(include_id=True)
            ],
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
    def __init__(
        self,
        BaseSchema: Type[BaseSchemaType],
        Model: Type[ModelType],
    ) -> None:
        super().__init__()

        self.BaseSchema: Type[BaseSchemaType] = BaseSchema
        self.Model: Type[ModelType] = Model
        self.BaseCard = BaseCard[BaseSchemaType]

        self.text_fields: list[ft.TextField] = [
            ft.TextField(
                label=(field.title),
                data=(field.name),
            )
            for field in self.BaseSchema.get_field_desc()
        ]
        self.button = ft.Button("Add", on_click=self.add_instance)
        self.add_row = ft.Row(self.text_fields + [self.button], wrap=True)
        self.cards = ft.Column()

        self.content = ft.Column(
            [
                self.add_row,
                self.cards,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def add_instance(self) -> None:
        schema_dict: dict[str, str] = {
            field.data: field.value for field in self.text_fields
        }
        schema: BaseSchemaType = self.BaseSchema.model_validate(schema_dict)

        with session_local() as db:  # dependency injection?
            repo: BaseRepository[ModelType] = BaseRepository(self.Model, db)
            # BaseService?
            model: ModelType = repo.create(**schema.model_dump())
            schema.id = model.id
            db.commit()

        card: BaseCard[BaseSchemaType] = self.BaseCard(
            schema,
            self.delete_instance,
        )
        self.cards.controls.append(card)

        for field in self.text_fields:
            field.value = ""

        self.update()

    def delete_instance(self, instance_id: int) -> None:
        with session_local() as db:
            repo: BaseRepository[ModelType] = BaseRepository(self.Model, db)
            repo.delete(instance_id)
            db.commit()

        self.cards.controls = [
            card for card in self.cards.controls if card.schema.id != instance_id
        ]
        self.update()

    def load_instances(self) -> None:
        with session_local() as db:
            repo: BaseRepository[ModelType] = BaseRepository(self.Model, db)
            instances: list[ModelType] = repo.get_all()

        for instance in instances:
            schema: BaseSchemaType = self.BaseSchema.model_validate(instance)
            card: BaseCard[BaseSchemaType] = self.BaseCard(schema, self.delete_instance)
            self.cards.controls.append(card)

        self.update()

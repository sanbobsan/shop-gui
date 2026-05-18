from typing import Callable, Generic, Type, TypeVar

import flet as ft

from app.database import session_local
from app.repositories.base import BaseRepository, ModelType
from app.schemas.base import BaseSchema
from app.services.base import BaseService

BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseSchema)


class BaseCard(ft.Card, Generic[BaseSchemaType]):
    def __init__(self, schema: BaseSchema, on_delete: Callable[[int], None]) -> None:
        super().__init__()
        # data
        self.schema: BaseSchemaType = schema
        assert self.schema.id
        # content
        self.content_row: ft.Row = ft.Row(
            controls=[
                ft.Container(
                    ft.Text(field.value, text_align=ft.TextAlign.CENTER),
                    expand=True,
                )
                for field in self.schema.get_field_data(include_id=True)
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
        self.button = ft.Button("Delete", on_click=lambda _: on_delete(self.schema.id))

        self.content = ft.Container(
            ft.Row(
                controls=[
                    self.content_row,
                    self.button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=6,
        )


class BaseContainer(ft.Container, Generic[BaseSchemaType]):
    def __init__(
        self,
        BaseSchema: Type[BaseSchemaType],
        Model: Type[ModelType],
    ) -> None:
        super().__init__()
        # base
        self.BaseSchema: Type[BaseSchemaType] = BaseSchema
        self.Model: Type[ModelType] = Model
        self.BaseCard = BaseCard[BaseSchemaType]
        # data
        self.title: str = self.Model.__name__
        # content
        self.text_fields: list[ft.TextField] = [
            ft.TextField(
                label=(field.title),
                data=(field.name),
                expand=True,
            )
            for field in self.BaseSchema.get_field_desc()
        ]
        self.button = ft.Button("Add", on_click=self.add_instance)
        self.add_row = ft.Container(ft.Row(self.text_fields + [self.button]), padding=5)
        self.cards = ft.Column()

        self.padding = 10
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
            service: BaseService[ModelType, BaseRepository[ModelType]] = BaseService(
                repo
            )
            model: ModelType = service.create_instance(**schema.model_dump())
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
            service: BaseService[ModelType, BaseRepository[ModelType]] = BaseService(
                repo
            )
            service.delete_instance(instance_id)
            db.commit()

        self.cards.controls = [
            card for card in self.cards.controls if card.schema.id != instance_id
        ]
        self.update()

    def load_instances(self) -> None:
        with session_local() as db:
            repo: BaseRepository[ModelType] = BaseRepository(self.Model, db)
            service: BaseService[ModelType, BaseRepository[ModelType]] = BaseService(
                repo
            )
            instances: list[ModelType] = service.get_all_instances()

        for instance in instances:
            schema: BaseSchemaType = self.BaseSchema.model_validate(instance)
            card: BaseCard[BaseSchemaType] = self.BaseCard(schema, self.delete_instance)
            self.cards.controls.append(card)

        self.update()

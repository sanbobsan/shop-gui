from contextlib import contextmanager
from typing import Callable, Generic, Type, TypeVar

import flet as ft
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

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
        session_factory: Callable[..., Session],
    ) -> None:
        super().__init__()
        # base
        self.BaseSchema: Type[BaseSchemaType] = BaseSchema
        self.Model: Type[ModelType] = Model
        self.BaseCard = BaseCard[BaseSchemaType]

        @contextmanager
        def safe_session_factory():
            db: Session = session_factory()
            try:
                yield db
            except SQLAlchemyError as e:
                db.rollback()
                raise e
            else:
                db.commit()
            finally:
                db.close()

        self.get_db: Callable[..., Session] = safe_session_factory
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

    def show_alert(self, error: str) -> None:
        self.dlg = ft.AlertDialog(
            title=ft.Text("Возникла ошибка"),
            content=ft.Text(error),
            alignment=ft.Alignment.CENTER,
            open=True,
        )
        self.page.show_dialog(self.dlg)

    def add_instance(self) -> None:
        schema_dict: dict[str, str] = {
            field.data: field.value for field in self.text_fields
        }
        try:
            schema: BaseSchemaType = self.BaseSchema.model_validate(schema_dict)

            with self.get_db() as db:
                repo: BaseRepository[ModelType] = BaseRepository(self.Model, db)
                service: BaseService[ModelType, BaseRepository[ModelType]] = (
                    BaseService(repo)
                )
                model: ModelType = service.create_instance(**schema.model_dump())
                schema.id = model.id
                db.commit()
        except (SQLAlchemyError, ValidationError) as e:
            self.show_alert(str(e))
            return

        card: BaseCard[BaseSchemaType] = self.BaseCard(
            schema,
            self.delete_instance,
        )
        self.cards.controls.append(card)

        for field in self.text_fields:
            field.value = ""

        self.update()

    def delete_instance(self, instance_id: int) -> None:
        try:
            with self.get_db() as db:
                repo: BaseRepository[ModelType] = BaseRepository(self.Model, db)
                service: BaseService[ModelType, BaseRepository[ModelType]] = (
                    BaseService(repo)
                )
                service.delete_instance(instance_id)
                db.commit()
        except (SQLAlchemyError, ValidationError) as e:
            self.show_alert(str(e))
            return

        self.cards.controls = [
            card for card in self.cards.controls if card.schema.id != instance_id
        ]
        self.update()

    def load_instances(self) -> None:
        try:
            with self.get_db() as db:
                repo: BaseRepository[ModelType] = BaseRepository(self.Model, db)
                service: BaseService[ModelType, BaseRepository[ModelType]] = (
                    BaseService(repo)
                )
                instances: list[ModelType] = service.get_all_instances()
        except (SQLAlchemyError, ValidationError) as e:
            self.show_alert(str(e))
            return

        for instance in instances:
            schema: BaseSchemaType = self.BaseSchema.model_validate(instance)
            card: BaseCard[BaseSchemaType] = self.BaseCard(schema, self.delete_instance)
            self.cards.controls.append(card)

        self.update()

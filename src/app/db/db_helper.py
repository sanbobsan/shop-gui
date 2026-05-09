from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


engine: Engine = create_engine("sqlite:///shop.db")


def create_tables():
    Base.metadata.create_all(engine)

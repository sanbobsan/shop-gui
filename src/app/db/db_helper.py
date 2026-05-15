from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm.session import Session


class Base(DeclarativeBase):
    pass


engine: Engine = create_engine("sqlite:///shop.db")


def create_tables() -> None:
    Base.metadata.create_all(engine)


session_local: sessionmaker[Session] = sessionmaker(bind=engine)

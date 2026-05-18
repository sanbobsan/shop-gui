from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.orm.session import Session


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


engine: Engine = create_engine("sqlite:///shop.db")


def create_tables() -> None:
    Base.metadata.create_all(engine)


session_local: sessionmaker[Session] = sessionmaker(bind=engine, expire_on_commit=False)

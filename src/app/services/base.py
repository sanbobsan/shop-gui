from typing import Generic, TypeVar

from app.repositories.base import BaseRepository, ModelType

BaseRepositoryType = TypeVar("BaseRepositoryType", bound=BaseRepository)


class BaseService(Generic[ModelType, BaseRepositoryType]):
    def __init__(self, repository: BaseRepositoryType) -> None:
        self.repo: BaseRepository = repository

    def create_instance(self, **kwds) -> ModelType:
        return self.repo.create(**kwds)

    def get_instance(self, id: int) -> ModelType | None:
        return self.repo.get(id)

    def delete_instance(self, id: int) -> bool:
        return self.repo.delete(id)

    def get_all_instances(self) -> list[ModelType]:
        return self.repo.get_all()

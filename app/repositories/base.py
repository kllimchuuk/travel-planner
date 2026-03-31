from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDRepository(Generic[ModelType], ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> ModelType | None:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self, skip: int, limit: int) -> list[ModelType]:
        raise NotImplementedError()

    @abstractmethod
    def create(self, **values) -> ModelType:
        raise NotImplementedError()

    @abstractmethod
    def update(self, instance: ModelType, **values) -> ModelType:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, instance: ModelType) -> None:
        raise NotImplementedError()


class CRUDRepositorySQLAlchemy(CRUDRepository[ModelType]):
    def __init__(self, db: Session, model: type[ModelType]) -> None:
        self.db = db
        self.model = model

    def find_by_id(self, id: int) -> ModelType | None:
        return self.db.get(self.model, id)

    def find_all(self, skip: int = 0, limit: int = 10) -> list[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(self.model).count()

    def create(self, **values) -> ModelType:
        instance = self.model(**values)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def update(self, instance: ModelType, **values) -> ModelType:
        for key, value in values.items():
            setattr(instance, key, value)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: ModelType) -> None:
        self.db.delete(instance)
        self.db.flush()

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.project_place import ProjectPlace
from app.repositories.base import CRUDRepository, CRUDRepositorySQLAlchemy


class PlaceRepository(CRUDRepository[ProjectPlace], ABC):
    @abstractmethod
    def find_by_id_and_project(
        self, place_id: int, project_id: int
    ) -> ProjectPlace | None:
        raise NotImplementedError()

    @abstractmethod
    def find_all_by_project(
        self, project_id: int, skip: int, limit: int
    ) -> tuple[list[ProjectPlace], int]:
        raise NotImplementedError()

    @abstractmethod
    def count_by_project(self, project_id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def exists_in_project(self, project_id: int, external_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def any_visited_in_project(self, project_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def all_visited_in_project(self, project_id: int) -> bool:
        raise NotImplementedError()


class PlaceRepositoryImpl(CRUDRepositorySQLAlchemy[ProjectPlace], PlaceRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, ProjectPlace)

    def find_by_id_and_project(
        self, place_id: int, project_id: int
    ) -> ProjectPlace | None:
        return (
            self.db.query(self.model)
            .filter_by(id=place_id, project_id=project_id)
            .first()
        )

    def find_all_by_project(
        self, project_id: int, skip: int, limit: int
    ) -> tuple[list[ProjectPlace], int]:
        query = self.db.query(self.model).filter_by(project_id=project_id)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def count_by_project(self, project_id: int) -> int:
        return self.db.query(self.model).filter_by(project_id=project_id).count()

    def exists_in_project(self, project_id: int, external_id: int) -> bool:
        return (
            self.db.query(self.model)
            .filter_by(project_id=project_id, external_id=external_id)
            .first()
            is not None
        )

    def any_visited_in_project(self, project_id: int) -> bool:
        return (
            self.db.query(self.model)
            .filter_by(project_id=project_id, is_visited=True)
            .first()
            is not None
        )

    def all_visited_in_project(self, project_id: int) -> bool:
        total = self.count_by_project(project_id)
        if total == 0:
            return False
        visited = (
            self.db.query(self.model)
            .filter_by(project_id=project_id, is_visited=True)
            .count()
        )
        return visited == total


def get_place_repository(
    db: Annotated[Session, Depends(get_db)],
) -> PlaceRepository:
    return PlaceRepositoryImpl(db)

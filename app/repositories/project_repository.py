from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.travel_project import TravelProject
from app.repositories.base import CRUDRepository, CRUDRepositorySQLAlchemy


class ProjectRepository(CRUDRepository[TravelProject], ABC):
    @abstractmethod
    def find_all_with_count(
        self, skip: int, limit: int
    ) -> tuple[list[TravelProject], int]:
        raise NotImplementedError()


class ProjectRepositoryImpl(CRUDRepositorySQLAlchemy[TravelProject], ProjectRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db, TravelProject)

    def find_all_with_count(
        self, skip: int, limit: int
    ) -> tuple[list[TravelProject], int]:
        total = self.count()
        items = self.find_all(skip=skip, limit=limit)
        return items, total


def get_project_repository(
    db: Annotated[Session, Depends(get_db)],
) -> ProjectRepository:
    return ProjectRepositoryImpl(db)

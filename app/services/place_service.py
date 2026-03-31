from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.art_institute_client import art_client
from app.core.database import get_db
from app.models.project_place import ProjectPlace
from app.repositories.place_repository import PlaceRepository, get_place_repository
from app.repositories.project_repository import (
    ProjectRepository,
    get_project_repository,
)
from app.schemas.place import PlaceCreate, PlaceListResponse, PlaceResponse, PlaceUpdate

MAX_PLACES_PER_PROJECT = 10


class PlaceService:
    def __init__(
        self,
        db: Session,
        project_repository: ProjectRepository,
        place_repository: PlaceRepository,
    ) -> None:
        self._db = db
        self._project_repository = project_repository
        self._place_repository = place_repository

    def _get_project_or_404(self, project_id: int):
        project = self._project_repository.find_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    def _get_place_or_404(self, project_id: int, place_id: int) -> ProjectPlace:
        place = self._place_repository.find_by_id_and_project(place_id, project_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        return place

    def get_place(self, project_id: int, place_id: int) -> PlaceResponse:
        self._get_project_or_404(project_id)
        return PlaceResponse.model_validate(
            self._get_place_or_404(project_id, place_id)
        )

    def list_places(self, project_id: int, page: int, size: int) -> PlaceListResponse:
        self._get_project_or_404(project_id)
        skip = (page - 1) * size
        items, total = self._place_repository.find_all_by_project(
            project_id, skip, size
        )
        return PlaceListResponse(
            items=[PlaceResponse.model_validate(p) for p in items],
            total=total,
            page=page,
            size=size,
        )

    def add_place(self, project_id: int, data: PlaceCreate) -> PlaceResponse:
        self._get_project_or_404(project_id)

        count = self._place_repository.count_by_project(project_id)
        if count >= MAX_PLACES_PER_PROJECT:
            raise HTTPException(
                status_code=422,
                detail=f"Project already has {MAX_PLACES_PER_PROJECT} places (maximum)",
            )

        if self._place_repository.exists_in_project(project_id, data.external_id):
            raise HTTPException(
                status_code=409,
                detail="Place already exists in this project",
            )

        if not art_client.validate_artwork_exists(data.external_id):
            raise HTTPException(
                status_code=422,
                detail=f"Artwork {data.external_id} not found in Art Institute API",
            )

        place = self._place_repository.create(
            project_id=project_id, external_id=data.external_id
        )
        self._db.commit()
        self._db.refresh(place)
        return PlaceResponse.model_validate(place)

    def update_place(
        self, project_id: int, place_id: int, data: PlaceUpdate
    ) -> PlaceResponse:
        self._get_project_or_404(project_id)
        place = self._get_place_or_404(project_id, place_id)

        updated = self._place_repository.update(
            place, **data.model_dump(exclude_none=True)
        )

        if data.is_visited and self._place_repository.all_visited_in_project(
            project_id
        ):
            project = self._project_repository.find_by_id(project_id)
            self._project_repository.update(project, is_completed=True)

        self._db.commit()
        self._db.refresh(updated)
        return PlaceResponse.model_validate(updated)


def get_place_service(
    db: Annotated[Session, Depends(get_db)],
    project_repository: Annotated[ProjectRepository, Depends(get_project_repository)],
    place_repository: Annotated[PlaceRepository, Depends(get_place_repository)],
) -> PlaceService:
    return PlaceService(
        db=db,
        project_repository=project_repository,
        place_repository=place_repository,
    )

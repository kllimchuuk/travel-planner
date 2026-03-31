from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.art_institute_client import art_client
from app.core.database import get_db
from app.models.travel_project import TravelProject
from app.repositories.place_repository import PlaceRepository, get_place_repository
from app.repositories.project_repository import (
    ProjectRepository,
    get_project_repository,
)
from app.schemas.place import ProjectCreateWithPlaces
from app.schemas.project import (
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)


class ProjectService:
    def __init__(
        self,
        db: Session,
        project_repository: ProjectRepository,
        place_repository: PlaceRepository,
    ) -> None:
        self._db = db
        self._project_repository = project_repository
        self._place_repository = place_repository

    def _get_or_404(self, project_id: int) -> TravelProject:
        project = self._project_repository.find_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    def get_project(self, project_id: int) -> ProjectResponse:
        return ProjectResponse.model_validate(self._get_or_404(project_id))

    def list_projects(self, page: int, size: int) -> ProjectListResponse:
        skip = (page - 1) * size
        items, total = self._project_repository.find_all_with_count(skip, size)
        return ProjectListResponse(
            items=[ProjectResponse.model_validate(p) for p in items],
            total=total,
            page=page,
            size=size,
        )

    def create_project_with_places(
        self, data: ProjectCreateWithPlaces
    ) -> ProjectResponse:
        places = data.places or []
        if len(places) > 10:
            raise HTTPException(
                status_code=422, detail="Cannot add more than 10 places to a project"
            )

        external_ids = [p.external_id for p in places]
        if len(external_ids) != len(set(external_ids)):
            raise HTTPException(status_code=409, detail="Duplicate places in request")

        for place in places:
            if not art_client.validate_artwork_exists(place.external_id):
                raise HTTPException(
                    status_code=422,
                    detail=f"Artwork {place.external_id} not found in Art Institute API",
                )

        project_data = data.model_dump(exclude={"places"})
        project = self._project_repository.create(**project_data)

        for place in places:
            self._place_repository.create(
                project_id=project.id, external_id=place.external_id
            )

        self._db.commit()
        self._db.refresh(project)
        return ProjectResponse.model_validate(project)

    def update_project(self, project_id: int, data: ProjectUpdate) -> ProjectResponse:
        project = self._get_or_404(project_id)
        updated = self._project_repository.update(
            project, **data.model_dump(exclude_none=True)
        )
        self._db.commit()
        self._db.refresh(updated)
        return ProjectResponse.model_validate(updated)

    def delete_project(self, project_id: int) -> None:
        project = self._get_or_404(project_id)
        if self._place_repository.any_visited_in_project(project_id):
            raise HTTPException(
                status_code=400,
                detail="Cannot delete project with visited places",
            )
        self._project_repository.delete(project)
        self._db.commit()


def get_project_service(
    db: Annotated[Session, Depends(get_db)],
    project_repository: Annotated[ProjectRepository, Depends(get_project_repository)],
    place_repository: Annotated[PlaceRepository, Depends(get_place_repository)],
) -> ProjectService:
    return ProjectService(
        db=db,
        project_repository=project_repository,
        place_repository=place_repository,
    )

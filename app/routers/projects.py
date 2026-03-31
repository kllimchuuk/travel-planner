from fastapi import APIRouter, Depends, status

from app.schemas.place import ProjectCreateWithPlaces
from app.schemas.project import ProjectListResponse, ProjectResponse, ProjectUpdate
from app.services.project_service import ProjectService, get_project_service

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["projects"],
)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreateWithPlaces,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return project_service.create_project_with_places(data)


@router.get("/", response_model=ProjectListResponse)
def list_projects(
    page: int = 1,
    size: int = 10,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectListResponse:
    return project_service.list_projects(page, size)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return project_service.get_project(project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return project_service.update_project(project_id, data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service),
) -> None:
    project_service.delete_project(project_id)

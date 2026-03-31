from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user
from app.schemas.place import PlaceCreate, PlaceListResponse, PlaceResponse, PlaceUpdate
from app.services.place_service import PlaceService, get_place_service

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["places"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/{project_id}/places",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_place(
    project_id: int,
    data: PlaceCreate,
    place_service: PlaceService = Depends(get_place_service),
) -> PlaceResponse:
    return place_service.add_place(project_id, data)


@router.get("/{project_id}/places", response_model=PlaceListResponse)
def list_places(
    project_id: int,
    page: int = 1,
    size: int = 10,
    place_service: PlaceService = Depends(get_place_service),
) -> PlaceListResponse:
    return place_service.list_places(project_id, page, size)


@router.get("/{project_id}/places/{place_id}", response_model=PlaceResponse)
def get_place(
    project_id: int,
    place_id: int,
    place_service: PlaceService = Depends(get_place_service),
) -> PlaceResponse:
    return place_service.get_place(project_id, place_id)


@router.patch("/{project_id}/places/{place_id}", response_model=PlaceResponse)
def update_place(
    project_id: int,
    place_id: int,
    data: PlaceUpdate,
    place_service: PlaceService = Depends(get_place_service),
) -> PlaceResponse:
    return place_service.update_place(project_id, place_id, data)

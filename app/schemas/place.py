from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class PlaceCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    external_id: int


class PlaceUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    notes: str | None = None
    is_visited: bool | None = None


class PlaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    external_id: int
    notes: str | None
    is_visited: bool
    created_at: datetime
    updated_at: datetime


class PlaceListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[PlaceResponse]
    total: int
    page: int
    size: int


class ProjectCreateWithPlaces(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    start_date: date | None = None
    places: list[PlaceCreate] | None = None

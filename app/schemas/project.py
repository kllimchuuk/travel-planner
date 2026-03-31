from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    start_date: date | None = None


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None
    start_date: date | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    start_date: date | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ProjectResponse]
    total: int
    page: int
    size: int

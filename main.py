from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import Base, engine
from app.models import project_place, travel_project
from app.routers import places, projects
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Travel Planner API — manage travel projects and places to visit.",
    lifespan=lifespan,
)


app.include_router(projects.router)
app.include_router(places.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

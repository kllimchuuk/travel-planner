from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Travel Planner API"
    DATABASE_URL: str = "sqlite:///./travel_planner.db"
    ART_INSTITUTE_API_URL: str = "https://api.artic.edu/api/v1"
    DEBUG: bool = True
    BASIC_AUTH_USERNAME: str = "admin"
    BASIC_AUTH_PASSWORD: str = "secret"

    class Config:
        env_file = ".env"


settings = Settings()

# settings for the app, loaded from .env
# other files will import this instead of os.environ
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # database stuff
    DATABASE_URL: str

    # jwt auth
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # tmdb config
    TMDB_API_KEY: str
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    TMDB_IMAGE_BASE_URL: str = "https://image.tmdb.org/t/p"

    # cors
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    # app details
    APP_NAME: str = "Kinosoca API"
    API_V1_PREFIX: str = "/api/v1"

    # recommendation engine weights
    TFIDF_WEIGHT: float = 0.4
    SEMANTIC_WEIGHT: float = 0.45
    POPULARITY_WEIGHT: float = 0.15
    SIMILARITY_RESULT_LIMIT: int = 12

    # paging
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
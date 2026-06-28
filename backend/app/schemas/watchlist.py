# watchlist api models
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.movie import MovieCardOut


class WatchlistAddRequest(BaseModel):
    movie_id: int


class WatchlistUpdateRequest(BaseModel):
    status: str  


class WatchlistItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    movie_id: int
    status: str
    added_at: datetime
    movie: MovieCardOut


class WatchlistResponse(BaseModel):
    items: list[WatchlistItemOut]
    total: int
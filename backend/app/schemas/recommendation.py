# schemas for recommendation engine
from pydantic import BaseModel

from app.schemas.movie import MovieCardOut


class RecommendedMovieOut(MovieCardOut):
    # movie card but with a reason why it was recommended
    recommendation_reason: list[str] = []
    similarity_score: float | None = None


class RecommendationResponse(BaseModel):
    source_movie_id: int | None = None
    mood: str | None = None
    items: list[RecommendedMovieOut]


class MoodOut(BaseModel):
    id: int
    name: str


class MoodListResponse(BaseModel):
    moods: list[MoodOut]
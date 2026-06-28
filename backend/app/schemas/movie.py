# movie schemas for the api
from pydantic import BaseModel, ConfigDict


class GenreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class KeywordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class PersonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    profile_path: str | None = None


class CastMemberOut(PersonOut):
    character_name: str | None = None


class CrewMemberOut(PersonOut):
    job: str | None = None


class WatchProviderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    provider_id: int
    name: str
    logo_path: str | None = None
    access_type: str
    provider_url: str | None = None


class MovieCardOut(BaseModel):
    # small version of movie for lists
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    poster_path: str | None = None
    release_year: int | None = None
    vote_average: float
    popularity: float
    genres: list[GenreOut] = [] 


class MovieDetailOut(BaseModel):
    # full movie details
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    original_title: str | None = None
    overview: str | None = None
    release_year: int | None = None
    runtime: int | None = None
    popularity: float
    vote_average: float
    vote_count: int
    poster_path: str | None = None
    backdrop_path: str | None = None
    original_language: str | None = None
    country: str | None = None
    genres: list[GenreOut] = []
    keywords: list[KeywordOut] = []
    cast: list[CastMemberOut] = []
    crew: list[CrewMemberOut] = []
    watch_providers: list[WatchProviderOut] = []


class MovieListResponse(BaseModel):
    items: list[MovieCardOut]
    total: int
    page: int
    page_size: int
    total_pages: int


class SearchFilters(BaseModel):
    # all these are optional filters for search
    query: str | None = None
    genre: str | None = None
    country: str | None = None
    language: str | None = None
    year: int | None = None
    min_rating: float | None = None
    actor: str | None = None
    director: str | None = None
    provider: str | None = None
    page: int = 1
    page_size: int = 20


class SemanticSearchRequest(BaseModel):
    query: str
    limit: int = 12
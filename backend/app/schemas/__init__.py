"""
Re-exports all schema classes for convenient single-line imports
(e.g. `from app.schemas import UserResponse, MovieDetailOut`).
"""
from app.schemas.user import (
    UserBase,
    UserResponse,
    FavoriteGenreStat,
    FavoriteActorStat,
    ProfileStatsResponse,
    ProfileResponse,
)
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    AccessTokenResponse,
)
from app.schemas.movie import (
    GenreOut,
    KeywordOut,
    PersonOut,
    CastMemberOut,
    CrewMemberOut,
    WatchProviderOut,
    MovieCardOut,
    MovieDetailOut,
    MovieListResponse,
    SearchFilters,
    SemanticSearchRequest,
)
from app.schemas.watchlist import (
    WatchlistAddRequest,
    WatchlistUpdateRequest,
    WatchlistItemOut,
    WatchlistResponse,
)
from app.schemas.recommendation import (
    RecommendedMovieOut,
    RecommendationResponse,
    MoodOut,
    MoodListResponse,
)

__all__ = [
    "UserBase",
    "UserResponse",
    "FavoriteGenreStat",
    "FavoriteActorStat",
    "ProfileStatsResponse",
    "ProfileResponse",
    "RegisterRequest",
    "LoginRequest",
    "TokenResponse",
    "RefreshRequest",
    "AccessTokenResponse",
    "GenreOut",
    "KeywordOut",
    "PersonOut",
    "CastMemberOut",
    "CrewMemberOut",
    "WatchProviderOut",
    "MovieCardOut",
    "MovieDetailOut",
    "MovieListResponse",
    "SearchFilters",
    "SemanticSearchRequest",
    "WatchlistAddRequest",
    "WatchlistUpdateRequest",
    "WatchlistItemOut",
    "WatchlistResponse",
    "RecommendedMovieOut",
    "RecommendationResponse",
    "MoodOut",
    "MoodListResponse",
]
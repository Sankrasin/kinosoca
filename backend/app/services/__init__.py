"""
Re-exports service-layer functions for convenient single-line imports
(e.g. `from app.services import register_user, search_movies`).
"""
from app.services.auth_service import (
    register_user,
    authenticate_user,
    refresh_access_token,
)
from app.services.movie_service import (
    get_movie_detail,
    get_trending_movies,
    get_popular_movies,
    get_top_rated_movies,
    get_movie_providers,
)
from app.services.search_service import search_movies
from app.services.watchlist_service import (
    get_watchlist,
    add_to_watchlist,
    update_watchlist_status,
    remove_from_watchlist,
    get_profile_stats,
)
from app.services.provider_service import list_all_providers, get_provider_by_name
from app.services.tmdb_client import tmdb_client, TMDBClient

__all__ = [
    "register_user",
    "authenticate_user",
    "refresh_access_token",
    "get_movie_detail",
    "get_trending_movies",
    "get_popular_movies",
    "get_top_rated_movies",
    "get_movie_providers",
    "search_movies",
    "get_watchlist",
    "add_to_watchlist",
    "update_watchlist_status",
    "remove_from_watchlist",
    "get_profile_stats",
    "list_all_providers",
    "get_provider_by_name",
    "tmdb_client",
    "TMDBClient",
]
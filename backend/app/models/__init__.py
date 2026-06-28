"""
Imports every model so they all register on Base.metadata.
This module must be imported (directly or transitively) before Alembic
autogenerates a migration, and before app startup creates/validates tables.
"""
from app.models.user import User
from app.models.genre import Genre, movie_genres
from app.models.person import Person, movie_cast, movie_crew
from app.models.movie import Movie, Keyword, movie_keywords
from app.models.watch_provider import WatchProvider, MovieWatchProvider, AccessType
from app.models.embedding import MovieEmbedding, SEMANTIC_EMBEDDING_DIM
from app.models.watchlist import Watchlist, WatchlistStatus, Mood, MoodGenreMapping

__all__ = [
    "User",
    "Genre",
    "movie_genres",
    "Person",
    "movie_cast",
    "movie_crew",
    "Movie",
    "Keyword",
    "movie_keywords",
    "WatchProvider",
    "MovieWatchProvider",
    "AccessType",
    "MovieEmbedding",
    "SEMANTIC_EMBEDDING_DIM",
    "Watchlist",
    "WatchlistStatus",
    "Mood",
    "MoodGenreMapping",
]
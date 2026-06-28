"""
Re-exports all router instances so main.py can register them in one place
(e.g. `from app.routers import auth, movies, search, ...`).
"""
from app.routers import auth
from app.routers import movies
from app.routers import search
from app.routers import recommendations
from app.routers import mood
from app.routers import watchlist
from app.routers import profile
from app.routers import providers

__all__ = [
    "auth",
    "movies",
    "search",
    "recommendations",
    "mood",
    "watchlist",
    "profile",
    "providers",
]
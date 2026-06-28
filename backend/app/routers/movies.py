# routes for getting movies (popular, details, etc)
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.movie import MovieDetailOut, MovieListResponse, WatchProviderOut
from app.services.movie_service import (
    get_movie_detail,
    get_trending_movies,
    get_popular_movies,
    get_top_rated_movies,
    get_movie_providers,
)
from app.utils.pagination import pagination_params

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/trending", response_model=MovieListResponse)
def trending(
    pagination: tuple[int, int] = Depends(pagination_params),
    db: Session = Depends(get_db),
):
    # get trending movies with paging
    page, page_size = pagination
    return get_trending_movies(db, page=page, page_size=page_size)


@router.get("/popular", response_model=MovieListResponse)
def popular(
    pagination: tuple[int, int] = Depends(pagination_params),
    db: Session = Depends(get_db),
):
    page, page_size = pagination
    return get_popular_movies(db, page=page, page_size=page_size)


@router.get("/top-rated", response_model=MovieListResponse)
def top_rated(
    pagination: tuple[int, int] = Depends(pagination_params),
    db: Session = Depends(get_db),
):
    page, page_size = pagination
    return get_top_rated_movies(db, page=page, page_size=page_size)


@router.get("/{movie_id}", response_model=MovieDetailOut)
def movie_detail(
    movie_id: int,
    country: str = Query(default="IN", description="country code to show where to watch it"),
    db: Session = Depends(get_db),
):
    return get_movie_detail(db, movie_id, country=country)


@router.get("/{movie_id}/providers", response_model=list[WatchProviderOut])
def movie_providers(
    movie_id: int,
    country: str = Query(default="IN"),
    db: Session = Depends(get_db),
):
    return get_movie_providers(db, movie_id, country=country)
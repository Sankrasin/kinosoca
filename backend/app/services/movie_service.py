# logic for getting movies (details, trending, popular)
# we use our own db so it's fast and doesn't hit tmdb rate limits
import math

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.models.movie import Movie
from app.models.watch_provider import MovieWatchProvider
from app.core.exceptions import NotFoundException
from app.schemas.movie import (
    MovieCardOut,
    MovieDetailOut,
    MovieListResponse,
    WatchProviderOut,
    CastMemberOut,
    CrewMemberOut,
)

DEFAULT_COUNTRY = "IN"
MIN_VOTES_FOR_TOP_RATED = 50


def _movie_query_with_relations(db: Session):
    # helper to fetch movie with all its related data
    return db.query(Movie).options(
        joinedload(Movie.genres),
        joinedload(Movie.keywords),
        joinedload(Movie.cast),
        joinedload(Movie.crew),
        joinedload(Movie.watch_providers).joinedload(MovieWatchProvider.provider),
    )


def get_movie_detail(db: Session, movie_id: int, country: str = DEFAULT_COUNTRY) -> MovieDetailOut:
    movie = _movie_query_with_relations(db).filter(Movie.id == movie_id).first()
    if movie is None:
        raise NotFoundException(f"Movie with id {movie_id} not found")

    # filter providers by country
    providers_for_country = [
        WatchProviderOut(
            provider_id=link.provider_id,
            name=link.provider.name,
            logo_path=link.provider.logo_path,
            access_type=link.access_type.value,
            provider_url=link.provider_url,
        )
        for link in movie.watch_providers
        if link.country_code == country
    ]

    return MovieDetailOut(
        id=movie.id,
        title=movie.title,
        original_title=movie.original_title,
        overview=movie.overview,
        release_year=movie.release_year,
        runtime=movie.runtime,
        popularity=movie.popularity,
        vote_average=movie.vote_average,
        vote_count=movie.vote_count,
        poster_path=movie.poster_path,
        backdrop_path=movie.backdrop_path,
        original_language=movie.original_language,
        country=movie.country,
        genres=movie.genres,
        keywords=movie.keywords,
        cast=[
            CastMemberOut(id=p.id, name=p.name, profile_path=p.profile_path, character_name=None)
            for p in movie.cast
        ],
        crew=[
            CrewMemberOut(id=p.id, name=p.name, profile_path=p.profile_path, job=None)
            for p in movie.crew
        ],
        watch_providers=providers_for_country,
    )


def _paginate(query, page: int, page_size: int) -> tuple[list[Movie], int, int]:
    # helper for pagination
    total = query.count()
    total_pages = max(1, math.ceil(total / page_size))
    page = max(1, min(page, total_pages))
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total, total_pages


def _to_movie_list_response(items: list[Movie], total: int, page: int, page_size: int, total_pages: int) -> MovieListResponse:
    return MovieListResponse(
        items=[MovieCardOut.model_validate(m) for m in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


def get_trending_movies(db: Session, page: int = 1, page_size: int = 20) -> MovieListResponse:
    query = db.query(Movie).options(joinedload(Movie.genres)).order_by(desc(Movie.popularity))
    items, total, total_pages = _paginate(query, page, page_size)
    return _to_movie_list_response(items, total, page, page_size, total_pages)

def get_popular_movies(db: Session, page: int = 1, page_size: int = 20) -> MovieListResponse:
    query = (
        db.query(Movie).options(joinedload(Movie.genres))
        .filter(Movie.vote_count >= MIN_VOTES_FOR_TOP_RATED)
        .order_by(desc(Movie.popularity))
    )
    items, total, total_pages = _paginate(query, page, page_size)
    return _to_movie_list_response(items, total, page, page_size, total_pages)

def get_top_rated_movies(db: Session, page: int = 1, page_size: int = 20) -> MovieListResponse:
    query = (
        db.query(Movie).options(joinedload(Movie.genres))
        .filter(Movie.vote_count >= MIN_VOTES_FOR_TOP_RATED)
        .order_by(desc(Movie.vote_average))
    )
    items, total, total_pages = _paginate(query, page, page_size)
    return _to_movie_list_response(items, total, page, page_size, total_pages)


def get_movie_providers(db: Session, movie_id: int, country: str = DEFAULT_COUNTRY) -> list[WatchProviderOut]:
    movie = db.query(Movie).options(
        joinedload(Movie.watch_providers).joinedload(MovieWatchProvider.provider)
    ).filter(Movie.id == movie_id).first()
    if movie is None:
        raise NotFoundException(f"Movie with id {movie_id} not found")

    return [
        WatchProviderOut(
            provider_id=link.provider_id,
            name=link.provider.name,
            logo_path=link.provider.logo_path,
            access_type=link.access_type.value,
            provider_url=link.provider_url,
        )
        for link in movie.watch_providers
        if link.country_code == country
    ]
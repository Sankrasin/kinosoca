# logic for searching movies with all those filters
import math

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.person import Person, movie_cast, movie_crew
from app.models.watch_provider import MovieWatchProvider, WatchProvider
from app.schemas.movie import SearchFilters, MovieCardOut, MovieListResponse


def search_movies(db: Session, filters: SearchFilters) -> MovieListResponse:
    # start with a basic query to get all movies
    query = db.query(Movie).options(joinedload(Movie.genres)).distinct()

    # add filters one by one if they exist
    if filters.query:
        query = query.filter(
            or_(
                Movie.title.ilike(f"%{filters.query}%"),
                Movie.original_title.ilike(f"%{filters.query}%"),
            )
        )

    if filters.genre:
        query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{filters.genre}%"))

    if filters.country:
        query = query.filter(Movie.country == filters.country.upper())

    if filters.language:
        query = query.filter(Movie.original_language == filters.language.lower())

    if filters.year:
        query = query.filter(Movie.release_year == filters.year)

    if filters.min_rating is not None:
        query = query.filter(Movie.vote_average >= filters.min_rating)

    if filters.actor:
        query = query.join(movie_cast, Movie.id == movie_cast.c.movie_id).join(
            Person, Person.id == movie_cast.c.person_id
        ).filter(Person.name.ilike(f"%{filters.actor}%"))

    if filters.director:
        query = query.join(movie_crew, Movie.id == movie_crew.c.movie_id).join(
            Person, Person.id == movie_crew.c.person_id
        ).filter(
            and_(
                Person.name.ilike(f"%{filters.director}%"),
                movie_crew.c.job == "Director",
            )
        )

    if filters.provider:
        query = query.join(
            MovieWatchProvider, MovieWatchProvider.movie_id == Movie.id
        ).join(
            WatchProvider, WatchProvider.id == MovieWatchProvider.provider_id
        ).filter(WatchProvider.name.ilike(f"%{filters.provider}%"))

    # sort by popular movies first
    query = query.order_by(Movie.popularity.desc())

    # handle pagination
    total = query.count()
    total_pages = max(1, math.ceil(total / filters.page_size))
    page = max(1, min(filters.page, total_pages))
    items = query.offset((page - 1) * filters.page_size).limit(filters.page_size).all()

    return MovieListResponse(
        items=[MovieCardOut.model_validate(m) for m in items],
        total=total,
        page=page,
        page_size=filters.page_size,
        total_pages=total_pages,
    )
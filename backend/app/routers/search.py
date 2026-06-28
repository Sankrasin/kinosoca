# routes for searching movies, both normal filters and semantic search
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieListResponse, SearchFilters, SemanticSearchRequest, MovieCardOut
from app.schemas.recommendation import RecommendedMovieOut
from app.services.search_service import search_movies
from app.ml.semantic_engine import semantic_engine

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=MovieListResponse)
def search(
    query: str | None = Query(default=None),
    genre: str | None = Query(default=None),
    country: str | None = Query(default=None),
    language: str | None = Query(default=None),
    year: int | None = Query(default=None),
    min_rating: float | None = Query(default=None),
    actor: str | None = Query(default=None),
    director: str | None = Query(default=None),
    provider: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    # just put all the query params into a filter object
    filters = SearchFilters(
        query=query,
        genre=genre,
        country=country,
        language=language,
        year=year,
        min_rating=min_rating,
        actor=actor,
        director=director,
        provider=provider,
        page=page,
        page_size=page_size,
    )
    return search_movies(db, filters)


@router.post("/semantic", response_model=list[RecommendedMovieOut])
def semantic_search(payload: SemanticSearchRequest, db: Session = Depends(get_db)):
    # do a semantic search using the ml engine
    results = semantic_engine.search_by_text(db, payload.query, top_n=payload.limit)
    if not results:
        return []

    movie_ids = [movie_id for movie_id, _ in results]
    score_by_id = dict(results)

    # fetch the actual movies from db
    movies = (
        db.query(Movie)
        .options(joinedload(Movie.genres))
        .filter(Movie.id.in_(movie_ids))
        .all()
    )
    movies_by_id = {m.id: m for m in movies}

    output = []
    for movie_id, score in results:
        movie = movies_by_id.get(movie_id)
        if movie is None:
            continue
        output.append(
            RecommendedMovieOut(
                id=movie.id,
                title=movie.title,
                poster_path=movie.poster_path,
                release_year=movie.release_year,
                vote_average=movie.vote_average,
                popularity=movie.popularity,
                genres=movie.genres,
                recommendation_reason=["Matches the meaning of your search"],
                similarity_score=round(score, 4),
            )
        )

    return output
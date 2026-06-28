# this mixes the text matching (tfidf) and meaning matching (semantic) 
# and popularity to get the final movie recommendations
import math

from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.models.movie import Movie
from app.ml.tfidf_engine import tfidf_engine
from app.ml.semantic_engine import semantic_engine
from app.ml.explainer import explain_recommendation
from app.schemas.recommendation import RecommendedMovieOut

POPULARITY_LOG_BASE = 10


def _normalize_popularity(popularity: float, max_popularity: float) -> float:
    # normalize popularity so it doesn't overpower the ml scores
    if max_popularity <= 0:
        return 0.0
    log_pop = math.log(popularity + 1, POPULARITY_LOG_BASE)
    log_max = math.log(max_popularity + 1, POPULARITY_LOG_BASE)
    return log_pop / log_max if log_max > 0 else 0.0


def _movie_with_relations(db: Session, movie_id: int) -> Movie | None:
    return (
        db.query(Movie)
        .options(
            joinedload(Movie.genres),
            joinedload(Movie.keywords),
            joinedload(Movie.cast),
            joinedload(Movie.crew),
        )
        .filter(Movie.id == movie_id)
        .first()
    )


def get_hybrid_recommendations(db: Session, movie_id: int, top_n: int | None = None) -> list[RecommendedMovieOut]:
    top_n = top_n or settings.SIMILARITY_RESULT_LIMIT

    source = _movie_with_relations(db, movie_id)
    if source is None:
        return []

    # get results from both ml engines
    tfidf_results = dict(tfidf_engine.get_similar_movie_ids(movie_id, top_n=top_n * 3))
    semantic_results = dict(semantic_engine.get_similar_by_movie_id(db, movie_id, top_n=top_n * 3))

    candidate_ids = set(tfidf_results.keys()) | set(semantic_results.keys())
    if not candidate_ids:
        return []

    max_popularity = db.query(Movie.popularity).order_by(Movie.popularity.desc()).limit(1).scalar() or 1.0

    candidates = (
        db.query(Movie)
        .options(
            joinedload(Movie.genres),
            joinedload(Movie.keywords),
            joinedload(Movie.cast),
            joinedload(Movie.crew),
        )
        .filter(Movie.id.in_(candidate_ids))
        .all()
    )

    scored: list[tuple[Movie, float, float, float]] = []  # (movie, final_score, tfidf, semantic)
    for candidate in candidates:
        tfidf_score = tfidf_results.get(candidate.id, 0.0)
        semantic_score = semantic_results.get(candidate.id, 0.0)
        popularity_score = _normalize_popularity(candidate.popularity, max_popularity)

        # combine all scores based on config weights
        final_score = (
            settings.TFIDF_WEIGHT * tfidf_score
            + settings.SEMANTIC_WEIGHT * semantic_score
            + settings.POPULARITY_WEIGHT * popularity_score
        )
        scored.append((candidate, final_score, tfidf_score, semantic_score))

    # sort by highest score
    scored.sort(key=lambda item: item[1], reverse=True)
    top_results = scored[:top_n]

    output: list[RecommendedMovieOut] = []
    for candidate, final_score, tfidf_score, semantic_score in top_results:
        # add human readable reason
        reasons = explain_recommendation(source, candidate, tfidf_score, semantic_score)
        output.append(
            RecommendedMovieOut(
                id=candidate.id,
                title=candidate.title,
                poster_path=candidate.poster_path,
                release_year=candidate.release_year,
                vote_average=candidate.vote_average,
                popularity=candidate.popularity,
                genres=candidate.genres,
                recommendation_reason=reasons,
                similarity_score=round(final_score, 4),
            )
        )

    return output
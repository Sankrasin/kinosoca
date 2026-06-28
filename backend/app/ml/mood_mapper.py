# logic for mapping moods like 'happy' to genres and finding movies
import math

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.watchlist import Mood, MoodGenreMapping
from app.ml.explainer import explain_mood_match
from app.schemas.recommendation import RecommendedMovieOut

POPULARITY_LOG_BASE = 10


def _normalize_popularity(popularity: float, max_popularity: float) -> float:
    # keeps popularity score in a 0 to 1 range
    if max_popularity <= 0:
        return 0.0
    log_pop = math.log(popularity + 1, POPULARITY_LOG_BASE)
    log_max = math.log(max_popularity + 1, POPULARITY_LOG_BASE)
    return log_pop / log_max if log_max > 0 else 0.0


def get_all_moods(db: Session) -> list[Mood]:
    return db.query(Mood).order_by(Mood.name.asc()).all()


def get_movies_for_mood(db: Session, mood_name: str, top_n: int = 20) -> list[RecommendedMovieOut]:
    mood = db.query(Mood).filter(Mood.name.ilike(mood_name)).first()
    if mood is None:
        return []

    # get the genres that match this mood
    mappings = (
        db.query(MoodGenreMapping)
        .options(joinedload(MoodGenreMapping.genre))
        .filter(MoodGenreMapping.mood_id == mood.id)
        .all()
    )
    if not mappings:
        return []

    genre_weights = {m.genre_id: m.weight for m in mappings}
    genre_ids = list(genre_weights.keys())

    # find movies with these genres
    candidates = (
        db.query(Movie)
        .options(joinedload(Movie.genres))
        .join(Movie.genres)
        .filter(Genre.id.in_(genre_ids))
        .distinct()
        .all()
    )
    if not candidates:
        return []

    max_popularity = db.query(func.max(Movie.popularity)).scalar() or 1.0

    scored: list[tuple[Movie, float, list[str]]] = []
    for movie in candidates:
        matched_genres = [g for g in movie.genres if g.id in genre_weights]
        if not matched_genres:
            continue

        # calculate how well it matches the mood based on genre weights
        genre_score = sum(genre_weights[g.id] for g in matched_genres) / sum(genre_weights.values())
        popularity_score = _normalize_popularity(movie.popularity, max_popularity)

        final_score = (0.7 * genre_score) + (0.3 * popularity_score)
        matched_names = [g.name for g in matched_genres]
        scored.append((movie, final_score, matched_names))

    # sort by highest score
    scored.sort(key=lambda item: item[1], reverse=True)
    top_results = scored[:top_n]

    output: list[RecommendedMovieOut] = []
    for movie, score, matched_names in top_results:
        output.append(
            RecommendedMovieOut(
                id=movie.id,
                title=movie.title,
                poster_path=movie.poster_path,
                release_year=movie.release_year,
                vote_average=movie.vote_average,
                popularity=movie.popularity,
                genres=movie.genres,
                recommendation_reason=explain_mood_match(mood.name, matched_names),
                similarity_score=round(score, 4),
            )
        )

    return output
# logic for saving movies to watchlist and calculating user stats
import uuid
from collections import Counter

from sqlalchemy.orm import Session, joinedload

from app.models.watchlist import Watchlist, WatchlistStatus
from app.models.movie import Movie
from app.core.exceptions import NotFoundException, ConflictException, BadRequestException
from app.schemas.watchlist import WatchlistItemOut, WatchlistResponse
from app.schemas.user import ProfileStatsResponse, FavoriteGenreStat, FavoriteActorStat


def get_watchlist(db: Session, user_id: uuid.UUID) -> WatchlistResponse:
    entries = (
        db.query(Watchlist)
        .options(joinedload(Watchlist.movie).joinedload(Movie.genres))
        .filter(Watchlist.user_id == user_id)
        .order_by(Watchlist.added_at.desc())
        .all()
    )
    return WatchlistResponse(
        items=[WatchlistItemOut.model_validate(e) for e in entries],
        total=len(entries),
    )


def add_to_watchlist(db: Session, user_id: uuid.UUID, movie_id: int) -> WatchlistItemOut:
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise NotFoundException(f"Movie with id {movie_id} not found")

    existing = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id, Watchlist.movie_id == movie_id)
        .first()
    )
    if existing:
        raise ConflictException("Movie is already in your watchlist")

    entry = Watchlist(user_id=user_id, movie_id=movie_id, status=WatchlistStatus.saved)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return WatchlistItemOut.model_validate(entry)


def update_watchlist_status(db: Session, user_id: uuid.UUID, movie_id: int, status: str) -> WatchlistItemOut:
    if status not in (WatchlistStatus.saved.value, WatchlistStatus.watched.value):
        raise BadRequestException("status must be 'saved' or 'watched'")

    entry = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id, Watchlist.movie_id == movie_id)
        .first()
    )
    if entry is None:
        raise NotFoundException("Watchlist entry not found")

    entry.status = WatchlistStatus(status)
    db.commit()
    db.refresh(entry)

    return WatchlistItemOut.model_validate(entry)


def remove_from_watchlist(db: Session, user_id: uuid.UUID, movie_id: int) -> None:
    entry = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id, Watchlist.movie_id == movie_id)
        .first()
    )
    if entry is None:
        raise NotFoundException("Watchlist entry not found")

    db.delete(entry)
    db.commit()


def get_profile_stats(db: Session, user_id: uuid.UUID) -> ProfileStatsResponse:
    # get all watchlist entries to calculate stats
    entries = (
        db.query(Watchlist)
        .options(joinedload(Watchlist.movie).joinedload(Movie.genres))
        .filter(Watchlist.user_id == user_id)
        .all()
    )

    total_saved = sum(1 for e in entries if e.status == WatchlistStatus.saved)
    total_watched = sum(1 for e in entries if e.status == WatchlistStatus.watched)

    # find top 5 genres
    genre_counter: Counter = Counter()
    genre_names: dict[int, str] = {}
    for entry in entries:
        for genre in entry.movie.genres:
            genre_counter[genre.id] += 1
            genre_names[genre.id] = genre.name

    # find top 5 actors
    actor_counter: Counter = Counter()
    actor_names: dict[int, str] = {}
    for entry in entries:
        for person in entry.movie.cast:
            actor_counter[person.id] += 1
            actor_names[person.id] = person.name

    favorite_genres = [
        FavoriteGenreStat(genre_id=gid, genre_name=genre_names[gid], count=count)
        for gid, count in genre_counter.most_common(5)
    ]
    favorite_actors = [
        FavoriteActorStat(person_id=pid, person_name=actor_names[pid], count=count)
        for pid, count in actor_counter.most_common(5)
    ]

    return ProfileStatsResponse(
        total_saved=total_saved,
        total_watched=total_watched,
        favorite_genres=favorite_genres,
        favorite_actors=favorite_actors,
    )
# routes for watchlist things (adding, removing, marking as watched)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.watchlist import (
    WatchlistAddRequest,
    WatchlistUpdateRequest,
    WatchlistItemOut,
    WatchlistResponse,
)
from app.services.watchlist_service import (
    get_watchlist,
    add_to_watchlist,
    update_watchlist_status,
    remove_from_watchlist,
)

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


@router.get("", response_model=WatchlistResponse)
def list_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_watchlist(db, current_user.id)


@router.post("", response_model=WatchlistItemOut, status_code=201)
def add_movie(
    payload: WatchlistAddRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # adds movie to watchlist as 'saved' by default
    return add_to_watchlist(db, current_user.id, payload.movie_id)


@router.patch("/{movie_id}", response_model=WatchlistItemOut)
def update_status(
    movie_id: int,
    payload: WatchlistUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # use this to change status to watched
    return update_watchlist_status(db, current_user.id, movie_id, payload.status)


@router.delete("/{movie_id}", status_code=204)
def remove_movie(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    remove_from_watchlist(db, current_user.id, movie_id)
    return None
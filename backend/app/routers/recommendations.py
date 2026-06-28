# routes for getting recommendations like similar movies and personalized ones
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.recommendation import RecommendationResponse, RecommendedMovieOut
from app.ml.hybrid_engine import get_hybrid_recommendations
from app.services.watchlist_service import get_watchlist

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/similar/{movie_id}", response_model=RecommendationResponse)
def similar_movies(
    movie_id: int,
    limit: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    # get similar movies for a specific movie
    items = get_hybrid_recommendations(db, movie_id, top_n=limit)
    return RecommendationResponse(source_movie_id=movie_id, items=items)


@router.get("/personalized", response_model=RecommendationResponse)
def personalized_recommendations(
    limit: int = Query(default=12, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # look at user's watchlist and recommend based on that
    watchlist = get_watchlist(db, current_user.id)
    if not watchlist.items:
        return RecommendationResponse(items=[])

    seen_movie_ids = {entry.movie_id for entry in watchlist.items}
    aggregated: dict[int, RecommendedMovieOut] = {}

    # just checking up to 10 movies from watchlist so it doesn't get too slow
    for entry in watchlist.items[:10]:
        candidates = get_hybrid_recommendations(db, entry.movie_id, top_n=limit)
        for candidate in candidates:
            # skip if they already watched/saved it
            if candidate.id in seen_movie_ids:
                continue
            existing = aggregated.get(candidate.id)
            if existing is None or (candidate.similarity_score or 0) > (existing.similarity_score or 0):
                aggregated[candidate.id] = candidate

    ranked = sorted(aggregated.values(), key=lambda m: m.similarity_score or 0, reverse=True)[:limit]
    return RecommendationResponse(items=ranked)
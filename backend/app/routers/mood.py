# routes for getting movies by mood
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.recommendation import RecommendationResponse, MoodListResponse, MoodOut
from app.ml.mood_mapper import get_all_moods, get_movies_for_mood

router = APIRouter(prefix="/moods", tags=["Moods"])


@router.get("", response_model=MoodListResponse)
def list_moods(db: Session = Depends(get_db)):
    # get list of all moods
    moods = get_all_moods(db)
    return MoodListResponse(moods=[MoodOut(id=m.id, name=m.name) for m in moods])


@router.get("/{mood_name}/movies", response_model=RecommendationResponse)
def movies_for_mood(
    mood_name: str,
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    # get movies that fit this mood
    items = get_movies_for_mood(db, mood_name, top_n=limit)
    return RecommendationResponse(mood=mood_name, items=items)
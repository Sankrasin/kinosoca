# route for user profile and stats
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import ProfileResponse, UserResponse
from app.services.watchlist_service import get_profile_stats

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # calculate stats like favorite actors based on watchlist
    stats = get_profile_stats(db, current_user.id)
    return ProfileResponse(user=UserResponse.model_validate(current_user), stats=stats)
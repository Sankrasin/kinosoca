# schemas for user profiles and stats
# login stuff is in auth.py
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


class UserBase(BaseModel):
    email: EmailStr
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        if not v.replace("_", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class FavoriteGenreStat(BaseModel):
    genre_id: int
    genre_name: str
    count: int


class FavoriteActorStat(BaseModel):
    person_id: int
    person_name: str
    count: int


class ProfileStatsResponse(BaseModel):
    total_saved: int
    total_watched: int
    favorite_genres: list[FavoriteGenreStat]
    favorite_actors: list[FavoriteActorStat]


class ProfileResponse(BaseModel):
    user: UserResponse
    stats: ProfileStatsResponse
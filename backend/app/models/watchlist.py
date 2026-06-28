# watchlist table for users saving movies
# also putting the mood stuff here so we don't have to make a new file
import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Enum, Integer, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.movie import Movie
    from app.models.genre import Genre


class WatchlistStatus(str, enum.Enum):
    saved = "saved"
    watched = "watched"


class Watchlist(Base):
    __tablename__ = "watchlist"
    __table_args__ = (UniqueConstraint("user_id", "movie_id", name="uq_user_movie"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    movie_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[WatchlistStatus] = mapped_column(
        Enum(WatchlistStatus, name="watchlist_status_enum"), default=WatchlistStatus.saved
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="watchlist_items")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="watchlist_entries")

    def __repr__(self) -> str:
        return f"<Watchlist user_id={self.user_id} movie_id={self.movie_id} status={self.status}>"


class Mood(Base):
    __tablename__ = "moods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    genre_mappings: Mapped[list["MoodGenreMapping"]] = relationship(
        "MoodGenreMapping", back_populates="mood", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Mood id={self.id} name={self.name}>"


class MoodGenreMapping(Base):
    __tablename__ = "mood_genre_mapping"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mood_id: Mapped[int] = mapped_column(Integer, ForeignKey("moods.id", ondelete="CASCADE"), nullable=False)
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0)

    mood: Mapped["Mood"] = relationship("Mood", back_populates="genre_mappings")
    genre: Mapped["Genre"] = relationship("Genre")

    def __repr__(self) -> str:
        return f"<MoodGenreMapping mood_id={self.mood_id} genre_id={self.genre_id} weight={self.weight}>"
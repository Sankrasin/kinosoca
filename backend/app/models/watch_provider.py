# models for netflix, prime etc and which movies they have
import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.movie import Movie


class AccessType(str, enum.Enum):
    flatrate = "flatrate"
    rent = "rent"
    buy = "buy"


class WatchProvider(Base):
    __tablename__ = "watch_providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # tmdb provider id
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    logo_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    movie_links: Mapped[list["MovieWatchProvider"]] = relationship(
        "MovieWatchProvider", back_populates="provider", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<WatchProvider id={self.id} name={self.name}>"


class MovieWatchProvider(Base):
    __tablename__ = "movie_watch_providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("watch_providers.id", ondelete="CASCADE"), nullable=False
    )
    country_code: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    access_type: Mapped[AccessType] = mapped_column(
        Enum(AccessType, name="access_type_enum"), nullable=False
    )
    provider_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    movie: Mapped["Movie"] = relationship("Movie", back_populates="watch_providers")
    provider: Mapped["WatchProvider"] = relationship("WatchProvider", back_populates="movie_links")

    def __repr__(self) -> str:
        return f"<MovieWatchProvider movie_id={self.movie_id} provider_id={self.provider_id} country={self.country_code}>"